import datetime

import pandas as pd


def _pretty_row(row: pd.Series) -> str:
    """
    Format the row in a pretty format.
    Omits the date as it is expected to be printed separately.
    """
    start_time: datetime.datetime = row['start_datetime']
    home_team: str = row['home_team']
    away_team: str = row['away_team']
    competition: str = row['competition']
    return f'{start_time.strftime("%H:%M")} | {home_team} - {away_team} | {competition}'


def list_fixtures(df_fixtures: pd.DataFrame) -> None:
    dates = df_fixtures['start_datetime'].map(lambda d: d.date())
    for date in dates.unique():
        print(date.strftime("%a %d %b %Y"))
        fixtures_on_date = df_fixtures[dates == date]
        for idx, row in fixtures_on_date.iterrows():
            print(_pretty_row(row))
        print()


def competition_cmd(df_fixtures: pd.DataFrame, competition: str | None = None) -> None:
    competition_series = df_fixtures['competition']
    if competition is None:
        available_competitions = competition_series.unique()
        print('Available competitions:')
        for comp in available_competitions:
            print(f'- {comp}')
    else:
        fixtures_competition = df_fixtures[
            df_fixtures['competition'].str.lower() == competition.lower()
        ]
        if len(fixtures_competition) == 0:
            print('No fixtures available for this competition')
        else:
            list_fixtures(fixtures_competition)


def club_cmd(df_fixtures: pd.DataFrame, club: str | None = None) -> None:
    home_teams_series = df_fixtures['home_team']
    away_teams_series = df_fixtures['away_team']
    if club is None:
        available_home = home_teams_series.unique()
        available_away = away_teams_series.unique()
        available_total = set(available_home) | set(available_away)
        available_total = sorted(list(available_total))
        print('Available clubs:')
        for team in available_total:
            print(f'- {team}')
    else:
        club_lowercase = club.lower()
        fixtures_club = df_fixtures[
            (home_teams_series.str.lower() == club_lowercase)
            | (away_teams_series.str.lower() == club_lowercase)
        ]
        if len(fixtures_club) == 0:
            print('No fixtures available for this club')
        else:
            list_fixtures(fixtures_club)


def _games_for_day(df_fixtures: pd.DataFrame, date: datetime.date) -> pd.DataFrame:
    fixtures_dates = df_fixtures['start_datetime'].map(lambda d: d.date())
    day_fixtures = df_fixtures[fixtures_dates == date]
    return day_fixtures


def today_cmd(df_fixtures: pd.DataFrame) -> None:
    """Lists today's fixtures"""
    today_fixtures = _games_for_day(
        df_fixtures,
        datetime.date.today(),
    )
    if len(today_fixtures) == 0:
        print('No fixtures today! :(')
    list_fixtures(today_fixtures)


def tomorrow_cmd(df_fixtures: pd.DataFrame) -> None:
    """Lists tomorrow's fixtures"""
    tomorrow_fixtures = _games_for_day(
        df_fixtures,
        datetime.date.today() + datetime.timedelta(days=1),
    )
    if len(tomorrow_fixtures) == 0:
        print('No fixtures tomorrow! :(')
    list_fixtures(tomorrow_fixtures)
