from fastapi import APIRouter

routerT = APIRouter(prefix="/task",tags=["task"])

@routerT.get("/")
async def all_tasks():
    pass

@routerT.get("/task_id'")
async def task_by_id():
    pass

@routerT.post("/create")
async def create_task():
    pass

@routerT.put("update")
async def update_task():
    pass

@routerT.delete("/delete")
async def delete_task():
    pass

@routerT.delete("/cross")
async def delete_task():
    pass
