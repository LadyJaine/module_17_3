from fastapi import FastAPI
from routers import task, user

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True})


@app.get("/")
async def welcome():
    return {"message":"My shop"}

app.include_router(user.router)
app.include_router(task.router)


