from django.core.validators import RegexValidator, validate_ipv4_address, validate_ipv6_address
from django.core.exceptions import ValidationError
import re

def  validate_domain(value):
    domain_regex = re.compile(
            r"^(?!\-)([A-Za-z0-9\-]{1,63}\.){1,}[A-Za-z]{2,6}$"

    )
    if not domain_regex.match(value):
        raise ValidationError('ingrese un dominio o  sbdominio')



def validate_ip_domain(value):
    try:
        validate_ipv4_address(value)

    except ValidationError:
        try:
          validate_ipv6_address(value)
        except   ValidationError:
            try:
                validate_domain(value)
            except ValidationError:
                raise ValidationError('ingrese una ip o subdominio')

