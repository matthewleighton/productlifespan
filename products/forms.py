# from django.forms import ModelForm, TextInput, NumberInput, DateInput, SelectInput

from django import forms

from .models import Product

class ProductForm(forms.ModelForm):
	class Meta:
		model = Product
		# fields = '__all__'
		fields = ['name', 'price', 'purchase_date', 'currency']
		widgets = {
			'name': forms.TextInput(attrs={'class': 'form-control'}),
			'price': forms.NumberInput(attrs={'class': 'form-control'}),
			'purchase_date': forms.DateInput(attrs={'class': 'form-control'}),
			'currency': forms.TextInput(attrs={'class': 'form-control'}),
			# 'owner': forms.Select(attrs={'class': 'form-control'})
		}

# class LifespanForm(forms.ModelForm):
# 	class Meta:
# 		model = Product
# 		fields = ['target_end_date']
# 		widgets = {
# 			'target_end_date'
# 		}