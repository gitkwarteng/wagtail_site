from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.admin.panels import FieldPanel, MultiFieldPanel

from wagtail_site.shop.models.category import ProductCategory
from wagtail_site.shop.models.order import Order
from wagtail_site.shop.models.customer import Customer
from wagtail_site.shop.models.cart import Cart




class CategoryViewSet(ModelViewSet):
    model = ProductCategory
    icon = 'list-ul'
    menu_label = 'Categories'
    menu_order = 201
    
    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('description'),
    ]
    
    list_display = ['name', 'slug']
    search_fields = ['name', 'description']


class OrderViewSet(ModelViewSet):
    model = Order
    icon = 'doc-full'
    menu_label = 'Orders'
    menu_order = 202
    
    panels = [
        MultiFieldPanel([
            FieldPanel('number'),
            FieldPanel('customer'),
            FieldPanel('status'),
        ], heading="Order Information"),
        
        MultiFieldPanel([
            FieldPanel('total'),
            FieldPanel('created_at'),
            FieldPanel('updated_at'),
        ], heading="Order Details"),
    ]
    
    list_display = ['number', 'customer', 'status', 'total', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['number', 'customer__email']


class CustomerViewSet(ModelViewSet):
    model = Customer
    icon = 'user'
    menu_label = 'Customers'
    menu_order = 203
    
    panels = [
        FieldPanel('email'),
        FieldPanel('first_name'),
        FieldPanel('last_name'),
        FieldPanel('date_joined'),
    ]
    
    list_display = ['email', 'first_name', 'last_name', 'date_joined']
    search_fields = ['email', 'first_name', 'last_name']


class CartViewSet(ModelViewSet):
    model = Cart
    icon = 'pick'
    menu_label = 'Carts'
    menu_order = 204
    
    panels = [
        FieldPanel('customer'),
        FieldPanel('created_at'),
        FieldPanel('updated_at'),
    ]
    
    list_display = ['customer', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']