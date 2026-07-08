from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas.categoria_schema import (CategoriaCreate, CategoriaResponse)
from ..services.categoria_service import CategoriaService
from ..core.database import get_db

router = APIRouter(
    prefix="/categoria",
    tags=["categoria"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=CategoriaResponse)
async def criar_categoria(categoria: CategoriaCreate, db: Session = Depends(get_db)):
    service = CategoriaService(db)
    return service.criar(categoria)

@router.get("/", response_model=list[CategoriaResponse])
async def listar_categorias(db: Session = Depends(get_db), nome: str = None):
    service = CategoriaService(db)
    
    if nome:
        return service.buscar_por_nome(nome.upper())
    
    return service.listar()

