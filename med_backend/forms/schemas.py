from typing import List

from pydantic import BaseModel

from med_backend.auth.schemas import UserPublicInfo


class Question(BaseModel):
    id: int
    type: str
    question: str


class BaseFormField(BaseModel):
    type: str
    question: str
    ref_min: int | None
    ref_max: int | None


class CreateFormField(BaseFormField):
    ...


class FormField(BaseFormField):
    id: int

    class Config:
        orm_mode = True


class QuestionRef(BaseModel):
    id: int
    ref_min: int | None
    ref_max: int | None


class FormAssigment(BaseModel):
    user_id: int
    question_refs: List[QuestionRef]


class BaseForm(BaseModel):
    name: str


class FormCreate(BaseForm):
    user_id: int


class ListForm(BaseForm):
    id: int

    class Config:
        orm_mode = True


class Form(BaseForm):
    id: int
    user: UserPublicInfo
    questions: List[Question]

    class Config:
        orm_mode = True
