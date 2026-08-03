from fastapi import Depends
from fastapi import APIRouter

from ..core.database import get_db
from ..schemas.compra_schema import (
    CompraCreate,
    CompraFiltros,
    CompraResponse,
    CompraUpdate,
)
from ..services.compra_service import CompraService

router = APIRouter(
    prefix="/compra",
    tags=["compra"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=CompraResponse)
async def criar_compra(compra: CompraCreate):
    with get_db() as db:
        service = CompraService(db)
        return CompraResponse.model_validate(service.criar(compra))


@router.get("/", response_model=list[CompraResponse])
async def listar_compra(filtros: CompraFiltros = Depends()):
    with get_db() as db:
        service = CompraService(db)
        return service.listar(filtros=filtros)


@router.get("/{id}", response_model=CompraResponse)
async def listar_compra_id(id: int):
    with get_db() as db:
        service = CompraService(db)
        return CompraResponse.model_validate(service.listar_id(id))


@router.put("/{id}", response_model=CompraResponse)
async def alterar_compra(id: int, compra: CompraUpdate):
    with get_db() as db:
        service = CompraService(db)
        return CompraResponse.model_validate(service.alterar(id, compra))


@router.delete("/{id}", status_code=204)
async def deletar_compra(id: int):
    with get_db() as db:
        service = CompraService(db)
        service.deletar(id)
