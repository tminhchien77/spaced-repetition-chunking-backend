from core.repositories.chunk_repository import ChunkRepository
import random

class ChunkService:
    def __init__(self, repo: ChunkRepository) -> None:
        self.repo = repo

    def weighted_shuffle(self, chunks):
        overdue = [c for c in chunks if c.is_overdue]
        normal = [c for c in chunks if not c.is_overdue]

        random.shuffle(overdue)
        random.shuffle(normal)

        return overdue + normal

    def get_chunks_to_learn(self, conn, user_id: int, limit: int = 50):
        review_chunks = self.repo.get_due_review_chunks(conn, user_id, limit)

        remaining = limit - len(review_chunks)

        if remaining > 0:
            unseen_chunks = self.repo.get_unseen_chunks(conn, user_id, remaining)
        else:
            unseen_chunks = []

        chunks = review_chunks + unseen_chunks

        self.weighted_shuffle(chunks)

        return chunks

