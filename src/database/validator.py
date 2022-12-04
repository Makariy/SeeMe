from typing import Any, Type
from tortoise import Model
from tortoise.fields.base import Field


def validate_field_value(field: Field, value: Any):
    for validator in field.validators:
        validator.__call__(value)


def validate_fields(model: Type[Model], **fields):
    model_fields = model._meta.fields_map
    for field in fields:
        validate_field_value(model_fields[field], fields[field])
