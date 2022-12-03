from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

from datetime import date
from decimal import Decimal

# Create your models here.

class Product(models.Model):
	name 		  = models.CharField('Product Name', max_length=50)
	purchase_date = models.DateField('Date Purchased')
	price 		  = models.DecimalField('Product Price', max_digits=9, decimal_places=2)
	currency 	  = models.CharField('Currency', max_length=3)
	owner		  = models.ForeignKey(User, on_delete=models.CASCADE)
	target_end_date = models.DateField('Target End Date', default=date.today)
	image		  = models.ImageField(upload_to='products/uploads/', blank=True)

	DAYS_IN_MONTH = Decimal(365.25 / 12)
	DAYS_IN_YEAR  = Decimal(365.25)

	def get_image_url(self):
		if self.image:
			return self.image.url

		# Default to placeholder image.
		return static('products/placeholder_image.png')

	def get_current_days_old(self):
		today = date.today()
		purchase_date = self.purchase_date

		days_old = (today - purchase_date).days

		return days_old

	def get_total_lifespan_days(self):
		return (self.target_end_date - self.purchase_date).days

	def get_current_lifespan_days(self):
		return (date.today() - self.purchase_date).days

	def get_age_string(self):
		days_old = self.get_current_days_old()

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
		currency_symbol = self.get_currency_symbol()

		return f'{currency_symbol}{self.price}'

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

	def format_price(self, price):
		price = round(price, 2)
		currency_symbol = self.get_currency_symbol()

		return f'{currency_symbol}{price}'

	def get_current_daily_price(self):
		days_old = self.get_current_days_old()
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

		