from fastapi import APIRouter, Depends, status, HTTPException
# Сессия БД
from sqlalchemy.orm import Session
# Функция подключения к БД
from backend.db_depends import get_db
# Аннотации, Модели БД и Pydantic.
from typing import Annotated
from models import User
from schemas import CreateUser, UpdateUser
# Функции работы с записями.
from sqlalchemy import insert, select, update, delete
# Функция создания slug-строки
from slugify import slugify

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


@router.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="The user is not found")
    return user


@router.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)], createuser: CreateUser):
    db.execute(insert(User).values(username = createuser.username,
                                   firstname = createuser.firstname,
                                   lastname = createuser.lastname,
                                   age = createuser.age,
                                   slug = slugify(createuser.username))
                                                          )
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'}


@router.put("update")
async def update_user(db: Annotated[Session, Depends(get_db)], user_id: int, updateuser: UpdateUser):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="The user is not found")
    db.execute(update(User).where(User.id == user_id).values(
                                username=updateuser.username,
                                firstname=updateuser.firstname,
                                lastname=updateuser.lastname,
                                age=updateuser.age,
                                slug=slugify(updateuser.username)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'update': 'User update is successful'}



@router.delete("/delete")
async def delete_user(db:Annotated[Session, Depends(get_db)],user_id: int, task_id: int):
    user = db.scalar(select(User).where(User.id == user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="The user is not found")
    db.execute(delete(User).where(User.id == user_id and Task.id == task_id))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'update': 'User delete is successful'}


@router.get("/user_id/tasks")
async def tasks_by_user_id(db:Annotated[Session, Depends(get_db)],user_id: int):
    user_task = db.scalar(select(User).where(User.id == user_id, Task.is_active == True))
    if not user_task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="The user is not found")
    return user_task
