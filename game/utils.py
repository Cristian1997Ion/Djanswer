import datetime
from django.utils.timezone import utc


def get_remaining_time(date):
    """Returns how many seconds are left until the given date is reached."""
    print(date)
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    timediff = date - now
    remaining_seconds = int(timediff.total_seconds())
    return remaining_seconds if remaining_seconds > 0 else 0