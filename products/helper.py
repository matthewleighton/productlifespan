from currency_converter import CurrencyConverter
from django.contrib.auth.models import User

# from .models import Product

from babel.numbers import format_currency
import numpy as np

from pprint import pprint

class ProductLifespanHelper():

	DAYS_IN_YEAR = 365.25
	DAYS_IN_MONTH = DAYS_IN_YEAR / 12

	# TODO: CurrencyConverter takes about 0.2 secs to load. So we need to store it somewhere, rather than reload it for each operation.
	# Attaching it to User probably isn't quite the correct way of doing this. Need to look into where it should actually be stored.
	def initialize_currency_converter():
		if not hasattr(User, 'currency_converter'):
			User.currency_converter = CurrencyConverter(fallback_on_missing_rate=True, fallback_on_wrong_date=True)

	def get_currencies(select_field=False):
		__class__.initialize_currency_converter()

		currencies = list(User.currency_converter.currencies)
		currencies.sort()

		currencies.insert(0, currencies.pop(currencies.index('USD')))
		currencies.insert(0, currencies.pop(currencies.index('GBP')))
		currencies.insert(0, currencies.pop(currencies.index('EUR')))

		if not select_field:
			return currencies

		select_options = [(curr, curr) for curr in currencies]

		return select_options

	def get_average_price(products, average_type='mean', format_price=True):
		average_function = np.mean if average_type == 'mean' else np.median
		averaged_price = average_function([p.convert_currency() for p in products])

		if not format_price:
			return averaged_price

		user_currency = products[0].owner.profile.currency

		return format_currency(averaged_price, user_currency, locale='en_US')

	def get_average_period_price(products, period, when='current', average_type='mean', format_price=True):
		average_function = __class__.get_average_function(average_type)

		averaged_price = average_function([ p.get_period_price(period=period, when=when, convert_currency=True, format_price=False) for p in products ])

		if not format_price:
			return averaged_price

		user_currency = products[0].owner.profile.currency

		return format_currency(averaged_price, user_currency, locale='en_US')		

	def get_total_period_price(products, period, when='current', format_price=True):
		return __class__.get_average_period_price(products, period, when=when, average_type='sum', format_price=format_price)

	def get_average_product_age(products, average_type='mean', when='current'):
		average_function = __class__.get_average_function(average_type)
		age_in_days = average_function([ p.get_age_days(when=when) for p in products ])

		return __class__.format_days_to_best_unit(age_in_days)

	def get_average_lifespan_percentage(products, average_type, format_percentage=True):
		average_function = __class__.get_average_function(average_type)

		average_lifespan_percentage = average_function([ p.get_current_lifespan_percentage(round_value=False) for p in products ])

		if format_percentage:
			return str(round(average_lifespan_percentage, 2)) + '%'
		
		return average_lifespan_percentage


	def get_average_function(average_type):
		average_function = {
			'mean': np.mean,
			'median': np.median,
			'sum': np.sum,
			'standard_deviation': np.std
		}.get(average_type)

		return average_function

	def format_days_to_best_unit(days):
		abs_days = abs(days)

		if abs_days < 7:
			number = days
			unit = 'day' if days == 1 else 'days'

		elif abs_days < __class__.DAYS_IN_MONTH:
			number = days / 7
			unit = 'weeks'

		elif abs_days < __class__.DAYS_IN_YEAR:
			number = days / __class__.DAYS_IN_MONTH
			unit = 'months'

		else:
			number = days / __class__.DAYS_IN_YEAR
			unit = 'years'

		return f'{round(number, 1)} {unit}'

	# Return the products of a given user.
	# filter_name can be either "active", "retires", or "all".
	def get_user_products_by_filter(user, filter_name):
		from .models import Product # Importing here to avoid circular import.

		if not user.is_authenticated:
			return Product.objects.none()

		products = Product.objects.filter(owner=user)

		if filter_name == 'active':
			products = products.filter(retirement_date=None)
		elif filter_name == 'retired':
			products = products.exclude(retirement_date=None)

		return products