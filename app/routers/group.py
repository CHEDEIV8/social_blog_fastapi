from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import crud, database, oauth2, schemas, utils

router = APIRouter(prefix='/groups', tags=['Group'])


@router.get('/', response_model=list[schemas.Group])
def read_groups(db: Session = Depends(database.get_db)):
    return crud.get_groups(db)


@router.get('/{group_id}', response_model=schemas.Group)
def read_group(group_id: int, db: Session = Depends(database.get_db)):
    group = crud.get_group(db, group_id)
    if not group:
        utils.raise_not_found('Группа не найдена')
    return group
