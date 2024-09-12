from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

from src.auth.base_config import auth_backend, fastapi_users
from src.auth.models import User
from src.auth.manager import get_user_manager
from src.auth.schemas import UserRead, UserCreate
from src.operations.router import router as router_operation
from src.tasks.router import router as router_tasks

app = FastAPI(
    title="Trading App"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_operation)
app.include_router(router_tasks)


# Startup event for Redis connection
@app.on_event("startup")
async def startup_event():
    try:
        redis = aioredis.from_url("redis://localhost", encoding="utf8", decode_responses=True)
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    except Exception as e:
        print(f"Failed to connect to Redis: {e}")

# Uncomment this block if you want to protect routes using JWT cookies
# current_user = fastapi_users.current_user()

# @app.get('/protected-route')
# def protected_route(user: User = Depends(current_user)):
#     return f'Hello {user.username}'

# Example of using common parameters for routes
# @app.get("/items/")
# async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
#     return commons

# @app.get("/users/")
# async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
#     return commons
