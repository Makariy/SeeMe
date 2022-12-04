from typing import Union, Type, Any, List
from tortoise import Model, fields
from tortoise.validators import (
    Validator,
    ValidationError,
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
    MaxLengthValidator
)
import uuid
import pydantic


class BaseModel(Model):
    id = fields.IntField(pk=True)
    uuid = fields.UUIDField(default=uuid.uuid4, generated=False)

    class Meta:
        abstract = True


class ChoiceValidator(Validator):
    def __init__(self, choices: List[Any]):
        self.choices = choices

    def __call__(self, value: Any):
        if value not in self.choices:
            raise ValidationError(f"Received incorrect value: '{value}', choices are: '{self.choices}'")


class NotNullValidator(Validator):
    def __call__(self, *args, **kwargs):
        if len(args) != 1 or args[0] is None:
            raise ValidationError(f"Provided value is None")


SEXES = ['MALE', 'FEMALE']


class Point(pydantic.BaseModel):
    lat: float
    lon: float

    def __init__(self, lat: float, lon: float):
        super().__init__(lat=lat, lon=lon)


class LocationField(fields.base.Field):
    SQL_TYPE = "POINT"
    NULL = False

    def to_python_value(self, value: Any) -> Point:
        self.validate(value)
        if type(value) is dict:
            return Point(lat=value['lat'], lon=value['lon'])
        if type(value) is Point:
            return Point(lat=value.lat, lon=value.lon)
        return Point(lat=value.x, lon=value.y)

    def to_db_value(self, value: Any, instance: Union[Type[Model], Model]) -> Any:
        if type(value) is dict:
            return [value['lat'], value['lon']]
        if type(value) is Point:
            return [value.lat, value.lon]
        return [value.x, value.y]


class Client(BaseModel):
    telegram_id = fields.BigIntField(null=False, default=-1, unique=True)  # User's id in the telegram API
    name = fields.CharField(
        max_length=64,
        null=False,
        validators=[MinLengthValidator(2), MaxLengthValidator(20)]
    )                           # User's name
    surname = fields.CharField(
        max_length=64,
        null=True,
        validators=[MaxLengthValidator(20)]
    )                           # User's surname
    age = fields.IntField(
        validators=[MinValueValidator(10), MaxValueValidator(120)]
    )                           # Age with an integer
    location = LocationField(validators=[NotNullValidator()])  # User's location
    sex = fields.CharField(
        max_length=36,
        validators=[ChoiceValidator(choices=SEXES)]
    )                           # Choices from SEXES
    target = fields.CharField(
        max_length=36,
        validators=[ChoiceValidator(choices=SEXES)]
    )                           # Choices from SEXES
    description = fields.TextField(
        max_length=1024,
        null=False,
        default=""
    )                           # User's description
    image_id = fields.CharField(
        null=False,
        max_length=512
    )


