from fastapi import FastAPI
from .database import Base, engine
from .models import User, Post
from . import routes



app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(routes.route)
