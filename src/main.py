from fastapi import FastAPI
from .data.session import lifespan

app = FastAPI(lifespan=lifespan, title="Talent Management API", version="0.1.0")


@app.get("/")
def root():
    return {"message": "Hello World"}
