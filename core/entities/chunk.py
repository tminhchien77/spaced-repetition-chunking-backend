from dataclasses import dataclass
from datetime import datetime, timezone


@dataclass
class Chunk:
    chunk_id: int
    chunk: str
    frequency: int
    keyword: str
    syntagmid: int
    syntagm_name: str
    target_part_of_speech: str
    next_review_at: datetime | None = None

    @property
    def is_overdue(self) -> bool:
        if not self.next_review_at:
            return False
        return self.next_review_at <= datetime.now(timezone.utc)