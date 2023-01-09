from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.core.exceptions import ObjectDoesNotExist
from django_resized import ResizedImageField

import os
from datetime import date
from time import perf_counter
from decimal import Decimal
from babel.numbers import format_currency
from currency_converter import CurrencyConverter

from pprint import pprint



def get_product_image_location(product, filename):
	file_extension = filename.split('.')[-1]
	product_id = product.id

	return f'products/uploads/{product_id}.{file_extension}'

class Product(models.Model):
	name 		  = models.CharField('Product Name', max_length=50)
	purchase_date = models.DateField('Date Purchased')
	price 		  = models.DecimalField('Product Price', max_digits=9, decimal_places=2)
	currency 	  = models.CharField('Currency', max_length=3)
	owner		  = models.ForeignKey(User, on_delete=models.CASCADE)
	target_end_date = models.DateField('Target End Date', default=date.today)
	retirement_date = models.DateField('Retirement Date', blank=True, null=True)
	image		  = ResizedImageField(size=[250, 250], upload_to=get_product_image_location, blank=True)

	DAYS_IN_MONTH = Decimal(365.25 / 12)
	DAYS_IN_YEAR  = Decimal(365.25)

	def __str__(self):
		return self.name

	# If the product already has an image, delete it when a new one is given.
	def save(self, *args, **kwargs):
		try:
			this = Product.objects.get(id=self.id)

			# Only delete the old image if a new one is actually given.
			if this.image and this.image.path != self.image.path:
				try:
					os.remove(this.image.path)
				except:
					pass
		except ObjectDoesNotExist:
			pass

		super(Product, self).save(*args, **kwargs)

	def get_image_url(self):
		if self.image:

			image_exists = self.image.storage.exists(self.image.name)

			if image_exists:
				return self.image.url

		# Default to placeholder image.
		return static('products/placeholder_image.png')

	def get_current_days_old(self, until_retirement=False):
		end_date = self.retirement_date if until_retirement else date.today()

		today = date.today()
		purchase_date = self.purchase_date

		days_old = (end_date - purchase_date).days

		return days_old

	def get_total_lifespan_days(self):
		return (self.target_end_date - self.purchase_date).days

	def get_current_lifespan_days(self):
		if self.is_retired():
			return (self.retirement_date - self.purchase_date).days
		else:
			return (date.today() - self.purchase_date).days

	def get_days_since_purchase_string(self):
		days_old = self.get_current_days_old()

		return self.format_days_to_best_unit(days_old)

	def get_lifetime_string(self):
		until_retirement = True if self.is_retired() else False
		days_old = self.get_current_days_old(until_retirement)

		return self.format_days_to_best_unit(days_old)

	def format_days_to_best_unit(self, days):
		days_in_month = 365.25 / 12

		if days < 7:
			number = days
			unit = 'day' if days == 1 else 'days'

		elif days < days_in_month:
			number = days / 7
			unit = 'weeks'

		elif days < 365.25:
			number = days / days_in_month
			unit = 'months'

		else:
			number = days / 365.25
			unit = 'years'

		return f'{round(number, 1)} {unit}'

	def get_formatted_price(self):
		user_currency = self.owner.profile.currency

		return format_currency(self.price, user_currency, locale='en_US')

		# currency_symbol = self.get_currency_symbol()
		# return f'{currency_symbol}{self.price}'

	def get_currency_symbol(self):
		if self.currency == 'GBP':
			return '£'

		return '€'

	def get_current_lifespan_percentage(self):
		total_lifespan_days   = self.get_total_lifespan_days()
		current_lifespan_days = self.get_current_lifespan_days()

		current_lifespan_percentage = (current_lifespan_days / total_lifespan_days)*100

		current_lifespan_percentage = round(current_lifespan_percentage, 2)

		return current_lifespan_percentage

	def get_remaining_lifetime(self):
		remaining_days = (self.target_end_date - date.today()).days

		return self.format_days_to_best_unit(remaining_days) + ' remaining'

	def get_end_date_string(self, format_string='%-d %b %Y'):
		return self.target_end_date.strftime(format_string)

	def format_price(self, price=None):
		original_currency = self.currency
		user_currency = self.owner.profile.currency
		purchase_date = self.purchase_date

		if not price:
			price = self.price

		if not user_currency:
			user_currency = original_currency

		# TODO: CurrencyConverter takes about 0.2 secs to load. So we need to store it somewhere, rather than reload it for each operation.
		# Attaching it to User probably isn't quite the correct way of doing this. Need to look into where it should actually be stored.
		if not hasattr(User, 'currency_converter'):
			User.currency_converter = CurrencyConverter(fallback_on_missing_rate=True)

		converted_price = User.currency_converter.convert(price, original_currency, user_currency, date=purchase_date)

		return format_currency(converted_price, user_currency, locale='en_US')

	def get_current_daily_price(self):
		until_retirement = True if self.is_retired() else False

		days_old = self.get_current_days_old(until_retirement)
		daily_price = self.price / days_old

		return daily_price

	def get_target_daily_price(self):
		total_lifespan_days = self.get_total_lifespan_days()
		return self.price / total_lifespan_days

	def get_current_daily_price_string(self):
		daily_price = self.get_current_daily_price()
		return self.format_price(daily_price)

	def get_current_weekly_price_string(self):
		weekly_price = self.get_current_daily_price() * 7
		return self.format_price(weekly_price)

	def get_current_monthly_price_string(self):
		monthly_price = self.get_current_daily_price() * self.DAYS_IN_MONTH
		return self.format_price(monthly_price)

	def get_current_yearly_price_string(self):
		yearly_price = self.get_current_daily_price() * self.DAYS_IN_YEAR
		return self.format_price(yearly_price)

	def get_target_daily_price_string(self):
		target_daily_price = self.get_target_daily_price()
		return self.format_price(target_daily_price)

	def get_target_weekly_price_string(self):
		target_weekly_price = self.get_target_daily_price() * 7
		return self.format_price(target_weekly_price)

	def get_target_monthly_price_string(self):
		target_monthly_price = self.get_target_daily_price() * self.DAYS_IN_MONTH
		return self.format_price(target_monthly_price)

	def get_target_yearly_price_string(self):
		target_yearly_price = self.get_target_daily_price() * self.DAYS_IN_YEAR
		return self.format_price(target_yearly_price)


	def get_target_daily_price_difference_string(self):
		target_daily_price = self.get_target_daily_price()
		current_daily_price = self.get_current_daily_price()

		price_difference = current_daily_price - target_daily_price

		return self.format_price(price_difference)

	def get_target_weekly_price_difference_string(self):
		target_weekly_price = self.get_target_daily_price() * 7
		current_weekly_price = self.get_current_daily_price() * 7

		price_difference = current_weekly_price - target_weekly_price

		return self.format_price(price_difference)

	def get_target_monthly_price_difference_string(self):
		target_monthly_price = self.get_target_daily_price() * self.DAYS_IN_MONTH
		current_monthly_price = self.get_current_daily_price() * self.DAYS_IN_MONTH

		price_difference = current_monthly_price - target_monthly_price

		return self.format_price(price_difference)

	def get_target_yearly_price_difference_string(self):
		target_yearly_price = self.get_target_daily_price() * self.DAYS_IN_YEAR
		current_yearly_price = self.get_current_daily_price() * self.DAYS_IN_YEAR

		price_difference = current_yearly_price - target_yearly_price

		return self.format_price(price_difference)


	# Return today if the product is not retired.
	def get_retirement_date_field_value(self):
		if self.is_retired():
			return self.retirement_date

		return date.today()

	def is_retired(self):
		retirement_date = self.retirement_date

		if retirement_date:
			return True

		return False

	def get_retire_button_text(self):
		if self.is_retired():
			return 'Un-Retire'

		return 'Retire'

	def get_retired_table_class(self):
		if self.is_retired():
			return 'retired'

		return ''

	def get_product_list_retired_note(self):
		if self.is_retired():
			return ' (RETIRED)'

		return ''

	def detail_section_css_class(self):
		if self.is_retired():
			return 'product-detail-retired'

		return 'product-detail-not-retired'

	# Returns a key which allows sorttable.js to correctly sort the date coloumn in the product list table.
	# See: https://www.kryogenix.org/code/browser/sorttable/#dates
	def get_sorttable_custom_date_key(self):
		return self.purchase_date.strftime('%Y%m%d')

class Profile(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	currency = models.CharField('Currency', max_length=3)

	def __str__(self):
		return str(self.user)