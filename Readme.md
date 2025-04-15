

Create contact page from `AbstractFormWebPage`
```python

class ContactPage(AbstractFormWebPage, Page):
    template = 'web/contact.html'

```

Use `{% include 'wagtail_site/layout/includes/site-logo.html' with logo_class="logo-dark" %}` to add site logo

Use `{% include 'wagtail_site/layout/includes/site-root.html' with root_class='tmp-btn btn-primary' %}` to add link to site root