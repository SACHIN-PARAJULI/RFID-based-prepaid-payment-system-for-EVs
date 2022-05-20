from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_hex(value):
    hex_digits = set("0123456789ABCDEF")
    for char in value:
        if not (char in hex_digits):
            raise ValidationError(
                _('%(value)s is not Valid Card UID'),
                params={'value': value},
            )

def is_hex(value):
    hex_digits = set("0123456789ABCDEF")
    for char in value:
        if not (char in hex_digits):
            return False
    return True

# check if decimal less than hex FFFFFFFF i.e 4294967295 in decimal convert it into hex 

def validate_decimal(value):
    if not int(value) <= 4294967295:  
        raise ValidationError(
                _('%(value)s is not Valid Card UID'),
                params={'value': value},
            )
        

def is_valid_decimal(value):
    if int(value) <= 4294967295:  
        return True
    else:
        return False
