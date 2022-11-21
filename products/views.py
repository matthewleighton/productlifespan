from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import Http404
from django.contrib import messages

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
	form = ProductForm()


	if request.method == 'POST':
		form = ProductForm(request.POST)
		if form.is_valid():
			new_product = form.save()
			product_id = new_product.id

			product_name = request.POST['name']
			messages.success(request, f'Product "{product_name}" created.')

			return redirect(f'product/{product_id}')

	context = {'form': form}

	return render(request, 'products/new.html', context)


def product(request, product_id):
	product = get_object_or_404(Product, pk=product_id)

	form = ProductForm(instance=product)

	template = loader.get_template('products/index.html')
	context = {
		'product': product,
		'form': form
	}

	return render(request, 'products/product.html', context)