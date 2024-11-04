from fastapi import APIRouter

routerUser = APIRouter(prefix="/user",tags=["user"])

@routerUser.get("/")
async def all_users():
    pass

@routerUser.get("/user_id'")
async def user_by_id():
    pass

@routerUser.post("/create")
async def create_user():
    pass

@routerUser.put("update")
async def update_user():
    pass

@routerUser.delete("/delete")
async def delete_user():
    pass
