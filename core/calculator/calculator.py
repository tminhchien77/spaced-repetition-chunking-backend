from core.entities.review_state import ReviewState
from core.strategies.sm2 import sm2_calculate

def calculate_next_review(
    state: ReviewState,
    quality: int,
    strategy: str = "sm2"
) -> ReviewState:
    if strategy == "sm2":
        return sm2_calculate(state, quality)

    raise ValueError(f"Unknown strategy: {strategy}")
