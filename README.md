# EFL Scraper

## Overview

I made this to be able to quickly check which EFL (and Premier League) fixtures can be watched on Viaplay in Poland. The project consists of two scripts:
- `fetch_data.py` - Visits viaplay.pl to check for available fixtures in Premier League, Championship, League One, League Two, and Carabao Cup. Any fixutres found are saved into a CSV file. 
- `browse_data.py` - Loads previously saved data and runs an interactive shell for a user to browse the data. User can list all fixtures, or filter them by team/competition

## Usage
Scripts need to be run from the project's root directory. Try it:
- `python3 -m scripts.fetch_data --help`
- `python3 -m scripts.browse_data --help`

## Main packages used
- Selenium
- BeautifulSoup4
- pandas
