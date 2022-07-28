from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .db.base import async_engine, Base
from .routers.user import auth_user_router

app = FastAPI()

# origins = [
#     "http://localhost",
#     "https://localhost",
#     "http://localhost:8000",
#     "https://localhost:8000",
#     "http://localhost:8080",
#     "https://localhost:8080",
#     "http://172.17.255.125:8080",
#     "https://172.17.255.125:8080",
# ]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(auth_user_router)
@app.get('/')
async def root():
    return {'message': 'success'}
