from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas.categoria_schema import CategoriaCreate, CategoriaResponse, CategoriaUpdate
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
async def listar_categoria(db: Session = Depends(get_db), nome: str = None):
    service = CategoriaService(db)
    
    if nome:
        return service.listar(nome).all()
    
    else:
        return service.listar().all()
    
@router.get("/{id}", response_model=CategoriaResponse)
async def listar_categoria_id(id: int, db: Session = Depends(get_db)):
    service = CategoriaService(db)
    return service.listar(id).first()

@router.put("/{id}", response_model=CategoriaResponse)
async def alterar_categoria(categoria: CategoriaUpdate, id: int, db: Session = Depends(get_db)):
    service = CategoriaService(db)
    return service.alterar(id, categoria)

@router.delete("/{id}", status_code=204)
async def deletar_categoria(id: int, db: Session = Depends(get_db)):
    service = CategoriaService(db)
    service.deletar(id)