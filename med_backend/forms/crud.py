from typing import List

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from med_backend.db.models.forms import (
    FormAssignment,
    FormQuestion,
    FormScheme,
    UserFormFieldSubmission,
    UserFormSubmission,
    UserRevQuestion,
)
from med_backend.forms.schemas import (
    BaseForm,
    CreateFormField,
    FullAnswer,
    FullSubmission,
)
from med_backend.users.crud import get_user


async def get_forms(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 100,
) -> List[FormScheme] | None:
    r = await session.execute(
        select(FormScheme).offset(skip).limit(limit),
    )
    forms = r.scalars().all()
    return forms


async def get_form(session: AsyncSession, form_id: int) -> FormScheme | None:
    r = await session.execute(select(FormScheme).where(FormScheme.id == form_id))
    form = r.scalars().first()
    return form


async def filter_form_assigment(
    session: AsyncSession,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
) -> List[FormScheme] | None:
    r = await session.execute(
        select(FormScheme)
        .outerjoin(FormAssignment)
        .where(FormAssignment.user_id == user_id)
        .offset(skip)
        .limit(limit),
    )
    forms = r.scalars().fetchall()
    return forms


async def get_questions(session: AsyncSession, form_id: int) -> List[FormQuestion]:
    r = await session.execute(
        select(FormQuestion).where(FormQuestion.form_id == form_id),
    )
    questions = r.scalars().all()
    return questions


async def create_form(
    session: AsyncSession,
    form: BaseForm,
    user_id: int,
) -> FormScheme:
    user = await get_user(session, user_id)
    if not user or not user.is_manager:
        raise HTTPException(status_code=422, detail="User can't be used")

    db_form = FormScheme(name=form.name, user_id=user_id)
    session.add(db_form)
    await session.commit()
    await session.refresh(db_form)
    return db_form


async def create_form_field(
    session: AsyncSession,
    field: CreateFormField,
    user_id: int,
    form_id: int,
) -> FormQuestion:
    user = await get_user(session, user_id)
    if not user or not user.is_manager:
        raise HTTPException(status_code=422, detail="User can't be used")

    form = await get_form(session, form_id)
    if not form:
        raise HTTPException(status_code=422, detail="Form can't be used")

    if user.id != form.user_id:
        raise HTTPException(
            status_code=401,
            detail="You are not allowed to access this form",
        )

    obj = FormQuestion(
        form_id=form_id,
        type=field.type,
        question=field.question,
        ref_min=field.ref_min,
        ref_max=field.ref_max,
    )
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


async def create_form_assigment(session: AsyncSession, form_id: int, user_id: int):
    user = await get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=422, detail="User can't be used")

    form = await get_form(session, form_id)
    if not form:
        raise HTTPException(status_code=422, detail="Form can't be used")

    assigment = await session.execute(
        select(FormAssignment)
        .where(FormAssignment.form_id == form_id)
        .where(FormAssignment.user_id == user_id),
    )

    if assigment.scalars().first():
        return True

    obj = FormAssignment(form_id=form_id, user_id=user_id)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return True


async def create_user_form_rev_question(
    session: AsyncSession,
    field_id: int,
    user_id: int,
    ref_min: int,
    ref_max: int,
):
    r = await session.execute(select(FormQuestion).where(FormQuestion.id == field_id))
    field = r.scalars().first()
    if not field:
        raise HTTPException(status_code=422, detail="Such field doesn't exist")

    r = await session.execute(
        select(UserRevQuestion)
        .where(UserRevQuestion.user_id == user_id)
        .where(UserRevQuestion.question_id == field_id),
    )
    rev = r.scalars().first()
    if rev:
        await session.execute(
            update(UserRevQuestion)
            .where(UserRevQuestion.id == rev.id)
            .values(ref_max=ref_max, ref_min=ref_min),
        )
    else:
        rev = UserRevQuestion(
            question_id=field_id,
            user_id=user_id,
            ref_max=ref_max,
            ref_min=ref_min,
        )
        session.add(rev)
        await session.commit()
    await session.refresh(rev)
    return rev


async def create_submission(session: AsyncSession, form_id: int, user_id: int):
    user = await get_user(session, user_id)
    if not user:
        raise HTTPException(status_code=422, detail="User can't be used")

    form = await get_form(session, form_id)
    if not form:
        raise HTTPException(status_code=422, detail="Form can't be used")

    obj = UserFormSubmission(form_id=form_id, user_id=user_id)
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


async def create_submission_answer(
    session: AsyncSession,
    sumb_id: int,
    field_id: int,
    data: str,
):

    r = await session.execute(select(FormQuestion).where(FormQuestion.id == field_id))
    field = r.scalars().first()
    if not field:
        raise HTTPException(status_code=422, detail="Such field doesn't exist")

    obj = UserFormFieldSubmission(
        submission_id=sumb_id,
        question_id=field_id,
        answer=data,
    )
    session.add(obj)
    await session.commit()
    await session.refresh(obj)
    return obj


async def get_submissions(session: AsyncSession, form_id: int) -> List[FullSubmission]:
    r = await session.execute(
        select(UserFormSubmission)
        .options(selectinload(UserFormSubmission.answers))
        .options(selectinload(UserFormSubmission.user))
        .where(UserFormSubmission.form_id == form_id),
    )
    submissions = r.scalars().all()
    res: List[FullSubmission] = []
    for submission in submissions:
        answers: List[FullAnswer] = []
        for answer in submission.answers:
            r = await session.execute(
                select(UserRevQuestion)
                .where(UserRevQuestion.user_id == submission.user.id)
                .where(UserRevQuestion.question_id == answer.question_id),
            )
            obj = r.scalars().first()
            ref_min = None
            ref_max = None
            if obj:
                ref_min = obj.ref_min
                ref_max = obj.ref_max

            r = await session.execute(
                select(FormQuestion).where(FormQuestion.id == answer.question_id),
            )
            obj = r.scalars().first()
            answers.append(
                FullAnswer(
                    field_id=obj.id,
                    question=obj.question,
                    type=obj.type,
                    answer=answer.answer,
                    ref_min=ref_min if ref_min else obj.ref_min,
                    ref_max=ref_max if ref_max else obj.ref_max,
                ),
            )
        res.append(FullSubmission(fio=submission.user.fullname, answers=answers))
    return res
