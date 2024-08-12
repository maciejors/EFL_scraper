import argparse

from efl_scraper import load_matches_data
from efl_scraper.browsing import run_shell


def main():
    parser = argparse.ArgumentParser(
        description='Launches an interactive shell where user can browse the data'
                    'on broadcast EFL fixtures',
    )
    parser.add_argument(
        '--input-path', '-i',
        type=str,
        help='Path to a file or directory where the data is located',
        default=f'./data/',
    )
    args = parser.parse_args()

    df_fixtures = load_matches_data(args.input_path)

    n_fixtures = len(df_fixtures)
    if n_fixtures == 0:
        print('No fixtures data found at the specified location. Exiting...')
        return
    print(f'Found {n_fixtures} fixtures')

    run_shell(df_fixtures)


if __name__ == '__main__':
    main()
