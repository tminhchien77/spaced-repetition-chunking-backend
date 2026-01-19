from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.chunk_routes import router
from infra.db.init_db import init_db
app = FastAPI()
app.include_router(router)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.on_event("startup")
def startup():
    init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://spaced-repetition-chunking.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)