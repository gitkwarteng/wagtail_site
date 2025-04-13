import logging

from django.db import IntegrityError
from django.db.models import F
from django.dispatch import receiver

# from search.signals import user_search

from .models import UserSearch


# Helpers

logger = logging.getLogger('analytics')
