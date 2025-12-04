from wagtail.admin.panels import InlinePanel, MultiFieldPanel, FieldRowPanel

from wagtail.snippets.views.snippets import SnippetViewSet, SnippetViewSetGroup

from wagtail_site.shop.models import ProductCategory, Product, Customer, Order, Notification, Classification


class ProductCategoryViewSet(SnippetViewSet):
    model = ProductCategory
    icon = 'tag'
    menu_label = 'Category'
    name = 'category'
    inspect_view_enabled = True
    list_display = ['name', 'description']
    panels = [
        'name',
        'description',
    ]

class ClassificationViewSet(SnippetViewSet):
    model = Classification
    icon = 'pick'
    menu_label = 'Classification'
    name = 'classification'
    inspect_view_enabled = True
    list_display = ['name',]
    panels = [
        'name',
        'description',
        'pages',
    ]


class ProductViewSet(SnippetViewSet):
    model = Product
    icon = 'table'
    menu_label = 'Product'
    inspect_view_enabled = True
    name = 'product'
    list_display = [
        'name', 'code', 'unit_price', 'category','active'
    ]
    list_filter = ['name', 'caption', 'category']

    panels = [
        MultiFieldPanel([
            'code',
            'name',
            'caption',

            FieldRowPanel([
                'unit_price',
                'quantity',
            ]),
            'description',
            'active',
        ], heading="Basic Information"),

        MultiFieldPanel([
            'checkout_url',
            'category',
            'sample_image',
        ], heading="Display Settings"),

        InlinePanel('images'),
        InlinePanel('classifications')
    ]

    def get_form_fields(self):
        return super().get_form_fields()


class CustomerViewSet(SnippetViewSet):
    model = Customer
    icon = 'group'
    menu_label = 'Customers'
    name = "customer"
    list_display = [
        'number', 'recognized', 'last_access'
    ]
    panels = [
        'number', 'recognized',
    ]


class NotificationViewSet(SnippetViewSet):
    model = Notification
    icon = 'mail'
    menu_label = 'Notifications'
    menu_order = 300
    add_to_settings_menu = True

    panels = [
        'name',
        'notify',
        'recipient',
        'mail_template',
        'transition_target',
        InlinePanel('attachments', label="Attachments"),
    ]

    list_display = ['name', 'transition_target', 'mail_template']
    search_fields = ['name', 'mail_template']


class OrdersViewSet(SnippetViewSet):
    model = Order
    icon = 'bars'
    menu_label = 'Orders'
    name = "order"

    panels = [
        MultiFieldPanel([
            'number',
            'customer',
            'status',
        ], heading="Order Information"),
    ]

    list_display = ['number', 'customer', 'status', '_total', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['number', 'customer__email']


class ShopViewSetGroup(SnippetViewSetGroup):
    items = [ProductCategoryViewSet, ProductViewSet, ClassificationViewSet, CustomerViewSet, OrdersViewSet, NotificationViewSet]
    menu_icon = 'globe'
    menu_label = 'Shop'

    menu_order = 400

    add_to_admin_menu = True
