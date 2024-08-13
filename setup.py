from setuptools import setup, find_packages

setup(
    name='efl_scraper',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'selenium~=4.23',
        'beautifulsoup4~=4.12',
        'pandas~=2.2',
        'tqdm~=4.66',
    ],
    entry_points={
        'console_scripts': [
            'efl_fetch=scripts.fetch_data:main',
            'efl_browse=scripts.browse_data:main',
        ],
    },
)
