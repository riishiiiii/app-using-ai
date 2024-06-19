from fastapi import FastAPI
import json
from fastapi import HTTPException

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from blog import router as blog_router
from users import router as users_router

app.include_router(blog_router, prefix="/blog")
app.include_router(users_router, prefix="/users")


