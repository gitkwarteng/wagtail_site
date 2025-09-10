import re
import enum
from django.conf import settings
from django.db import models
from django.utils.encoding import force_str
from django.utils.translation import gettext_lazy as _
from django.db.models import SlugField as DjangoSlugField

from django.template.defaultfilters import slugify

postgresql_engine_names = [
    'django.db.backends.postgresql',
    'django.db.backends.postgresql_psycopg2',
]

if settings.DATABASES['default']['ENGINE'] in postgresql_engine_names:
    from django.contrib.postgres.fields import JSONField as _JSONField
else:
    from django.db.models import JSONField as _JSONField


class JSONField(_JSONField):
    def __init__(self, *args, **kwargs):
        kwargs.update({'default': dict})
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs['default']
        return name, path, args, kwargs


class ChoiceEnumMeta(enum.EnumMeta):
    def __call__(cls, value, *args, **kwargs):
        if isinstance(value, str):
            try:
                value = cls.__members__[value]
            except KeyError:
                pass  # let the super method complain
        return super().__call__(value, *args, **kwargs)

    def __new__(metacls, classname, bases, classdict):
        labels = {}
        for key in classdict._member_names:
            source_value = classdict[key]
            if isinstance(source_value, (list, tuple)):
                try:
                    val, labels[key] = source_value
                except ValueError:
                    raise ValueError("Invalid ChoiceEnum member '{}'".format(key))
            else:
                val = source_value
                labels[key] = key.replace("_", " ").title()
            # Use dict.__setitem__() to suppress defenses against
            # double assignment in enum's classdict
            dict.__setitem__(classdict, key, val)
        cls = super().__new__(metacls, classname, bases, classdict)
        for key, label in labels.items():
            getattr(cls, key).label = label
        return cls

    @property
    def choices(cls):
        return [(k.value, k.label) for k in cls]

    @property
    def default(cls):
        try:
            return next(iter(cls))
        except StopIteration:
            return None


class ChoiceEnum(enum.Enum, metaclass=ChoiceEnumMeta):
    """
    Utility class to handle choices in Django model and/or form fields.
    Usage:

    class Color(ChoiceEnum):
        WHITE = 0, "White"
        RED = 1, "Red"
        GREEN = 2, "Green"
        BLUE = 3, "Blue"

    green = Color.GREEN

    color = forms.ChoiceField(
        choices=Color.choices,
        default=Color.default,
    )
    """
    def __str__(self):
        return force_str(self.label)


class ChoiceEnumField(models.PositiveSmallIntegerField):
    description = _("Customer recognition state")

    def __init__(self, *args, **kwargs):
        self.enum_type = kwargs.pop('enum_type', ChoiceEnum)  # fallback is required form migrations
        if not issubclass(self.enum_type, ChoiceEnum):
            raise ValueError("enum_type must be a subclass of `ChoiceEnum`.")
        kwargs.update(choices=self.enum_type.choices)
        kwargs.setdefault('default', self.enum_type.default)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        if 'choices' in kwargs:
            del kwargs['choices']
        if kwargs['default'] is self.enum_type.default:
            del kwargs['default']
        elif isinstance(kwargs['default'], self.enum_type):
            kwargs['default'] = kwargs['default'].value
        return name, path, args, kwargs

    def from_db_value(self, value, expression, connection):
        try:
            return self.enum_type(value)
        except ValueError:
            return value

    def get_prep_value(self, state):
        if isinstance(state, self.enum_type):
            return state.value
        return state

    def to_python(self, state):
        return self.enum_type(state)

    def value_to_string(self, obj):
        value = getattr(obj, self.name, obj)
        if not isinstance(value, self.enum_type):
            raise ValueError("Value must be of type {}".format(self.enum_type))
        return value.name


