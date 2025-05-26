"""
---------------------------------------------------------------------
Admin Registration for Little Lemon Project
---------------------------------------------------------------------

This file registers the models for the Little Lemon project to appear
in the Django admin interface. This allows administrators to manage
the database content through a user-friendly interface.

---------------------------------------------------------------------
"""

from django.contrib import admin
from .models import Category, MenuItem, Cart, Order, OrderItem

# Register your models here.

# Register the Category model with the Django admin interface
admin.site.register(Category)
# Register the MenuItem model with the Django admin interface
admin.site.register(MenuItem)
# Register the Cart model with the Django admin interface
admin.site.register(Cart)
# Register the Order model with the Django admin interface
admin.site.register(Order)
# Register the OrderItem model with the Django admin interface
admin.site.register(OrderItem)