from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import order,user,auth,webhook_driver_register,app_auth,app_order,app_order_driver,app_order_v2


app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



app.include_router(order.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(app_order.router)


#
app.include_router(webhook_driver_register.router)

# Mobile api
app.include_router(app_auth.router)
app.include_router(app_order_driver.router)
app.include_router(app_order_v2.router)



models.Base.metadata.create_all(bind=engine)






@app.get("/")
async def root():
    return{"message":"Hello world"}



# How to run fastapi on public ip?
# uvicorn main:app --host 0.0.0.0 --port 8000