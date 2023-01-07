from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

from . import views

app_name = 'products'

urlpatterns = [
	# path('admin/', admin.site.urls),
	path('', views.index, name='index'),
	path('new', views.new, name='new'),
	path('product/<int:product_id>', views.product, name='product'),
	path('retire/<int:product_id>', views.retire, name='retire'),
	path('delete/<int:product_id>', views.delete, name='delete'),
	# *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    # NOTE: Is it correct that these are in the products urls file?
    # They were originally just in the main productlifespan one, but this was stopping the login and admin pages from working.
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
