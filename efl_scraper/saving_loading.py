import os

import pandas as pd


def save_matches_data(matches_data: list[dict], path: str) -> str:
    """
    Save matches data to a .csv file

    Args:
        matches_data: data to save
        path: path to a file where the data will be saved

    Returns:
        An absolute path to where the data was saved
    """
    df = pd.DataFrame(matches_data)
    df.to_csv(path, index=False)
    save_path = os.path.abspath(path)
    return save_path


def load_matches_data(path: str) -> pd.DataFrame | None:
    """
    Save matches data to a .csv file

    Args:
        path: path to a file to load, or a directory with multiple files to load

    Returns:
        A dataframe of matches data with the following columns
        - competition (str)
        - home_team (str)
        - away_team (str)
        - start_datetime (datetime)
        Will return None if the provided path is invalid
    """
    if os.path.isfile(path):
        return pd.read_csv(path)

    if os.path.isdir(path):
        files_data: list[pd.DataFrame] = []

        for filename in os.listdir(path):
            if filename.endswith('.csv'):
                file_data = pd.read_csv(os.path.join(path, filename))
                files_data.append(file_data)

        full_data = pd.concat(files_data).drop_duplicates()
        full_data['start_datetime'] = pd.to_datetime(full_data['start_datetime'])
        full_data = full_data.sort_values('start_datetime')
        return full_data

    return None
