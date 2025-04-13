

def get_form_fields_for_page(page):
    """Get the form fields for a form."""

    from models import FormField

    if not page.form:
        return FormField.objects.none()

    form_field_ids = page.form.fields.values_list('field_id', flat=True)
    return FormField.objects.filter(id__in=form_field_ids)