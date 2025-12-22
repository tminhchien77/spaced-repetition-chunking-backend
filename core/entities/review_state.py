from dataclasses import dataclass
from datetime import datetime


@dataclass
class ReviewState:
    recall_streak: int
    interval_days: int
    ease_factor: float
    next_review_at: datetime | None = None