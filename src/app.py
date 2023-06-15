from fastapi import FastAPI
from src.routes.contactRoute import contactRouter
app = FastAPI()

app.include_router(contactRouter)