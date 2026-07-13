from fastapi import FastAPI
from .routers import categoria_router
from .routers import unidade_router

app = FastAPI()


app.include_router(categoria_router.router)
app.include_router(unidade_router.router)