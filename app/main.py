from fastapi import FastAPI
from .routers import categoria_router

app = FastAPI()


app.include_router(categoria_router.router)