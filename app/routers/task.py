from fastapi import APIRouter, Depends, status, HTTPException
# # Сессия БД
# from sqlalchemy.orm import Session
# # Функция подключения к БД
# from app.backend.db_depends import get_db
# # Аннотации, Модели БД и Pydantic.
# from typing import Annotated
# from app.models import User,Task
# from app.schemas import CreateTask, UpdateTask
# # Функции работы с записями.
# from sqlalchemy import insert, select, update, delete
# # Функция создания slug-строки
# from slugify import slugify

router = APIRouter(prefix="/task",tags=["task"])

@router.get("/")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks

@router.get("/task_id'")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="The task is not found")
    return task


@router.post("/create")
async def create_task(db: Annotated[Session, Depends(get_db)], user_id: int, createtask: CreateTask):
    db.execute(insert(Task).values(tasktitle = createtask.title,
                                   userid = user_id,
                                   taskcontent = createtask.content,
                                   taskpriority = createtask.priority,
                                   taskcompleted = createtask.completed,
                                   slug = slugify(createtask.tasktitle))
                                                          )
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'}


@router.put("/update")
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, updatetask: UpdateTask):
    user = db.scalar(select(Task).where(Task.id == task_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="The task is not found")
    db.execute(update(Task).where(Task.id == task_id).values(
                                        tasktitle=updatetask.title,
                                        taskcontent=updatetask.content,
                                        taskpriority=updatetask.priority,
                                        taskcompleted=updatetask.completed,
                                        slug=slugify(updatetask.tasktitle)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'update': 'Task update is successful'}


@router.delete("/delete")
async def delete_task(db:Annotated[Session, Depends(get_db)],task_id: int):
    user = db.scalar(select(Task).where(Task.id == task_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="The task is not found")
    db.execute(delete(Task).where(Task.id == task_id))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'update': 'Task delete is successful'}

