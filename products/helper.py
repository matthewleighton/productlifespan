from currency_converter import CurrencyConverter
from django.contrib.auth.models import User

class ProductLifespanHelper():

	# TODO: CurrencyConverter takes about 0.2 secs to load. So we need to store it somewhere, rather than reload it for each operation.
	# Attaching it to User probably isn't quite the correct way of doing this. Need to look into where it should actually be stored.
	def initialize_currency_converter():
		if not hasattr(User, 'currency_converter'):
			User.currency_converter = CurrencyConverter(fallback_on_missing_rate=True)

	def get_currencies(select_field=False):
		__class__.initialize_currency_converter()

		currencies = list(User.currency_converter.currencies)
		currencies.sort()

		currencies.insert(0, currencies.pop(currencies.index('USD')))
		currencies.insert(0, currencies.pop(currencies.index('GBP')))
		currencies.insert(0, currencies.pop(currencies.index('EUR')))

		if not select_field:
			return currencies

		return [(curr, curr) for curr in currencies]