from django.conf import settings
from django.core import mail
from django.core.exceptions import ImproperlyConfigured
from django.template import loader
from django.template.exceptions import TemplateDoesNotExist


def send_template_email(recipients, title_template, body_template, context, language):
    """Sends e-mail using templating system"""

    # context.update(

    # )

    mail_title_template = loader.get_template(title_template)
    mail_body_template = loader.get_template(body_template)
    title = mail_title_template.render(context).strip()
    body = mail_body_template.render(context)
    try:
        mail_body_template_html = loader.get_template(body_template)
        html_body = mail_body_template_html.render(context)
    except TemplateDoesNotExist:
        html_body = None

    try:
        email_from = getattr(settings, "DEFAULT_FROM_EMAIL")
    except AttributeError:
        raise ImproperlyConfigured(
            "DEFAULT_FROM_EMAIL setting needed for sending e-mails"
        )

    mail.send_mail(title, body, email_from, recipients, html_message=html_body)
