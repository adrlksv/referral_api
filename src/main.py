from redis import asyncio as aioredis

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache import FastAPICache

from src.users.router import router as user_router
from src.auth.oauth.router import router as oauth_router
from src.referral.router import router as referral_router
from src.config import settings

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    await redis.close()


app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(oauth_router)
app.include_router(referral_router)
