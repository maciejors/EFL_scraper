import time
import re

import bs4
from selenium import webdriver
from tqdm import tqdm

from .parsing_matches import get_match_data_from_raw


def _get_url_for_competition(competition: str):
    return f'https://viaplay.pl/search#search={competition}'


def _load_page_contents(driver: webdriver.Chrome, competition: str, page_wait_time: float) -> str:
    url = _get_url_for_competition(competition)
    driver.get(url)
    # wait for page to load
    time.sleep(page_wait_time)
    page_source = driver.page_source
    return page_source


def _scrape_match_data(competition: str, page_source: str) -> list[dict]:
    soup = bs4.BeautifulSoup(page_source, 'html.parser')

    competition_labels = soup.find_all(
        name='span',
        string=competition,
        attrs={'class': re.compile('EpisodeMeta_secondaryTitle.*')},
    )
    matches_data: list[dict] = []

    for label in competition_labels:
        match_element: bs4.element.Tag = label.parent.parent.parent.parent
        match_title_tag = match_element.find(
            name='div',
            attrs={'class': re.compile('SportMeta_title.*')},
        )
        # filter out extra programs
        if '-' not in match_title_tag.text:
            continue

        start_date_tag = match_element.find(
            name='div',
            attrs={'class': re.compile('Badge_badge.*')},
        )
        start_time_tag = match_element.find(
            name='div',
            attrs={'class': re.compile('SportMeta_start.*')},
        )
        match_data = get_match_data_from_raw(
            competition,
            match_title_raw=match_title_tag.text,
            start_date_raw=start_date_tag.text,
            start_time_raw=start_time_tag.text,
        )
        matches_data.append(match_data)

    return matches_data


def scrape_matches_data(competitions: str, page_wait_time: float) -> list[dict]:
    """
    Scrape available data for a single competition.
    This involves a single GET request.

    Args:
        competitions: Competitions names (search terms)
        page_wait_time: how many seconds to wait for the page to load.

    Returns:
        list of matches data, each match is encoded as a
        dictionary with the following keys:
        - competition
        - home_team
        - away_team
        - start_datetime
    """
    driver = webdriver.Chrome()

    matches_data_all_competitions: list[dict] = []
    for competition in tqdm(competitions):
        page_source = _load_page_contents(driver, competition, page_wait_time)
        new_matches_data = _scrape_match_data(competition, page_source)
        matches_data_all_competitions.extend(new_matches_data)

    driver.quit()
    return matches_data_all_competitions
