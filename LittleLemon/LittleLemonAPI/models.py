"""
---------------------------------------------------------------------
Models for the Little Lemon project
---------------------------------------------------------------------

This file contains the models used by the Little Lemon API. These models
represent the data structures for the menu items, categories, shopping 
cart, orders, and order items. Each model corresponds to a table in the 
database.

---------------------------------------------------------------------
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify


# Create your models here.

class Category(models.Model):
    """
    Category model to categorize menu items (e.g., Appetizers, Main Course).
    The 'slug' field is automatically generated based on the title for URL-friendly identification.
    """
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        """Override the save method to auto-generate a slug if not provided."""
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class MenuItem(models.Model):
    """
    MenuItem model to store individual items available for purchase in the restaurant.
    Each item belongs to a specific category (e.g., appetizers or main course) and has a price.
    """
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)  # Protect: Prevent deletion of category
    featured = models.BooleanField(default=False)  # Whether the menu item is featured on the menu

    def __str__(self):
        return self.title


class Cart(models.Model):
    """
    Cart model for storing the user's selected menu items before placing an order.
    A user can have multiple items in their cart.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        """Ensure that a user cannot have duplicate entries for the same menu item in their cart."""
        unique_together = ('user', 'menuitem')


class Order(models.Model):
    """
    Order model to store customer orders. Each order has an associated user and can be delivered by a crew member.
    The status indicates whether the order has been delivered (True = delivered, False = not delivered).
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_crew = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='deliveries', blank=True)
    status = models.BooleanField(default=False)  # False = not delivered
    total = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateField(auto_now_add=True)  # Automatically set the order creation date

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"


class OrderItem(models.Model):
    """
    OrderItem model to store items associated with an order. Each item refers to a specific menu item and quantity.
    This model helps to break down an order into its individual items.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    menuitem = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    class Meta:
        """Ensure that a menu item can only appear once in an order."""
        unique_together = ('order', 'menuitem')

    def __str__(self):
        return f"{self.quantity} x {self.menuitem.title} (Order {self.order.id})"
