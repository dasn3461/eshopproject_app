from django.contrib import admin
from .models import Customer,Category,Product,Cart,CartProduct,Order,Admin,ProductImage
# Register your models here.

admin.site.register([Customer,Category,Product,Cart,CartProduct,Order,Admin,ProductImage])
