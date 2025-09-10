from wagtail_site.shop.models.base.cart import CartModel
from wagtail_site.shop.models.base.order import OrderModel, OrderItemModel

from wagtail_site.shop.modifiers.pool import cart_modifiers_pool


def convert_cart_to_order(*, cart: "CartModel"):
    """
    Convert the cart into an order, applying all cart modifiers.
    """
    # Create the order
    order = OrderModel.objects.create(
        customer=cart.customer,
        subtotal=cart.subtotal,
        total=cart.total,
        extra=cart.extra.copy()
    )

    # Convert cart items to order items
    for cart_item in cart.items.filter(quantity__gt=0):
        OrderItemModel.objects.create(
            order=order,
            product=cart_item.product,
            product_code=cart_item.product_code or cart_item.product.product_code,
            quantity=cart_item.quantity,
            unit_price=cart_item.unit_price,
            line_total=cart_item.line_total,
            extra=cart_item.extra.copy()
        )

        # Iterate over the registered modifiers, and search for the active payment service provider
        for modifier in cart_modifiers_pool.get_payment_modifiers():
            if modifier.is_active(cart.extra.get('payment_modifier')):
                expression = modifier.payment_provider.get_payment_request(cart, request)
                # response_data.update(expression=expression)
                break

    return order