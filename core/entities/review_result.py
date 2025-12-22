from dataclasses import dataclass
import datetime


@dataclass
class ReviewResult:
    chunk_id: int
    user_id: int
    is_correct: bool
    reviewed_at: datetime