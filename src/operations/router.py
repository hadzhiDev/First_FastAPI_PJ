import time

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_async_session
from src.operations.models import operation
from src.operations.schemas import OperationCreate

router = APIRouter(
    prefix='/operations',
    tags=['Operation']
)


@router.get('/long-operation')
@cache(expire=30)
def get_long_op():
    time.sleep(2)
    return "too much data, which is calculated 100 years"


@router.get('/')
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        operations = result.fetchall()
        return {
            'status': 'success',
            'data': [
                dict(zip(operation.columns.keys(), row))
                for row in operations
            ],
            'details': None
        }
    except Exception:
        raise HTTPException(status_code=500, detail={
            'status': 'error',
            'data': None,
            'details': None
        })


@router.post('/')
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {'status': 'success'}
