from core.entities.review_state import ReviewState
from core.calculator.calculator import calculate_next_review
from core.repositories.chunk_repository import ChunkRepository

class ReviewService:
    def __init__(self, repo: ChunkRepository, strategy="sm2"):
        self.repo = repo
        self.strategy = strategy

    def review(
        self,
        conn,
        user_id: int,
        chunk_id: int,
        quality: int
    ) -> ReviewState:

        db_state = self.repo.get_review_state(
            conn, user_id, chunk_id
        )

        if db_state:
            state = ReviewState(
                recall_streak=db_state["recall_streak"],
                interval_days=db_state["interval_days"],
                ease_factor=db_state["ease_factor"]
            )
        else:
            state = ReviewState(
                recall_streak=0,
                interval_days=1,
                ease_factor=2.5
            )

        new_state = calculate_next_review(
            state=state,
            quality=quality,
            strategy=self.strategy
        )

        self.repo.upsert_review_state(
            conn, user_id, chunk_id, new_state
        )

        return new_state
