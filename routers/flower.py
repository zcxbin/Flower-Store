from fastapi import APIRouter, Path, status

from dependency import db_dependency
import crud
from schemas import FlowerRequest

router = APIRouter()


@router.get("/read_flower", status_code=status.HTTP_200_OK)
async def read_flower(db: db_dependency):
    return crud.get_flowers(db)


@router.get("/{flower_id}", status_code=status.HTTP_200_OK)
async def read_flower(db: db_dependency, flower_id: int = Path(gt=0)):
    return crud.get_flower_by_id(db, flower_id)


@router.post("/create_flower", status_code=status.HTTP_201_CREATED)
async def create_flower(db: db_dependency, flower_request: FlowerRequest):
    return crud.create_flower(db, flower_request)


@router.put("/{flower_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_flower(db: db_dependency, flower_request: FlowerRequest, flower_id: int = Path(gt=0)):
    return crud.update_flower(db, flower_id, flower_request)


@router.delete("/{flower_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_flower(db: db_dependency, flower_id: int = Path(gt=0)):
    crud.delete_flower(db, flower_id)
