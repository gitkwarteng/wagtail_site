import hashlib
from functools import cached_property
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User as AUTH_USER_MODEL
from apps.common import AutoSlugField
from apps.common.models import BaseModel


class UserSearch(BaseModel):

    user = models.ForeignKey(
        AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_("User"))
    query = models.CharField(_("Search term"), max_length=255, db_index=True)
    date_created = models.DateTimeField(_("Date Created"), auto_now_add=True)

    class Meta:
        app_label = 'analytics'
        ordering = ['-pk']
        verbose_name = _("User search query")
        verbose_name_plural = _("User search queries")

    def __str__(self):
        return _("%(user)s searched for '%(query)s'") % {
            'user': self.user,
            'query': self.query}


class PageVisit(BaseModel):
    """
    Record web store page visits
    """
    path = models.CharField(_("URL"), max_length=500, db_index=True)
    method = models.CharField(_("Method"), max_length=10, db_index=True)
    ip_address = models.GenericIPAddressField(_("IP Address"), blank=True, null=True)
    user_agent = models.CharField(_("Browser"), max_length=255, blank=True, null=True)
    session_id = models.CharField(_("Session ID"), max_length=255, blank=True, null=True)
    location_lat = models.DecimalField(_("Latitude"), max_digits=9, decimal_places=6, blank=True, null=True)
    location_lng = models.DecimalField(_("Longitude"), max_digits=9, decimal_places=6, blank=True, null=True)
    country = models.CharField(_("Country"), max_length=3, blank=True, null=True)
    city = models.CharField(_("City"), max_length=255, blank=True, null=True)
    referer = models.CharField(_("Referer"), max_length=250, blank=True, null=True)
    advertiser = models.ForeignKey("apps.analytics.Advertiser", on_delete=models.SET_NULL, related_name="page_visits", blank=True, null=True)
    advertiser_name = models.CharField(_("Advertiser name"), blank=True, null=True)


    class Meta:
        app_label = 'analytics'
        ordering = ['-pk']
        verbose_name = _("Page visit")
        verbose_name_plural = _("Page visits")

    def __str__(self):
        return self.path

    # function to annotate page visits with location data from ip address


class Advertiser(BaseModel):
    name = models.CharField(_("Name"), max_length=150)
    slug = AutoSlugField(_("Slug"), max_length=150, populate_from="name", overwrite=True)
    tracking_no = models.CharField(_("Advertising ID"), max_length=150, blank=True, null=True,
                                   help_text=_("This ID is used to track visits to our website from this advertiser. To enable tracking, add '?wds=' to url"))

    form_fields = ["name", "tracking_no"]
    field_sequence = ["name", "tracking_no"]
    filter_fields = ["name", "tracking_no"]
    property_fields = [("visits","Visits")]
    url_name_prefix = "advertiser"

    class Meta:
        app_label = 'analytics'
        ordering = ['-pk']
        verbose_name = _("Advertiser")
        verbose_name_plural = _("Advertisers")

    def save(self, *args, **kwargs):
        if not self.tracking_no:
            self.tracking_no = hashlib.sha1(self.name.encode()).hexdigest()
        super().save(*args, **kwargs)

    @cached_property
    def visits(self):
        return self.page_visits.count()