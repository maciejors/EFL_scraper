import json
import datetime
import argparse

from efl_scraper.fetching_data import scrape_matches_data
from efl_scraper import save_matches_data


CONFIG_PATH = './scripts/fetch_data_config.json'


def main():
    parser = argparse.ArgumentParser(
        description='Scrape current data from viaplay.com',
    )
    parser.add_argument(
        '--page-wait-time', '-w',
        type=float,
        help='How many seconds to wait for the page to load',
        default=5.0,
    )
    parser.add_argument(
        '--output-path', '-o',
        type=str,
        help='Path to a file where the data will be saved',
        default=f'./data/data-{datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")}.csv',
    )
    args = parser.parse_args()

    with open(CONFIG_PATH) as config_file:
        config = json.load(config_file)
        competitions = config['competitions']

    print('Scraping data...')
    matches_data = scrape_matches_data(competitions, page_wait_time=args.page_wait_time)

    output_path_abs = save_matches_data(matches_data, args.output_path)
    print(f'Matches data saved to {output_path_abs}')


if __name__ == '__main__':
    main()
