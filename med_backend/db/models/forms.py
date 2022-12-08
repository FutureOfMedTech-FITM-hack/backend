from typing import List

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from med_backend.db.base import Base
from med_backend.db.models.users import UserScheme


class FormScheme(Base):
    __tablename__ = "forms"

    id: int = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        index=True,
    )
    name: str = Column(String, nullable=False)

    # user
    user_id: int = Column(Integer, ForeignKey(UserScheme.id), primary_key=True)
    user: UserScheme = relationship("UserScheme", foreign_keys="FormScheme.user_id")

    questions: List["FormQuestion"] = relationship(
        "FormQuestion",
        back_populates="form",
    )


class FormQuestion(Base):
    __tablename__ = "form_questions"

    id: int = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        index=True,
    )

    # form
    form_id: int = Column(Integer, ForeignKey(FormScheme.id), primary_key=True)
    form: FormScheme = relationship("FormScheme", foreign_keys="FormQuestion.form_id")

    type: str = Column(String, default="number")
    question: str = Column(String, nullable=False)
    ref_min: int = Column(Integer, nullable=True)
    ref_max: int = Column(Integer, nullable=True)


class FormAssignment(Base):
    __tablename__ = "form_assignment"
    id: int = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        index=True,
    )

    form_id: int = Column(Integer, ForeignKey(FormScheme.id), primary_key=True)
    form: FormScheme = relationship("FormScheme", foreign_keys="FormAssignment.form_id")

    user_id: int = Column(Integer, ForeignKey(UserScheme.id), primary_key=True)
    user: UserScheme = relationship("UserScheme", foreign_keys="FormAssignment.user_id")


class UserRevQuestion(Base):
    __tablename__ = "user_form_rev_question"
    id: int = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        index=True,
    )

    # question
    question_id: int = Column(Integer, ForeignKey(FormQuestion.id), primary_key=True)
    question: FormQuestion = relationship(
        "FormQuestion",
        foreign_keys="UserRevQuestion.question_id",
    )

    # user
    user_id: int = Column(Integer, ForeignKey(UserScheme.id), primary_key=True)
    user: UserScheme = relationship(
        "UserScheme",
        foreign_keys="UserRevQuestion.user_id",
    )

    ref_min: int = Column(Integer, nullable=False)
    ref_max: int = Column(Integer, nullable=False)


class UserFormSubmission(Base):
    __tablename__ = "user_form_submission"
    id: int = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        index=True,
    )

    # form
    form_id: int = Column(Integer, ForeignKey(FormScheme.id), primary_key=True)
    form: FormScheme = relationship(
        "FormScheme",
        foreign_keys="UserFormSubmission.form_id",
    )

    # user
    user_id: int = Column(Integer, ForeignKey(UserScheme.id), primary_key=True)
    user: UserScheme = relationship(
        "UserScheme",
        foreign_keys="UserFormSubmission.user_id",
    )

    answers: List["UserFormFieldSubmission"] = relationship(
        "UserFormFieldSubmission",
        back_populates="submission",
    )


class UserFormFieldSubmission(Base):
    __tablename__ = "user_form_field_submission"
    id: int = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
        index=True,
    )

    # submission
    submission_id: int = Column(
        Integer,
        ForeignKey(UserFormSubmission.id),
        primary_key=True,
    )
    submission: UserFormSubmission = relationship(
        "UserFormSubmission",
        foreign_keys="UserFormFieldSubmission.submission_id",
    )
