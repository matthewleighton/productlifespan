from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
	name 		  = models.CharField('Product Name', max_length=50)
	purchase_date = models.DateField('Date Purchased')
	price 		  = models.DecimalField('Product Price', max_digits=9, decimal_places=2)
	currency 	  = models.CharField('Currency', max_length=3)
	owner		  = models.ForeignKey(User, on_delete=models.CASCADE)
