import pytest

from keybroads.tasks import tasks as task_keyboard
from crud import task_crud, user_crud
from schemas import CreateTask, CreateUser


@pytest.mark.asyncio
async def test_tasks_keyboard_is_empty_when_user_has_no_tasks(session):
    await user_crud.create(
        db=session,
        obj_in=CreateUser(id=1001, chat_id="1001", username="tester"),
    )

    keyboard = await task_keyboard(session=session, user_id=1001)

    assert keyboard is None


@pytest.mark.asyncio
async def test_tasks_keyboard_contains_task_buttons(session):
    user = await user_crud.create(
        db=session,
        obj_in=CreateUser(id=1001, chat_id="1001", username="tester"),
    )
    task = await task_crud.create(
        db=session,
        obj_in=CreateTask(user_id=user.id, title="Buy milk"),
    )

    keyboard = await task_keyboard(session=session, user_id=user.id)

    assert keyboard is not None
    assert len(keyboard.inline_keyboard) == 1
    assert keyboard.inline_keyboard[0][0].text == "Buy milk"
    assert keyboard.inline_keyboard[0][0].callback_data == f"task_{task.id}"
