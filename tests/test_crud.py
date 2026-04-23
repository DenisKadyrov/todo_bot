import pytest

from crud import task_crud, user_crud
from schemas import CreateTask, CreateUser


@pytest.mark.asyncio
async def test_create_and_list_user_tasks(session):
    user = await user_crud.create(
        db=session,
        obj_in=CreateUser(id=1001, chat_id="1001", username=None),
    )
    await task_crud.create(
        db=session,
        obj_in=CreateTask(user_id=user.id, title="Buy milk"),
    )
    await task_crud.create(
        db=session,
        obj_in=CreateTask(user_id=user.id, title="Read docs"),
    )

    tasks = await task_crud.get_multi(db=session, user_id=user.id)

    assert [task.title for task in tasks] == ["Buy milk", "Read docs"]


@pytest.mark.asyncio
async def test_remove_deletes_only_current_user_task(session):
    first_user = await user_crud.create(
        db=session,
        obj_in=CreateUser(id=1001, chat_id="1001", username="first"),
    )
    second_user = await user_crud.create(
        db=session,
        obj_in=CreateUser(id=2002, chat_id="2002", username="second"),
    )
    second_user_task = await task_crud.create(
        db=session,
        obj_in=CreateTask(user_id=second_user.id, title="Private task"),
    )

    deleted_by_wrong_user = await task_crud.remove(
        db=session,
        id=second_user_task.id,
        user_id=first_user.id,
    )
    second_user_tasks = await task_crud.get_multi(db=session, user_id=second_user.id)

    assert deleted_by_wrong_user is False
    assert [task.title for task in second_user_tasks] == ["Private task"]

    deleted_by_owner = await task_crud.remove(
        db=session,
        id=second_user_task.id,
        user_id=second_user.id,
    )
    second_user_tasks = await task_crud.get_multi(db=session, user_id=second_user.id)

    assert deleted_by_owner is True
    assert second_user_tasks == []
