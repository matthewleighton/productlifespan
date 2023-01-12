from django import forms
from django.urls import reverse_lazy

from .models import Product
from pprint import pprint

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, MultiField, Row, Column

from .helper import ProductLifespanHelper

class ProductForm(forms.ModelForm):
	
	def __init__(self, *args, **kwargs):

		super().__init__(*args, **kwargs)

		target_price_period_choices = [
			('365.25', 'Per Year'),
			('30.4375', 'Per Month'),
			('7', 'Per Week'),
			('1', 'Per Day')
		]

		self.fields['target_age'] = forms.FloatField(
			widget=forms.NumberInput(attrs={
				'onchange': 'target_age_changed();',
				'class': 'form-control',
				'step': '0.01',
				'autocomplete': 'off'
			})
		)
		self.fields['target_price_amount'] = forms.FloatField(
			widget=forms.NumberInput(attrs={
				'onchange': 'target_price_amount_changed();',
				'class': 'form-control',
				'step': '0.01',
				'autocomplete': 'off'
			})
		)
		self.fields['target_price_period'] = forms.ChoiceField(
			choices=target_price_period_choices,
			widget=forms.Select(attrs={
				'onchange': 'target_price_period_changed();',
				'class':'form-select'
			})
		)

	class Meta:
		model = Product

		fields = [
			'name', 'price', 'purchase_date', 'currency', 'image',
			'target_end_date'
		]

		currencies = ProductLifespanHelper.get_currencies(select_field=True)

		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
			'price': forms.NumberInput(attrs={'class': 'form-control', 'autocomplete': 'off'}),
			'purchase_date': forms.DateInput(attrs={'onchange': '', 'type': 'date', 'class': 'form-control'}),
			'currency': forms.Select(choices=currencies, attrs={'class': 'form-control'}),
			'image': forms.FileInput(attrs={'class': 'form-control', 'accept': '.jpg, .jpeg, .png'}),
			'target_end_date': forms.DateInput(attrs={'onchange': 'target_end_date_changed();', 'type': 'date', 'class': 'form-control'})
		}