from currency_converter import CurrencyConverter

class ProductLifespanHelper():

	def get_currencies(select_field=False):

		c = CurrencyConverter()

		currencies = list(c.currencies)

		currencies.sort()

		currencies.insert(0, currencies.pop(currencies.index('USD')))
		currencies.insert(0, currencies.pop(currencies.index('GBP')))
		currencies.insert(0, currencies.pop(currencies.index('EUR')))

		if not select_field:
			return currencies

		return [(curr, curr) for curr in currencies]