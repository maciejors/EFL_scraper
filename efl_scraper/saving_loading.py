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
