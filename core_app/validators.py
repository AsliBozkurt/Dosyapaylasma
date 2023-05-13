import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class NumberValidator(object):
    @staticmethod
    def validate(password, user=None):
        if not re.findall("\d", password):
            raise ValidationError(
                _("At least one number character : 0-9."),
                code="password_no_number",
            )

    @staticmethod
    def get_help_text():
        return _("At least one number character : 0-9.")


class UppercaseValidator(object):
    @staticmethod
    def validate(password, user=None):
        if not re.findall("[A-Z]", password):
            raise ValidationError(
                _("At least one uppercase character : A-Z."),
                code="password_no_upper",
            )

    @staticmethod
    def get_help_text():
        return _("At least one uppercase character : A-Z.")


class LowercaseValidator(object):
    @staticmethod
    def validate(password, user=None):
        if not re.findall("[a-z]", password):
            raise ValidationError(
                _("At least one lowercase character : a-z."),
                code="password_no_lower",
            )

    @staticmethod
    def get_help_text():
        return _("At least one lowercase character : a-z.")


class SymbolValidator(object):
    @staticmethod
    def validate(password, user=None):
        if not re.findall("[()[\]{}|\\`~!@#$%^&*_\-+=;:'\",<>./?]", password):
            raise ValidationError(
                _("At least one symbol character :" + "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"),
                code="password_no_symbol",
            )

    @staticmethod
    def get_help_text():
        return _("At least one symbol character :" + "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?")
