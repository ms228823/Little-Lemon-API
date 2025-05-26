"""
----------------------------------------------------------------------------
Little Lemon API - URL Configuration
----------------------------------------------------------------------------
Defines all the API endpoints for the Little Lemon restaurant backend.

Routes:
- categories/                   -> List or create menu categories
- menu-items/                  -> List or create menu items
- menu-items/create/           -> Admin-only endpoint to add new menu items
- menu-items/<int:pk>/         -> Retrieve, update, or delete a specific menu item

- cart/                        -> Customer cart operations (view, add, remove)

- orders/                      -> Place an order or list orders (role-based visibility)
- orders/<int:pk>/             -> Retrieve, update, or delete a specific order
- orders/<int:pk>/update/      -> Delivery crew updates order status

- users/manager/               -> Admin assigns user to "Manager" group
- users/delivery-crew/         -> Manager assigns user to "Delivery Crew" group

Each route is mapped to its corresponding class-based view, with permissions
enforced based on user roles and authentication status.
----------------------------------------------------------------------------
"""

from django.urls import path
from . import views
from .views import CategoryListCreateView, MenuItemListCreateView, MenuItemListCreateView, MenuItemDetailView, OrderDetailView

urlpatterns = [
    path('categories/', CategoryListCreateView.as_view(), name='categories'),
    path('menu-items/', MenuItemListCreateView.as_view(), name='menu-items'),
    path('menu-items/create/', views.MenuItemCreateView.as_view()),

    path('cart/', views.CartView.as_view()),
    path('orders/', views.OrderView.as_view()),
    path('orders/<int:pk>/update/', views.OrderUpdateView.as_view()),

    path('users/manager/', views.ManagerUserView.as_view()),
    path('users/delivery-crew/', views.DeliveryCrewUserView.as_view()),
    
    path('menu-items/<int:pk>/', MenuItemDetailView.as_view(), name='menu-item-detail'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
]
