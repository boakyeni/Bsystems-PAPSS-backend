from djoser import email


class ConfirmationEmail(email.ConfirmationEmail):
    template_name = "users/confirmation.html"
