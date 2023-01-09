from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import Http404
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm 
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect

from .models import Product, Profile
from .forms import ProductForm
from .helper import ProductLifespanHelper

from datetime import datetime
from pprint import pprint
from currency_converter import CurrencyConverter

def index(request):
	current_user_id = request.user.id

	user_products = Product.objects.filter(owner=current_user_id).order_by('-purchase_date')

	context = {
		'user_products': user_products
	}

	return render(request, 'products/index.html', context)

def new(request):
	if request.method == 'POST':
		form = ProductForm(request.POST, request.FILES)

		if form.is_valid():
			new_product = form.save(commit=False)
			new_product.owner = request.user

			target_end_date = datetime.strptime(request.POST.get('target_end_date'), '%Y-%m-%d').date()
			new_product.target_end_date = target_end_date

			new_product.save()

			product_name = request.POST['name']
			messages.success(request, f'Product "{product_name}" created.')

			return redirect(f'product/{new_product.id}')
	
	else:
		form = ProductForm()

	context = {
		'form': form,
		'form_action': reverse('products:new'),
		'submit_text': 'Create Product',
	}

	return render(request, 'products/new.html', context)

def product(request, product_id):
	product = get_object_or_404(Product, pk=product_id)

	if request.user.id != product.owner.id:
		return redirect('/')

	if request.method == 'POST':
		form = ProductForm(request.POST, request.FILES, instance=product)
		
		if form.is_valid():
			product = form.save(commit=False)
			product.owner = request.user

			target_end_date = datetime.strptime(request.POST.get('target_end_date'), '%Y-%m-%d').date()
			product.target_end_date = target_end_date
			
			product.save()


	
	else:
		form = ProductForm(instance=product)


	submit_retirement_form_text = 'Update Retirement Date' if product.is_retired() is True else 'Retire'

	graph_data = {
		'purchase_date': product.purchase_date,
		'target_end_date': product.target_end_date,
		'price': product.price
	}

	template = loader.get_template('products/index.html')
	context = {
		'product': product,
		'form': form,
		'form_action': reverse(f'products:product', kwargs={'product_id': product_id}),
		'retirement_form_action': reverse(f'products:retire', kwargs={'product_id': product_id}),
		'submit_text': 'Update Product',
		'graph_data': graph_data,
		'submit_retirement_form_text': submit_retirement_form_text,
	}

	return render(request, 'products/product.html', context)

def retire(request, product_id):
	product = get_object_or_404(Product, pk=product_id)

	if request.user.id != product.owner.id:
		return redirect('/')

	if request.method != 'POST':
		return redirect('/')


	submitted_retirement_date = request.POST.get('retirement_date')

	if submitted_retirement_date:
		retirement_date = datetime.strptime(submitted_retirement_date, '%Y-%m-%d').date()
	else:
		retirement_date = None

	product.retirement_date = retirement_date
	product.save()

	return redirect(f'/product/{product_id}')


def delete(request, product_id):
	product = get_object_or_404(Product, pk=product_id)

	if request.user.id != product.owner.id:
		return redirect('/')

	product_name = product.name

	product.delete()

	messages.success(request, f'Product "{product_name}" deleted.')

	return redirect('/')

# Update the user's currency.
# To be triggered by the navbar select field.
def currency(request):
	if request.method != 'POST':
		return redirect('/')

	user = request.user

	if user.id is None:
		return redirect('/')

	currency = request.POST.get('currency')

	valid_currencies = ProductLifespanHelper.get_currencies() + ['']

	if not hasattr(user, 'profile'):
		user.profile = Profile()

	if currency in valid_currencies:
		user.profile.currency = currency
		user.profile.save()

	return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def register_user(request):
	if request.user.is_authenticated:
		return redirect('/')

	if request.method == 'POST':
		form = UserCreationForm(request.POST)

		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']

			user = authenticate(username=username, password=password)
			login(request, user)

			messages.success(request, ('Account Created'))
			return redirect('/')

	else:
		form = UserCreationForm()

	return render(request, 'register_user.html', {'form': form})
