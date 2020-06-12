import datetime
import math
import time
import uuid
import humanize
from random import randint


def split_list(input_list, n):
    """
    Takes a list and splits it into smaller lists of n elements each.
    :param input_list:
    :param n:
    :return:
    """
    n = max(1, n)
    return [input_list[i:i + n] for i in range(0, len(input_list), n)]


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

def subtract_time(start, end):
    subtracted = humanize.naturaltime(start - end)
    return str(subtracted)

def random_interval():
    """
    Get me a time delta between 4 hours and 12 hours.
    :return: int
    """
    rand_value = randint(14400, 43200)
    delta = (time.time() + rand_value) - time.time()
    return int(delta)


def get_random_hex(chars=4):
    """ Generate random hex. limited to chars provided.
        If chars not provided then limit to 4
    """
    my_hex = uuid.uuid4().hex[:chars]
    return my_hex
