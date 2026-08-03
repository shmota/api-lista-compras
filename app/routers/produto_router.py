from fastapi import Depends
from fastapi import APIRouter

from ..core.database import get_db
from ..schemas.produto_schema import (
    ProdutoCreate,
    ProdutoFiltros,
    ProdutoResponse,
    ProdutoUpdate,
)
from ..services.produto_service import ProdutoService

router = APIRouter(
    prefix="/produto",
    tags=["produto"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=ProdutoResponse)
async def criar_produto(produto: ProdutoCreate):
    with get_db() as db:
        service = ProdutoService(db)
        return service.criar(produto)


@router.get("/", response_model=list[ProdutoResponse])
async def listar_produto(filtros: ProdutoFiltros = Depends()):
    with get_db() as db:
        service = ProdutoService(db)
        return service.listar(filtros=filtros)


@router.get("/{id}", response_model=ProdutoResponse)
async def listar_produto_id(id: int):
    with get_db() as db:
        service = ProdutoService(db)
        return service.listar(id=id)


@router.put("/{id}", response_model=ProdutoResponse)
async def alterar_produto(id: int, produto: ProdutoUpdate):
    with get_db() as db:
        service = ProdutoService(db)
        service.alterar(id, produto)
        return service.listar(id=id)


@router.delete("/{id}", status_code=204)
async def deletar_produto(id: int):
    with get_db() as db:
        service = ProdutoService(db)
        service.deletar(id)

