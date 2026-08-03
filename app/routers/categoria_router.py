from fastapi import APIRouter

from ..core.database import get_db
from ..schemas.categoria_schema import (
    CategoriaCreate,
    CategoriaResponse,
    CategoriaUpdate,
)
from ..services.categoria_service import CategoriaService

router = APIRouter(
    prefix="/categoria",
    tags=["categoria"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=CategoriaResponse)
async def criar_categoria(categoria: CategoriaCreate):
    with get_db() as db:
        service = CategoriaService(db)
        return service.criar(categoria)


@router.get("/", response_model=list[CategoriaResponse])
async def listar_categoria(nome: str = None):
    with get_db() as db:
        service = CategoriaService(db)
        return service.listar(dado=nome)


@router.get("/{id}", response_model=CategoriaResponse)
async def listar_categoria_id(id: int):
    with get_db() as db:
        service = CategoriaService(db)
        return service.listar_id(id)


@router.put("/{id}", response_model=CategoriaResponse)
async def alterar_categoria(id: int, categoria: CategoriaUpdate):
    with get_db() as db:
        service = CategoriaService(db)
        return service.alterar(id, categoria)


@router.delete("/{id}", status_code=204)
async def deletar_categoria(id: int):
    with get_db() as db:
        service = CategoriaService(db)
        service.deletar(id)