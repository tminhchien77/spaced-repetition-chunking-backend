from sqlite3 import Connection
from core.entities.chunk import Chunk
from typing import List
from psycopg2.extensions import connection
from core.entities.review_state import ReviewState
from psycopg2.extras import RealDictCursor

class ChunkRepository:
    # def __init__(self, conn: connection) -> None:
    #     self.conn = conn

    def get_due_review_chunks(self, conn, user_id: int, limit: int = 50) -> List[Chunk]:
        sql = """
            SELECT *
            FROM
            (
                SELECT
                    app_user_chunk.chunk_id,
                    md_chunk.chunk,
                    md_chunk.frequency
                FROM
                    application.app_user_chunk
                    JOIN masterdata.md_chunk
                        ON md_chunk.chunk_id = app_user_chunk.chunk_id
                WHERE
                    app_user_chunk.user_id = %s
                    AND md_chunk.isdeleted = FALSE
                    AND app_user_chunk.next_review_at <= NOW()
                ORDER BY next_review_at
                LIMIT %s
            ) tmp
            ORDER BY RANDOM();
        """

        with conn.cursor() as cursor:
            cursor.execute(sql, (user_id, limit,))
            rows = cursor.fetchall()

        return [Chunk(*row) for row in rows]

    def get_unseen_chunks(self, conn, user_id: int, limit: int = 50) -> List[Chunk]:
        sql = """
            SELECT *
            FROM
            (
                SELECT
                    md_chunk.chunk_id,
                    md_chunk.chunk,
                    md_chunk.frequency
                FROM
                    masterdata.md_chunk
                    LEFT JOIN application.app_user_chunk
                        ON app_user_chunk.chunk_id = md_chunk.chunk_id
                        AND app_user_chunk.user_id = %s
                WHERE
                    md_chunk.isdeleted = FALSE
                    AND app_user_chunk.user_chunk_id IS NULL
                ORDER BY md_chunk.frequency DESC
                LIMIT %s
            ) tmp
            ORDER BY RANDOM()
        """

        with conn.cursor() as cursor:
            cursor.execute(sql, (user_id, limit,))
            rows = cursor.fetchall()

        return [Chunk(*row) for row in rows]

    def get_review_state(self, conn: Connection, user_id: int, chunk_id: int):
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
            SELECT recall_streak, interval_days, ease_factor
            FROM application.app_user_chunk
            WHERE user_id = %s AND chunk_id = %s
        """, (user_id, chunk_id))
            return cur.fetchone()

    def upsert_review_state(self, conn: Connection, user_id: int, chunk_id: int, state: ReviewState):
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO application.app_user_chunk
            (
                user_id,
                chunk_id,
                interval_days,
                recall_streak,
                last_reviewed_at,
                next_review_at
            )
            VALUES
            (
                %s,
                %s,
                %s,
                %s,
                now(),
                %s
            )
            ON CONFLICT (user_id, chunk_id) DO UPDATE SET
                recall_streak = EXCLUDED.recall_streak,
                interval_days = EXCLUDED.interval_days,
                last_reviewed_at = now(),
                next_review_at = EXCLUDED.next_review_at,
                updated_at = now()
            """, (user_id, chunk_id, state.interval_days, state.recall_streak, state.next_review_at))