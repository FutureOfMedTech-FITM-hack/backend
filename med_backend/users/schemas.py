from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, EmailStr, root_validator


class ExtendedUser(BaseModel):
    id: int
    fullname: str
    gender: str
    born: date

    @root_validator(pre=False)
    def _set_fields(cls, values):
        """This is a validator that sets the field values based on the
        the user's account type.

        Args:
            values (dict): Stores the attributes of the User object.

        Returns:
            dict: The attributes of the user object with the user's fields.
        """
        values["key"] = values["id"]
        values["fio"] = values["fullname"]
        values["age"] = relativedelta(datetime.now(), values["born"]).years

        values.pop("id")
        values.pop("fullname")
        values.pop("born")
        return values


class ListUser(ExtendedUser):
    latest_form_result: str

    class Config:
        orm_mode = True


class FullUser(ListUser):
    email: EmailStr

    class Config:
        orm_mode = True
