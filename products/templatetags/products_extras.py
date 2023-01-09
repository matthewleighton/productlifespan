from django import template

register = template.Library()

# @register.simple_tag
# def call_method(obj, method_name, *args):
# 	method = getattr(obj, method_name)
# 	return method(*args)

# This isn't actually used anymore, but I'm leaving it here in case I later need to create other custom tags.
@register.simple_tag
def get_price_in_currency(product, currency):
	return product.price