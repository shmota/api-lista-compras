from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated

from ..services.produto_service import ProdutoService
from ..schemas.produto_schema import ProdutoCreate, ProdutoResponse, ProdutoFiltros
from ..core.database import get_db

router = APIRouter(
    prefix="/produto",
    tags=["produto"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=ProdutoResponse)
async def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    service = ProdutoService(db)
    return service.criar(produto)


@router.get("/", response_model=list[ProdutoResponse])
async def listar_produto(
    db: Session = Depends(get_db),
    filtros: ProdutoFiltros = Depends(),
):
    service = ProdutoService(db)
    
    return service.listar(filtros)
