# CoinMarketCap CLI App

This is a command-line app that uses the CoinMarketCap API to provide information about cryptocurrencies, split into two sections:
1. Top 100 performing cryptocurrencies by market cap, 24 hour price change, and daily volume
2. A user-defined portfolio of currencies

These are then presented in ASCII table format using the PrettyTable library, with Colorama providing some colour to illustrate changes in price information.

Option (1) shows the top 100 currencies by market cap - cut off here at the top 50. 

<img width="983" alt="Screenshot 2020-07-18 at 10 38 23" src="https://user-images.githubusercontent.com/40694097/87849931-4c836680-c8e4-11ea-8780-4e1692f8c826.png">

This is the portfolio construction option (4) - coins can either be entered manually, or imported from CSV. 

<img width="800" alt="Screenshot 2020-07-18 at 10 39 18" src="https://user-images.githubusercontent.com/40694097/87849944-63c25400-c8e4-11ea-8de1-82efa7a3dc56.png">

## Configuring your API key

To configure your CoinMarketCap API key, create a .env file in the project directory and write `API_KEY='{YOUR API KEY}'`.

## Dependencies

- Python 3
- PrettyTable
- Colorama

The complete list can be found in requirements.txt, and can be installed with `pip install -r requirements.txt`.

## To run

1. Download or clone the repository
2. Configure your API key (see instructions in second section)
3. cd into the directory
4. Run app.py
