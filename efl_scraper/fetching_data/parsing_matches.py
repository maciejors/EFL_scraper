import locale
import datetime
from contextlib import contextmanager


@contextmanager
def _polish_locale():
    """Temporarily set the polish locale"""
    original_locale = locale.setlocale(locale.LC_ALL)
    locale.setlocale(locale.LC_ALL, 'pl_PL.UTF-8')
    try:
        yield
    finally:
        locale.setlocale(locale.LC_ALL, original_locale)


def _get_start_date_from_raw(start_date_raw: str) -> datetime.date:
    start_date_raw = start_date_raw.strip().lower()
    # scenario 1: temporal adverb or live
    today: datetime.date = datetime.date.today()
    timedeltas = {
        'przedwczoraj': -2,
        'wczoraj': -1,
        'dziś': 0,
        'live': 0,
        'jutro': 1,
    }
    if start_date_raw in timedeltas.keys():
        return today + datetime.timedelta(days=timedeltas[start_date_raw])

    # scenario 2: weekday's name as start date
    weekday_name_to_number = {
        'poniedziałek': 0,
        'wtorek': 1,
        'środa': 2,
        'czwartek': 3,
        'piątek': 4,
        'sobota': 5,
        'niedziela': 6,
    }
    if start_date_raw in weekday_name_to_number.keys():
        weekday_no = weekday_name_to_number[start_date_raw]
        # https://stackoverflow.com/questions/8801084/how-to-calculate-next-friday
        days_until_weekday = (weekday_no - today.weekday()) % 7
        # in this scenario it can't be today so if the weekday is the same
        # it means the game is on the same day next week
        if days_until_weekday == 0:
            days_until_weekday = 7
        return today + datetime.timedelta(days=days_until_weekday)

    # scenario 3: polish date like "23 SIE"
    with _polish_locale():
        # for now match date does not have a proper year set
        match_date = datetime.datetime.strptime(start_date_raw, "%d %b").date()
    # set an appropriate year knowing there are not going to be any dates in the past
    if match_date.month >= today.month:
        match_date = match_date.replace(year=today.year)
    else:
        # the reasoning here: we can have November now and the date is in January
        match_date = match_date.replace(year=today.year + 1)
    return match_date


def get_match_data_from_raw(
        competition: str,
        match_title_raw: str,
        start_time_raw: str,
        start_date_raw: str
) -> dict:
    home_team, away_team = tuple(match_title_raw.split(' - '))
    start_date = _get_start_date_from_raw(start_date_raw)
    start_hour_str, start_minute_str = tuple(start_time_raw.split('.'))
    start_datetime = datetime.datetime(
        year=start_date.year,
        month=start_date.month,
        day=start_date.day,
        hour=int(start_hour_str),
        minute=int(start_minute_str),
    )
    return {
        'competition': competition,
        'home_team': home_team,
        'away_team': away_team,
        'start_datetime': start_datetime,
    }