class AutoSlugField(DjangoSlugField):
    """ AutoSlugField

    By default, sets editable=False, blank=True.

    Required arguments:

    populate_from
        Specifies which field or list of fields the slug is populated from.

    Optional arguments:

    separator
        Defines the used separator (default: '-')

    overwrite
        If set to True, overwrites the slug on every save (default: False)

    Inspired by SmileyChris' Unique Slugify snippet:
    http://www.djangosnippets.org/snippets/690/
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('blank', True)
        kwargs.setdefault('editable', False)

        populate_from = kwargs.pop('populate_from', None)
        if populate_from is None:
            raise ValueError("missing 'populate_from' argument")
        else:
            self._populate_from = populate_from
            self._populate_from_org = populate_from
        self.separator = kwargs.pop('separator', '-')
        self.overwrite = kwargs.pop('overwrite', False)
        self.uppercase = kwargs.pop('uppercase', False)
        self.allow_duplicates = kwargs.pop('allow_duplicates', False)

        # not override parameter if it was passed explicitly,
        # so passed parameters takes precedence over the setting
        # if settings.OSCAR_SLUG_ALLOW_UNICODE:
        kwargs.setdefault('allow_unicode', False)

        super().__init__(*args, **kwargs)

    def _slug_strip(self, value):
        """
        Cleans up a slug by removing slug separator characters that occur at
        the beginning or end of a slug.

        If an alternate separator is used, it will also replace any instances
        of the default '-' separator with the new separator.
        """
        re_sep = '(?:-|%s)' % re.escape(self.separator)
        value = re.sub('%s+' % re_sep, self.separator, value)
        return re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)

    def get_queryset(self, model_cls, slug_field):
        # https://github.com/django-extensions/django-extensions/pull/854/files
        for field in model_cls._meta._get_fields():
            if field == slug_field:
                return field.model._default_manager.all()
        return model_cls._default_manager.all()

    def slugify_func(self, content):
        if content:
            return slugify(content)
        return ''

    def create_slug(self, model_instance, add):  # NOQA (too complex)
        # get fields to populate from and slug field to set
        if not isinstance(self._populate_from, (list, tuple)):
            self._populate_from = (self._populate_from, )
        slug_field = model_instance._meta.get_field(self.attname)

        # only set slug if empty and first-time save, or when overwrite=True
        if add and not getattr(model_instance, self.attname) or self.overwrite:
            # slugify the original field content and set next step to 2
            def slug_for_field(field):
                return self.slugify_func(getattr(model_instance, field))
            slug = self.separator.join(map(slug_for_field, self._populate_from))  # NOQA
            next = 2
        else:
            # get slug from the current model instance
            slug = getattr(model_instance, self.attname)
            # model_instance is being modified, and overwrite is False,
            # so instead of doing anything, just return the current slug
            return slug

        # strip slug depending on max_length attribute of the slug field
        # and clean-up
        slug_len = slug_field.max_length
        if slug_len:
            slug = slug[:slug_len]
        slug = self._slug_strip(slug)

        if self.uppercase:
            slug = slug.upper()

        original_slug = slug

        if self.allow_duplicates:
            return slug

        # exclude the current model instance from the queryset used in finding
        # the next valid slug
        queryset = self.get_queryset(model_instance.__class__, slug_field)
        if model_instance.pk:
            queryset = queryset.exclude(pk=model_instance.pk)

        # form a kwarg dict used to impliment any unique_together contraints
        kwargs = {}
        for params in model_instance._meta.unique_together:
            if self.attname in params:
                for param in params:
                    kwargs[param] = getattr(model_instance, param, None)
        kwargs[self.attname] = slug

        # increases the number while searching for the next valid slug
        # depending on the given slug, clean-up
        while not slug or queryset.filter(**kwargs):
            slug = original_slug
            end = '%s%s' % (self.separator, next)
            end_len = len(end)
            if slug_len and len(slug) + end_len > slug_len:
                slug = slug[:slug_len - end_len]
                slug = self._slug_strip(slug)
            slug = '%s%s' % (slug, end)
            kwargs[self.attname] = slug
            next += 1
        return slug

    def pre_save(self, model_instance, add):
        value = force_str(self.create_slug(model_instance, add))
        setattr(model_instance, self.attname, value)
        return value

    def get_internal_type(self):
        return "SlugField"

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['populate_from'] = self._populate_from_org
        if not self.separator == '-':
            kwargs['separator'] = self.separator
        if self.overwrite is not False:
            kwargs['overwrite'] = True
        if self.allow_duplicates is not False:
            kwargs['allow_duplicates'] = True
        return name, path, args, kwargs
