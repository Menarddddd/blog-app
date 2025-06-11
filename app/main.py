from fastapi import FastAPI
from .database import Base, engine
from .models import User, Post



app = FastAPI()

Base.metadata.create_all(bind=engine)

