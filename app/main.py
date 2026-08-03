from fastapi import FastAPI

from .routers import (
    categoria_router,
    compra_router,
    item_compra_router,
    produto_router,
    unidade_router,
)

app = FastAPI()


app.include_router(categoria_router.router)
app.include_router(unidade_router.router)
app.include_router(produto_router.router)
app.include_router(compra_router.router)
app.include_router(item_compra_router.router)

