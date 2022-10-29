import os
from django.core.exceptions import ValidationError


def validate_file_xml(value):
    ext = os.path.splitext(value.name)[1]
    if not ext.lower() == '.xml':
        raise ValidationError('Unsupported file extension.')


def validate_file_csv(value):
    ext = os.path.splitext(value.name)[1]
    if not ext.lower() == '.csv':
        raise ValidationError('Unsupported file extension.')
