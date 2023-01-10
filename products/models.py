from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.core.exceptions import ObjectDoesNotExist
from django_resized import ResizedImageField

from .helper import ProductLifespanHelper

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

	DAYS_IN_YEAR  = Decimal(365.25)
	DAYS_IN_MONTH = Decimal(DAYS_IN_YEAR / 12)

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
		if days < 7:
			number = days
			unit = 'day' if days == 1 else 'days'

		elif days < self.DAYS_IN_MONTH:
			number = days / 7
			unit = 'weeks'

		elif days < self.DAYS_IN_YEAR:
			number = days / self.DAYS_IN_MONTH
			unit = 'months'

		else:
			number = days / self.DAYS_IN_YEAR
			unit = 'years'

		return f'{round(number, 1)} {unit}'

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

	def format_price(self, price=None, convert=True):
		if convert:
			price = self.convert_currency(price)

		currency = self.owner.profile.currency
		if not currency:
			currency = self.currency
	
		return format_currency(price, currency, locale='en_US')

	def convert_currency(self, price=None):
		original_currency = self.currency
		user_currency = self.owner.profile.currency
		purchase_date = self.purchase_date

		if not price:
			price = self.price

		if not user_currency:
			user_currency = original_currency

		ProductLifespanHelper.initialize_currency_converter()
		converted_price = User.currency_converter.convert(price, original_currency, user_currency, date=purchase_date)

		return converted_price

	

	# Return the cost of the product for a given period (day/week/month/year).
	# Use convert_currency to specify whether the currency should be converted into the user's default currency.
	# Use format_price to specify if the final price value should be formatted into a currency string.
	# Use "when" to specify either "current" or "target".
	def get_period_price(self, period='day', when='current', convert_currency=True, format_price=True):
		if when == 'current':
			daily_price = self.get_current_daily_price()
		else:
			daily_price = self.get_target_daily_price()

		multiplier = {
			'day': 1, 'week': 7, 'month': self.DAYS_IN_MONTH, 'year': self.DAYS_IN_YEAR
		}.get(period)

		period_price = daily_price * multiplier

		if convert_currency:
			period_price = self.convert_currency(period_price)

		if format_price:
			period_price = self.format_price(period_price, convert=False)

		return period_price


	def get_target_daily_price(self):
		total_lifespan_days = self.get_total_lifespan_days()
		return self.price / total_lifespan_days

	def get_current_daily_price(self):
		until_retirement = True if self.is_retired() else False

		days_old = self.get_current_days_old(until_retirement)
		return self.price / days_old


	def get_period_price_difference(self, period, convert_currency=True, format_price=True):
		current_price = self.get_period_price(period=period, when='current', convert_currency=convert_currency, format_price=False)
		target_price  = self.get_period_price(period=period, when='target',  convert_currency=convert_currency, format_price=False)

		price_difference = current_price - target_price

		if not format_price:
			return price_difference

		return self.format_price(price_difference, convert=False)



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