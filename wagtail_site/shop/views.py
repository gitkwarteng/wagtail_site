from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db import transaction
from django.utils.translation import gettext_lazy as _

from wagtail_site.shop.models.base.cart import CartModel, CartItemModel
from wagtail_site.shop.models.base.order import OrderModel
from wagtail_site.shop.models.base.product import ProductModel
from wagtail_site.shop.exceptions import ProductNotAvailable
from wagtail_site.shop.operations.checkout import convert_cart_to_order


class CartListView(ListView):
    model = CartItemModel
    template_name = 'shop/cart/list.html'
    context_object_name = 'cart_items'
    
    def get_queryset(self):
        cart = CartModel.objects.get_from_request(self.request)
        return CartItemModel.objects.filter(cart=cart)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = CartModel.objects.get_from_request(self.request)
        return context


class CartAddView(CreateView):
    model = CartItemModel
    fields = ['quantity']
    
    def post(self, request, *args, **kwargs):
        cart = CartModel.objects.get_from_request(request)
        product = get_object_or_404(ProductModel, pk=request.POST.get('product_id'))
        quantity = int(request.POST.get('quantity', 1))
        
        cart_item = cart.add_product(product, quantity)
        
        if request.headers.get('Accept') == 'application/json':
            return JsonResponse({'success': True, 'cart_item_id': cart_item.id})
        
        messages.success(request, _('Product added to cart'))
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


class CartUpdateView(UpdateView):
    model = CartItemModel
    fields = ['quantity']
    
    def post(self, request, *args, **kwargs):
        cart_item = self.get_object()
        quantity = int(request.POST.get('quantity', 0))
        
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
        
        if request.headers.get('Accept') == 'application/json':
            return JsonResponse({'success': True})
        
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/cart/'))


class CartDeleteView(DeleteView):
    model = CartItemModel
    
    def delete(self, request, *args, **kwargs):
        cart_item = self.get_object()
        cart_item.delete()
        
        if request.headers.get('Accept') == 'application/json':
            return JsonResponse({'success': True})
        
        return HttpResponseRedirect('/cart/')


class CheckoutView(CreateView):
    model = OrderModel
    template_name = 'shop/checkout/checkout.html'
    fields = []
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = CartModel.objects.get_from_request(self.request)
        return context
    
    def post(self, request, *args, **kwargs):
        cart = CartModel.objects.get_from_request(request)
        
        try:
            with transaction.atomic():
                cart.update(request, raise_exception=True)
                order = convert_cart_to_order(cart=cart)
                cart.delete()
                
                if request.headers.get('Accept') == 'application/json':
                    return JsonResponse({'success': True, 'order_id': order.id})
                
                return HttpResponseRedirect(f'/orders/{order.get_number()}/')
                
        except ProductNotAvailable as exc:
            messages.error(request, _('Product unavailable: {}').format(exc.product.product_name))
            
            if request.headers.get('Accept') == 'application/json':
                return JsonResponse({'error': str(exc)}, status=400)
            
            return HttpResponseRedirect('/cart/')


class ProductListView(ListView):
    model = ProductModel
    template_name = 'shop/catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 16
    
    def get_queryset(self):
        return ProductModel.objects.filter(active=True)


class ProductDetailView(DetailView):
    model = ProductModel
    template_name = 'shop/catalog/product_detail.html'
    context_object_name = 'product'
    slug_field = 'slug'
    
    def get_queryset(self):
        return ProductModel.objects.filter(active=True)


class OrderListView(ListView):
    model = OrderModel
    template_name = 'shop/orders/list.html'
    context_object_name = 'orders'
    paginate_by = 15
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return OrderModel.objects.filter(customer=self.request.user).order_by('-created_at')
        return OrderModel.objects.none()


class OrderDetailView(DetailView):
    model = OrderModel
    template_name = 'shop/orders/detail.html'
    context_object_name = 'order'
    slug_field = 'number'
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            return OrderModel.objects.filter(customer=self.request.user)
        return OrderModel.objects.none()