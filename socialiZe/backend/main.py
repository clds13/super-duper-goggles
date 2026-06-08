import os

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import api, ws
# from routers import api

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="socialiZe", version="0.1.0", summary="A user-friendly suite of tools to study the social behaviour of zebrafish.")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create the directories if they don't exist
os.makedirs("uploads", exist_ok=True)
os.makedirs("trajectories", exist_ok=True)

app.include_router(api.router, prefix="/api")
app.include_router(ws.router, prefix="/ws")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.mount("/trajectories", StaticFiles(directory="trajectories"), name="trajectories")
