import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _

class CustomPasswordValidator:
    def validate(self, password, user=None):
        if len(password) < 8:
            raise ValidationError(
                _("This password is too short. It must contain at least 8 characters."),
                code='password_too_short',
            )
        if not re.findall(r'[A-Z]', password):
            raise ValidationError(
                _("This password must contain at least one uppercase letter."),
                code='password_no_upper',
            )
        if not re.findall(r'[a-z]', password):
            raise ValidationError(
                _("This password must contain at least one lowercase letter."),
                code='password_no_lower',
            )
        if not re.findall(r'\d', password):
            raise ValidationError(
                _("This password must contain at least one digit."),
                code='password_no_digit',
            )
        # if not re.findall(r'[@$!%*?&]', password):
        #     raise ValidationError(
        #         _("This password must contain at least one special character: @$!%*?&"),
        #         code='password_no_special',
        #     )

    def get_help_text(self):
        return _(
            "Your password must contain at least 8 characters, including at least one uppercase letter, "
            "one lowercase letter, one digit"  # , and one special character: @$!%*?&
        )
