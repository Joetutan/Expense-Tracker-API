from datetime import datetime, timedelta, timezone

from app.schema.expense_schema import ExpenseFilter, TimeLine


def get_date_range(datefilter: ExpenseFilter)-> tuple[datetime, datetime]:

    now = datetime.now(timezone.utc)

    match datefilter:
        case TimeLine.WEEK:
            return (now - timedelta(days=7), now)
        case TimeLine.MONTH:
            return (now - timedelta(days=30), now)
        case TimeLine.THREE_MONTHS:
            return (now - timedelta(days=90), now)
        