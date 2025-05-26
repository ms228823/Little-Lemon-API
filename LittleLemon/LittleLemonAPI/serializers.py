"""
---------------------------------------------------------------------
Serializers for the Little Lemon API
---------------------------------------------------------------------

These serializers convert complex Django model instances into native Python datatypes
for rendering as JSON or XML (serialization), and handle incoming parsed data to be
converted back into Django model instances (deserialization).

Each serializer corresponds to a model in the application and may include extra logic
to control data representation and validation.
---------------------------------------------------------------------
"""


from rest_framework import serializers
from .models import Category, MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User

# Serializer for the Category model
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title', 'slug']
        read_only_fields = ['slug']


# Serializer for the MenuItem model
class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'category']


# Serializer for the Cart model with user and item details (for viewing cart)
class CartSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    menuitem = serializers.StringRelatedField()  # Displays item title instead of ID

    class Meta:
        model = Cart
        fields = '__all__'


# Serializer for adding items to the cart (simplified)
class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['menuitem', 'quantity']


# Serializer for individual items in an order
class OrderItemSerializer(serializers.ModelSerializer):
    menuitem = serializers.StringRelatedField()  # Displays item title instead of ID

    class Meta:
        model = OrderItem
        fields = ['menuitem', 'quantity', 'unit_price', 'price']


# Serializer for the Order model, including nested OrderItem data
class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    delivery_crew = serializers.StringRelatedField()  # Displays username

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew', 'status', 'total', 'date', 'order_items']


# Basic serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']
