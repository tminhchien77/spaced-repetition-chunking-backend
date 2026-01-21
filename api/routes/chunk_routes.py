from fastapi import APIRouter, Depends
from infra.db.connection import get_connection
from core.repositories.chunk_repository import ChunkRepository
from core.services.chunk_service import ChunkService
from core.services.review_service import ReviewService
from pydantic import BaseModel, conint
from dependencies.auth import get_current_user_id

class ReviewRequest(BaseModel):
    quality: conint(ge=0, le=5)

router = APIRouter()
repo=ChunkRepository()
chunk_service = ChunkService(repo)
review_service = ReviewService(repo)

@router.get("/chunks")
def get_chunks(conn = Depends(get_connection)):
    # conn = get_connection()
    # try:
    #     # repo = ChunkRepository(conn)
    #     # service = ChunkService(repo)
    #     chunks = chunk_service.get_chunks_to_learn(conn, user_id=1)
    #     return [c.__dict__ for c in chunks]
    # finally:
    #     close_connection(conn)
    chunks = chunk_service.get_chunks_to_learn(conn, user_id=1)
    return [c.__dict__ for c in chunks]


@router.post("/chunks/{chunk_id}/review")
def review_chunk(
    chunk_id: int,
    req: ReviewRequest,
    user_id: int = Depends(get_current_user_id),
    conn = Depends(get_connection)
):
    # repo = ChunkRepository(conn)
    # service = ReviewService(repo)
    quality = req.quality
    state = review_service.review(
        conn,
        user_id=user_id,
        chunk_id=chunk_id,
        quality=quality
    )

    print(f"State: {state}")

    return {
        "next_review_at": state.next_review_at,
        "interval": state.interval_days
    }
