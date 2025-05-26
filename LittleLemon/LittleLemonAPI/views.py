"""
----------------------------------------------------------------------------
Little Lemon API - Views
----------------------------------------------------------------------------
This module contains all the API views for the Little Lemon restaurant app,
handling operations such as managing menu items, categories, carts, orders,
and user group assignments.

View Overview:

- MenuItemDetailView:
    Retrieve, update, or delete a specific menu item.
    Permissions: Authenticated users can view; only authorized users can modify.

- CategoryListCreateView:
    List all categories or create a new one.
    Permissions: Read access for authenticated users; create for privileged users.

- MenuItemListCreateView:
    List all menu items or create a new one.
    Permissions: Authenticated read; write restricted.

- MenuItemCreateView:
    Admin-only view for adding menu items.

- CartView:
    Authenticated users can add/remove items to their cart or view cart items.

- OrderView:
    Authenticated users can place orders based on their cart.
    Queryset is filtered by role:
        - Managers see all orders
        - Delivery Crew sees their assigned orders
        - Customers see only their own orders

- OrderUpdateView:
    Delivery Crew can update the status of assigned orders.

- OrderDetailView:
    Retrieve, update, or delete a specific order.
    Role-based access similar to OrderView.

- ManagerUserView:
    Admin assigns a user to the "Manager" group.

- DeliveryCrewUserView:
    Managers assign users to the "Delivery Crew" group.

Authentication: Token-based
Permissions: Role-based via custom and DRF permission classes
----------------------------------------------------------------------------
"""


# Create your views here.
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404

from .models import Category, MenuItem, Cart, Order, OrderItem
from .serializers import (
    CategorySerializer, MenuItemSerializer, CartSerializer, 
    AddToCartSerializer, OrderSerializer, UserSerializer
)
from .permissions import IsManager, IsDeliveryCrew
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveUpdateDestroyAPIView

# MenuItemDetailView:
# Retrieve, update, or delete a specific menu item.
# Permissions: Read access for authenticated users; create for privileged users.
class MenuItemDetailView(RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    
# CategoryListCreateView:
# List all categories or create a new one.
# Permissions: Read access for authenticated users; create for privileged users.
class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]

# MenuItemListCreateView:
# List all menu items or create a new one.
# Permissions: Authenticated read; write restricted.
class MenuItemListCreateView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


# Admin adds menu items
# Permissions: Admin-only access
class MenuItemCreateView(generics.CreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    permission_classes = [IsAdminUser]

# CartView:
# Add/Remove from Cart (customer)
# Permissions: Authenticated users can add/remove items to their cart or view cart items.
class CartView(generics.ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        menuitem_id = request.data['menuitem']
        quantity = int(request.data['quantity'])
        menuitem = get_object_or_404(MenuItem, id=menuitem_id)
        price = quantity * menuitem.price

        cart_item, created = Cart.objects.update_or_create(
            user=request.user,
            menuitem=menuitem,
            defaults={'quantity': quantity, 'unit_price': menuitem.price, 'price': price}
        )
        return Response({'message': 'Added to cart'}, status=201)


# Place Order (customer)
# Permissions: Authenticated users can place orders based on their cart.
# Queryset is filtered by role:
# - Managers see all orders
# - Delivery Crew sees their assigned orders
# - Customers see only their own orders
class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Manager").exists():
            return Order.objects.all()
        if user.groups.filter(name="Delivery Crew").exists():
            return Order.objects.filter(delivery_crew=user)
        return Order.objects.filter(user=user)

    def create(self, request, *args, **kwargs):
        items = Cart.objects.filter(user=request.user)
        if not items:
            return Response({"message": "Cart is empty"}, status=400)

        total = sum([item.price for item in items])
        order = Order.objects.create(user=request.user, total=total)

        for item in items:
            OrderItem.objects.create(
                order=order,
                menuitem=item.menuitem,
                quantity=item.quantity,
                unit_price=item.unit_price,
                price=item.price
            )
        items.delete()
        return Response({"message": "Order placed"}, status=201)

# OrderUpdateView:
# Update Order status (delivery crew)
# Permissions: Delivery Crew can update the status of assigned orders.
# The view is restricted to authenticated users who are part of the Delivery Crew group.
class OrderUpdateView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsDeliveryCrew]

    def patch(self, request, *args, **kwargs):
        order = self.get_object()
        order.status = request.data.get('status', order.status)
        order.save()
        return Response({'message': 'Order updated'})


# User assignment to groups
# ManagerUserView:
# Admin assigns users to manager group
# Permissions: Admin-only access
class ManagerUserView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        group = Group.objects.get(name='Manager')
        user.groups.add(group)
        return Response({'message': f'{username} added to Manager group'})

# DeliveryCrewUserView:
# Manager assigns users to delivery crew
# Permissions: Manager-only access
class DeliveryCrewUserView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def post(self, request):
        username = request.data.get('username')
        user = get_object_or_404(User, username=username)
        group = Group.objects.get(name='Delivery Crew')
        user.groups.add(group)
        return Response({'message': f'{username} added to Delivery Crew group'})
    
# OrderDetailView:
# Retrieve, update, or delete a specific order.
# Permissions: Role-based access similar to OrderView.
class OrderDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Manager").exists():
            return Order.objects.all()
        if user.groups.filter(name="Delivery Crew").exists():
            return Order.objects.filter(delivery_crew=user)
        return Order.objects.filter(user=user)