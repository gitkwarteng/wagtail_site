from wagtail.admin.viewsets.chooser import ChooserViewSet


class ProductCategoryChooserViewSet(ChooserViewSet):

    model = "shop.ProductCategory"

    icon = "tag"
    choose_one_text = "Choose a category"
    choose_another_text = "Choose another category"
    edit_item_text = "Edit this category"
    form_fields = [
        'name',
        'description',
    ]

category_chooser_view_set = ProductCategoryChooserViewSet("category_chooser")


class ClassificationChooserViewSet(ChooserViewSet):

    model = "shop.Classification"

    icon = "star"
    choose_one_text = "Choose a classification"
    choose_another_text = "Choose another classification"
    edit_item_text = "Edit this classification"
    form_fields = [
        'name',
        'description',
        'pages',
    ]

classification_chooser_view_set = ClassificationChooserViewSet("classification_chooser")

