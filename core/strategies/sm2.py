from datetime import datetime, timedelta, timezone
from core.entities.review_state import ReviewState

DEFAULT_EF = 2.5
MIN_EF = 1.3

def sm2_calculate(
    state: ReviewState,
    quality: int
) -> ReviewState:
    ef = state.ease_factor or DEFAULT_EF

    # update ease factor
    ef = ef + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    if ef < MIN_EF:
        ef = MIN_EF

    if quality < 3:
        recall_streak = 0
        interval_days = 1
    else:
        recall_streak = state.recall_streak + 1

        if recall_streak == 1:
            interval_days = 1
        elif recall_streak == 2:
            interval_days = 6
        else:
            interval_days = round(state.interval_days * ef)

    next_review = datetime.now(timezone.utc) + timedelta(days=interval_days)

    return ReviewState(
        recall_streak=recall_streak,
        interval_days=interval_days,
        ease_factor=ef,
        next_review_at=next_review
    )
