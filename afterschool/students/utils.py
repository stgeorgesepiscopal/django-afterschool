from datetime import datetime
from django.utils import timezone


def ceil_dt(dt, delta):
    """
    Rounds a time up to the nearest [delta]
    :param dt: datetime.datetime object
    :param delta: datetime.timedelta object
    :return:
    """
    if timezone.is_naive(dt):
        return dt + (datetime.min - dt) % delta
    else:
        return dt + (datetime.min - timezone.make_naive(dt)) % delta


def floor_dt(dt, delta):
    """
    Rounds down to the nearest [delta]
    :param dt: datetime.datetime object
    :param delta: datetime.timedelta object
    :return:
    """
    return ceil_dt(dt, delta) - delta
