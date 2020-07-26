# CoinMarketCap CLI App

This is a command-line app that uses the CoinMarketCap API to provide information about cryptocurrencies, split into two sections:
1. Top 100 performing cryptocurrencies by market cap, 24 hour price change, and daily volume
2. A user-entered list of currencies

These are then presented in ASCII table format using the PrettyTable library, with Colorama providing some colour to illustrate changes in price information.

## Dependencies

- Python 3
- PrettyTable
- Colorama

The complete list can be found in requirements.txt, and can be installed with 'pip install -r requirements.txt'.

## To run

1. Download or clone the repository
2. cd into the directory
3. Run app.py