import datetime
import math
import time
from random import randint


def human_time(*args, **kwargs):
    secs = float(datetime.timedelta(*args, **kwargs).total_seconds())
    units = [("day", 86400), ("hour", 3600), ("minute", 60), ("second", 1)]
    parts = []
    for unit, mul in units:
        if secs / mul >= 1 or mul == 1:
            if mul > 1:
                n = int(math.floor(secs / mul))
                secs -= n * mul
            else:
                n = secs if secs != int(secs) else int(secs)
            parts.append("%s %s%s" % (n, unit, "" if n == 1 else "s"))
    return ", ".join(parts)


def random_interval():
    """
    Get me a time delta between 4 hours and 12 hours.
    :return: int
    """
    rand_value = randint(14400, 43200)
    delta = (time.time() + rand_value) - time.time()
    return int(delta)