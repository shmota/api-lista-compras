from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..services.unidade_service import UnidadeService
from ..schemas.unidade_schema import UnidadeCreate, UnidadeResponse, UnidadeUpdate
from ..core.database import get_db

router = APIRouter(
    prefix="/unidade",
    tags=["unidade"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=UnidadeResponse)
async def criar_unidade(unidade: UnidadeCreate, db: Session = Depends(get_db)):
    service = UnidadeService(db)
    return service.criar(unidade)


@router.get("/", response_model=list[UnidadeResponse])
async def listar_unidade(search: str = None ,db: Session = Depends(get_db)):
    service = UnidadeService(db)
    return service.listar(search)


@router.get("/{id}", response_model=UnidadeResponse)
async def listar_unidade(id: int, db: Session = Depends(get_db)):
    service = UnidadeService(db)
    return service.listar_id(id)

@router.put("/{id}", response_model=UnidadeResponse)
async def alterar_unidade(id: int, unidade: UnidadeUpdate, db: Session = Depends(get_db)):
    service = UnidadeService(db)
    return service.alterar(id, unidade)

@router.delete("/{id}", status_code=204)
async def deletar_unidade(id: int, db: Session = Depends(get_db)):
    service = UnidadeService(db)
    service.deletar(id)