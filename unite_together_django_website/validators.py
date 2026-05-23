import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomPasswordValidator:
    """
    Custom password validator for Django that enforces specific password requirements.

    This validator checks if a password meets the following criteria:
    - Minimum length of 8 characters.
    - Contains at least one uppercase letter.
    - Contains at least one lowercase letter.
    - Contains at least one digit.
    - (Optional) Contains at least one special character from a specific set.
    """

    def validate(self, password, user=None):
        """
        Validates the given password according to predefined security requirements.

        Parameters:
        - password (str): The password string to validate.
        - user (User): Optional; the user instance (can be used for more customized validation).

        Raises:
        - ValidationError: If the password does not meet one or more requirements.
        """
        # Check if password has at least 8 characters
        if len(password) < 8:
            raise ValidationError(
                _(
                    "Цей пароль занадто короткий. Він повинен містити щонайменше 8 символів."
                ),
                code="password_too_short",
            )

        # Check if password has at least one uppercase letter
        if not re.findall(r"[A-Z]", password):
            raise ValidationError(
                _("Пароль повинен містити щонайменше одну велику літеру."),
                code="password_no_upper",
            )

        # Check if password has at least one lowercase letter
        if not re.findall(r"[a-z]", password):
            raise ValidationError(
                _("Пароль повинен містити щонайменше одну малу літеру."),
                code="password_no_lower",
            )

        # Check if password has at least one digit
        if not re.findall(r"\d", password):
            raise ValidationError(
                _("Пароль повинен містити щонайменше одну цифру."),
                code="password_no_digit",
            )

        # Uncomment the following block if you want to require a special character
        # Check if password has at least one special character from the specified set
        # if not re.findall(r'[@$!%*?&]', password):
        #     raise ValidationError(
        #         _("Пароль повинен містити щонайменше один спеціальний символ: @$!%*?&"),
        #         code='password_no_special',
        #     )

    def get_help_text(self):
        """
        Returns a help text explaining the password requirements.

        This text is displayed to users to help them create a compliant password.

        Returns:
        - str: A user-friendly string describing the password requirements.
        """
        return _(
            "Ваш пароль повинен містити щонайменше 8 символів, включаючи щонайменше одну велику літеру, "
            "одну малу літеру та одну цифру"  # , а також один спеціальний символ: @$!%*?&
        )
