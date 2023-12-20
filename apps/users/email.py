from djoser import email


class ConfirmationEmail(email.ConfirmationEmail):
    template_name = "users/confirmation.html"

    def get_context_data(self):
        context = super().get_context_data()

        # user = context.get("user")
        return context


class PasswordResetEmail(email.PasswordResetEmail):
    template_name = "users/password_reset.html"


class PasswordChangedConfirmationEmail(email.PasswordChangedConfirmationEmail):
    template_name = "users/password_changed.html"
