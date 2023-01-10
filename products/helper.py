from currency_converter import CurrencyConverter
from django.contrib.auth.models import User

from babel.numbers import format_currency
import numpy as np

from pprint import pprint

class ProductLifespanHelper():

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

	def get_average_period_price(products, period, average_type='mean', format_price=True):
		average_function = np.mean if average_type == 'mean' else np.median
		averaged_price = average_function([ p.get_period_price(period=period, when='current', convert_currency=True, format_price=False) for p in products ])

		if not format_price:
			return averaged_price

		user_currency = products[0].owner.profile.currency

		return format_currency(averaged_price, user_currency, locale='en_US')		
