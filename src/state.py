from typing import Union, Type, Self, Dict, Any, List
from enum import Enum
from pydantic import BaseModel, root_validator
from models import Client, Point
import database.validator


class SECTION(Enum):
    CHOOSE_SECTION = "CHOOSE_SECTION"
    SEARCH_FOR_PROFILES = "SEARCH_FOR_PROFILES"
    EDIT_PROFILE = "EDIT_PROFILE"
    NOT_LOGGED = "NOT_LOGGED"


class BaseStateData(BaseModel):
    pass


class ProfileData(BaseStateData):
    name: str
    surname: str
    age: int
    sex: str      # One of SEXES
    target: str   # One of SEXES
    location: Point
    description: str
    image_id: str

    def get_fields(self) -> Dict[str, Any]:
        return self.dict()

    def get_unfilled_field(self) -> str:
        fields = list(self.__fields__.keys())
        for initialized_field in self.__fields_set__:
            fields.remove(initialized_field)
        if len(fields) != 0:
            return fields[0]

    def validate_initialized_fields(self: Type[Self]):
        return database.validator.validate_fields(Client, **self.get_fields())

    def validate_model(self: Type[Self]):
        super().validate(self)
        database.validator.validate_fields(model=Client, **self.get_fields())

    class Config:
        arbitrary_types_allowed = True


class ChooseSectionData(BaseStateData):
    pass


class SearchForProfilesData(BaseStateData):
    offset: int = 0
    current_profile: int
    search_list_ids: List[int]


class CreateProfileData(ProfileData):
    telegram_id: int


class EditProfileData(ProfileData):
    previous_profile_data: ProfileData

    def get_fields(self) -> Dict[str, Any]:
        return super().dict(exclude={"previous_profile_data"})


DATA_TO_SECTION_MAPPING = {
    ChooseSectionData: SECTION.CHOOSE_SECTION,
    SearchForProfilesData: SECTION.SEARCH_FOR_PROFILES,
    CreateProfileData: SECTION.NOT_LOGGED,
    EditProfileData: SECTION.EDIT_PROFILE
}


class State(BaseModel):
    section: SECTION
    data: Union[SearchForProfilesData, CreateProfileData, EditProfileData, BaseStateData]

    @root_validator(pre=True)
    def set_section(cls, value: Dict):
        if value.get('section') is None:
            data_type = type(value['data'])
            section = DATA_TO_SECTION_MAPPING[data_type]
            return {"section": section, **value}
        return value

