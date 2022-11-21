# from django.forms import ModelForm, TextInput, NumberInput, DateInput, SelectInput

from django import forms

from .models import Product

class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = '__all__'
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control'}),
			'price': forms.NumberInput(attrs={'class': 'form-control'}),
			'purchase_date': forms.DateInput(attrs={'class': 'form-control'}),
			'currency': forms.TextInput(attrs={'class': 'form-control'}),
			'owner': forms.Select(attrs={'class': 'form-control'})
		}