from django.db import models
from django.utils.translation import gettext_lazy as _


class ContentAlignmentChoices(models.TextChoices):
    LEFT = 'lft', _("Left")
    TOP = 'top', _("Top")
    RIGHT = 'rt', _("Right")
    BOTTOM = 'btm', _("Bottom")
    CENTER = 'ctr', _("Center")
    TOP_LEFT = 'tpl', _("Top Left")
    TOP_RIGHT = 'tpr', _("Top Right")
    BOTTOM_LEFT = 'btl', _("Bottom Left")
    BOTTOM_RIGHT = 'btr', _("Bottom Right")


class HeadingSizeChoices(models.TextChoices):
    NONE = '', _("Size")
    H1 = 'h1', _("Header 1")
    H2 = 'h2', _("Header 2")
    H3 = 'h3', _("Header 3")
    H4 = 'h4', _("Header 4")
    H5 = 'h5', _("Header 5")



class ContentDirectionChoices(models.TextChoices):
    LEFT_TO_RIGHT = 'ltr', _("Left To Right")
    RIGHT_TO_LEFT = 'rtl', _("Right To Left")
