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
        print(date.strftime("%d/%m/%Y"))
        fixtures_on_date = df_fixtures[dates == date]
        for idx, row in fixtures_on_date.iterrows():
            print(_pretty_row(row))
        print()


def competition_cmd(df_fixtures: pd.DataFrame, competition: str | None = None) -> None:
    if competition is None:
        available_competitions = df_fixtures['competition'].unique()
        print('Available competitions:')
        for comp in available_competitions:
            print(f'- {comp}')
    else:
        fixtures_competition = df_fixtures[df_fixtures['competition'] == competition]
        if len(fixtures_competition) == 0:
            print('No fixtures available for this competition')
        else:
            list_fixtures(fixtures_competition)


def club_cmd(df_fixtures: pd.DataFrame, club: str | None = None) -> None:
    if club is None:
        available_home = df_fixtures['home_team'].unique()
        available_away = df_fixtures['away_team'].unique()
        available_total = set(available_home) | set(available_away)
        print('Available clubs:')
        for team in available_total:
            print(f'- {team}')
    else:
        fixtures_club = df_fixtures[
            (df_fixtures['home_team'] == club) | (df_fixtures['away_team'] == club)
        ]
        if len(fixtures_club) == 0:
            print('No fixtures available for this club')
        else:
            list_fixtures(fixtures_club)


def today_cmd(df_fixtures: pd.DataFrame) -> None:
    """Lists today's fixtures"""

