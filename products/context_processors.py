from .helper import ProductLifespanHelper

# This allows us to obtain the currencies on any page.
def categories_processor(request):
	currencies = ProductLifespanHelper.get_currencies(select_field=True)

	default = ('', 'Original')

	currencies.insert(0, default)

	return {'currencies': currencies}