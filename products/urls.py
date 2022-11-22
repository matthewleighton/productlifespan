from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
	path('', views.index, name='index'),
	path('new', views.new, name='new'),
	path('product/<int:product_id>', views.product, name='product'),
	path('delete/<int:product_id>', views.delete, name='delete')
]