import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import uploads, files, folders, quota
from app.utils.security import auth_dep
from app.utils.db import init_db

app = FastAPI(title="Drive Local API", version="0.1.0")

WEB_ORIGIN = os.getenv("WEB_ORIGIN","http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[WEB_ORIGIN],
    allow_credentials=True,
    allow_methods=["GET","POST","PUT","PATCH","DELETE"],
    allow_headers=["Authorization","Content-Type"]
)

@app.get("/healthz")
def healthz():
    return {"ok": True}

# Init DB on startup
@app.on_event("startup")
def startup():
    init_db()

# Protected routers
app.include_router(uploads.router, prefix="/uploads", dependencies=[auth_dep])
app.include_router(files.router, prefix="/files", dependencies=[auth_dep])
app.include_router(folders.router, prefix="/folders", dependencies=[auth_dep])
app.include_router(quota.router, prefix="/quota", dependencies=[auth_dep])
