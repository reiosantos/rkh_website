import re

from django.core.exceptions import ValidationError


def validate_title(value):
    c = re.compile(r'^((?!\bthe\b).)*$', re.IGNORECASE)
    if not c:
        raise ValidationError("Title should not contain `the`. ")
    return value
