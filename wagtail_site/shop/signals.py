from django.dispatch import Signal

customer_recognized = Signal()

def email_queued():
    """
    If SESSION_REDIS is configured, inform a separately running worker engine, that
    emails are ready for delivery. Call this function every time an email has been
    handled over to the Post-Office.
    """
    # redis_con.publish('django-SHOP', 'send_queued_mail')
