from django.test import SimpleTestCase
from ..models import Product

from datetime import date, timedelta

# class TestGetCurrentDaysOld(SimpleTestCase):
	
# 	def test_bought_today(self):
# 		today = date.today()

# 		product = Product(purchase_date=today)
# 		days_old = product.get_current_days_old()

# 		self.assertEquals(days_old, 0)


# 	def test_bought_yesterday(self):
# 		yesterday = date.today() - timedelta(days=1)

# 		product = Product(purchase_date=yesterday)
# 		days_old = product.get_current_days_old()

# 		self.assertEquals(days_old, 1)

# 	def test_bought_365_days_ago(self):
# 		purchase_date = date.today() - timedelta(days=365)

# 		product = Product(purchase_date=purchase_date)
# 		days_old = product.get_current_days_old()

# 		self.assertEquals(days_old, 365)

# 	def test_retired_product(self):
# 		lifespan_days = 20

# 		purchase_date   = date.today() - timedelta(days=365)
# 		retirement_date = purchase_date + timedelta(days=lifespan_days)

# 		product = Product(purchase_date=purchase_date, retirement_date=retirement_date)
# 		days_old = product.get_current_days_old(until_retirement=True)

# 		self.assertEquals(days_old, lifespan_days)

class TestGetAgeDays(SimpleTestCase):

	def test_active_product_bought_today(self):
		purchase_date = date.today()

		product = Product(purchase_date=purchase_date)
		days_old = product.get_age_days()

		self.assertEquals(days_old, 0)

	def test_active_product_bought_20_days_ago(self):
		days_since_purchase = 20
		purchase_date = date.today() - timedelta(days=days_since_purchase)

		product = Product(purchase_date=purchase_date)
		days_old = product.get_age_days()

		self.assertEquals(days_old, days_since_purchase)

	def test_retired_product(self):
		days_since_purchase = 100
		days_from_purchase_to_retirement = 40

		purchase_date   = date.today() - timedelta(days=days_since_purchase)
		retirement_date = purchase_date + timedelta(days=days_from_purchase_to_retirement)

		product = Product(purchase_date=purchase_date, retirement_date=retirement_date)
		days_old = product.get_age_days()

		self.assertEquals(days_old, days_from_purchase_to_retirement)

	def test_active_product_target(self):
		days_since_purchase = 100
		target_days_old = 400

		purchase_date = date.today() - timedelta(days=days_since_purchase)
		target_end_date = purchase_date + timedelta(days=target_days_old)

		product = Product(purchase_date=purchase_date, target_end_date=target_end_date)
		lifespan_days = product.get_age_days(when='target')

		self.assertEquals(lifespan_days, target_days_old)

	def test_retired_early_product_target(self):
		days_since_purchase = 100
		days_from_purchase_to_retirement = 150
		target_days_old = 400

		purchase_date = date.today() - timedelta(days=days_since_purchase)
		retirement_date = purchase_date + timedelta(days=days_from_purchase_to_retirement)
		target_end_date = purchase_date + timedelta(days=target_days_old)

		product = Product(purchase_date=purchase_date, retirement_date=retirement_date, target_end_date=target_end_date)
		lifespan_days = product.get_age_days(when='target')

		self.assertEquals(lifespan_days, target_days_old)