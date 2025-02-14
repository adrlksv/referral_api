from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.users.router import router as user_router
from src.auth.oauth.router import router as oauth_router


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешает запросы отовсюду (можно ограничить)
    allow_credentials=True,
    allow_methods=["*"],  # Разрешает все методы (GET, POST и т. д.)
    allow_headers=["*"],  # Разрешает все заголовки
)

app.include_router(user_router)
app.include_router(oauth_router)
