from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    # Cart URLs
    path('cart/', views.CartListView.as_view(), name='cart-list'),
    path('cart/add/', views.CartAddView.as_view(), name='cart-add'),
    path('cart/update/<int:pk>/', views.CartUpdateView.as_view(), name='cart-update'),
    path('cart/delete/<int:pk>/', views.CartDeleteView.as_view(), name='cart-delete'),
    
    # Checkout URLs
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    
    # Product URLs
    path('products/', views.ProductListView.as_view(), name='product-list'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    
    # Order URLs
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/<str:slug>/', views.OrderDetailView.as_view(), name='order-detail'),
]