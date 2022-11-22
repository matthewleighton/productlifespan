from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import Http404
from django.contrib import messages
from django.urls import reverse

# Create your views here.
from django.http import HttpResponse

from .models import Product
from .forms import ProductForm

def index(request):
	user_products = Product.objects.filter(owner=2).order_by('purchase_date')

	context = {
		'user_products': user_products
	}

	return render(request, 'products/index.html', context)

def new(request):
	if request.method == 'POST':
		form = ProductForm(request.POST)
		if form.is_valid():
			new_product_id = form.save().id

			product_name = request.POST['name']
			messages.success(request, f'Product "{product_name}" created.')

			return redirect(f'product/{new_product_id}')
	
	else:
		form = ProductForm()

	context = {
		'form': form,
		'form_action': reverse('products:new')
	}

	return render(request, 'products/new.html', context)


def product(request, product_id):
	product = get_object_or_404(Product, pk=product_id)

	if request.method == 'POST':
		form = ProductForm(request.POST, instance=product)
		if form.is_valid():
			form.save()
	else:
		form = ProductForm(instance=product)

	template = loader.get_template('products/index.html')
	context = {
		'product': product,
		'form': form,
		'form_action': reverse(f'products:product', kwargs={'product_id': product_id})
	}

	return render(request, 'products/product.html', context)

def delete(request, product_id):
	product = get_object_or_404(Product, pk=product_id)
	product_name = product.name

	product.delete()

	messages.success(request, f'Product "{product_name}" deleted.')

	return redirect(f'/')