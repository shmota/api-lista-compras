from fastapi import APIRouter

from ..core.database import get_db
from ..schemas.item_compra_schema import (
    ItemCompraCreate,
    ItemCompraResponse,
    ItemCompraUpdate,
)
from ..services.item_compra_service import ItemCompraService

router = APIRouter(
    prefix="/item-compra",
    tags=["item-compra"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=ItemCompraResponse)
async def criar_item_compra(item: ItemCompraCreate):
    with get_db() as db:
        service = ItemCompraService(db)
        return service.criar(item)


@router.get("/", response_model=list[ItemCompraResponse])
async def listar_item_compra(compra_id: int = None):
    with get_db() as db:
        service = ItemCompraService(db)
        return service.listar(compra_id=compra_id)


@router.get("/{id}", response_model=ItemCompraResponse)
async def listar_item_compra_id(id: int):
    with get_db() as db:
        service = ItemCompraService(db)
        return service.listar_id(id)


@router.put("/{id}", response_model=ItemCompraResponse)
async def alterar_item_compra(id: int, item: ItemCompraUpdate):
    with get_db() as db:
        service = ItemCompraService(db)
        return service.alterar(id, item)


@router.delete("/{id}", status_code=204)
async def deletar_item_compra(id: int):
    with get_db() as db:
        service = ItemCompraService(db)
        service.deletar(id)
