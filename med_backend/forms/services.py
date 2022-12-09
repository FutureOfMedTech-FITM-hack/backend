from typing import List

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from med_backend.forms.crud import (
    create_form_assigment,
    create_submission,
    create_submission_answer,
    create_user_form_rev_question,
    get_form,
    get_questions,
    get_submissions,
)
from med_backend.forms.schemas import Form, FormAnswer, FormAssigment, Question


async def get_full_form(session: AsyncSession, form_id: int) -> Form:
    form = await get_form(session, form_id)
    if not form:
        raise HTTPException(status_code=404, detail="Form doesn't exist")
    questions = await get_questions(session, form_id)

    return Form(
        id=form_id,
        name=form.name,
        questions=[
            Question(id=q.id, type=q.type, question=q.question) for q in questions
        ],
    )


async def assign_form(session: AsyncSession, data: FormAssigment, form_id: int):
    form = await get_form(session, form_id)
    if not form:
        raise HTTPException(status_code=404, detail="Form doesn't exist")
    await create_form_assigment(session, form_id, data.user_id)
    for field in data.question_refs:
        await create_user_form_rev_question(
            session,
            field.id,
            data.user_id,
            field.ref_min,
            field.ref_max,
        )


async def submit_form(
    session: AsyncSession,
    data: List[FormAnswer],
    form_id: int,
    user_id: int,
):
    subm = await create_submission(session, form_id, user_id)
    for answer in data:
        await create_submission_answer(session, subm.id, answer.field_id, answer.answer)


async def get_form_submissions(session: AsyncSession, form_id: int):
    form = await get_form(session, form_id)
    if not form:
        raise HTTPException(status_code=404, detail="Form doesn't exist")
    submissions = await get_submissions(session, form_id)
    return submissions
