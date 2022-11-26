from django.db import models
from django.contrib.auth.models import User

from datetime import date

# Create your models here.

class Product(models.Model):
	name 		  = models.CharField('Product Name', max_length=50)
	purchase_date = models.DateField('Date Purchased')
	price 		  = models.DecimalField('Product Price', max_digits=9, decimal_places=2)
	currency 	  = models.CharField('Currency', max_length=3)
	owner		  = models.ForeignKey(User, on_delete=models.CASCADE)
	target_end_date = models.DateField('Target End Date', default=date.today)

	def get_age_string(self):
		today = date.today()
		purchase_date = self.purchase_date

		days_old = (today - purchase_date).days

		days_in_month = 365.25 / 12

		if days_old < 7:
			number = days_old
			unit = 'day' if days_old == 1 else 'days'

		elif days_old < days_in_month:
			number = days_old / 7
			unit = 'weeks'

		elif days_old < 365.25:
			number = days_old / days_in_month
			unit = 'months'

		else:
			number = days_old / 365.25
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
		# print(type(self.target_end_date))
		total_lifespan_days   = (self.target_end_date - self.purchase_date).days
		current_lifespan_days = (date.today() - self.purchase_date).days

		current_lifespan_percentage = (current_lifespan_days / total_lifespan_days)*100

		return current_lifespan_percentage