from django import template

register = template.Library()

@register.simple_tag
def get_period_price(product, period, when, convert_currency=True, format_price=True):
	return product.get_period_price(period, when, convert_currency=convert_currency, format_price=format_price)

@register.simple_tag
def get_period_price_difference(product, period, convert_currency=True, format_price=True):
	return product.get_period_price_difference(period, convert_currency=convert_currency, format_price=format_price)