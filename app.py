import csv
import json
import os

from colorama import Back, Style
from dotenv import load_dotenv
from prettytable import PrettyTable
from requests import Session

load_dotenv()
cmc_api_key = os.getenv('API_KEY')
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': cmc_api_key,
}
convert = 'GBP'


def coin_list_api_call():
    """Make API call to retrieve list of all active coins using /v1/cryptocurrency/map endpoint."""
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/map'
    parameters = {
        'listing_status': 'active',
        'sort': 'id',
    }
    session = Session()
    session.headers.update(headers)
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    coin_symbols = ([d['symbol'] for d in data['data']])
    return coin_symbols


def rankings_api_call(selection):
    """Make API call for rankings options using /v1/cryptocurrency/listings/latest endpoint."""
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start': 1,
      'limit': 100,
      'convert': convert,
      'sort': 'market_cap',
    }

    if selection == '1':
        parameters['sort'] = 'market_cap'

    if selection == '2':
        parameters['sort'] = 'percent_change_24h'

    if selection == '3':
        parameters['sort'] = 'volume_24h'

    if selection == '5':
        parameters['convert'] = input('Enter currency ticker: ')  # TODO: add full CMC ISO 8601 currency support

    session = Session()
    session.headers.update(headers)
    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    currencies = data['data']
    return parameters, currencies


def portfolio_api_call(list_of_coins):
    """Make API call for individual coins using /v1/cryptocurrency/quotes/latest endpoint."""
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
      'symbol': '',
      'convert': convert,
    }
    session = Session()
    session.headers.update(headers)
    currencies_data = []

    for coin in list_of_coins:
        parameters['symbol'] = list_of_coins[list_of_coins.index(coin)]
        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        currency = data['data'][parameters['symbol']]
        currencies_data.append(currency)

    return coin, parameters, currencies_data


def populate_rankings_table(parameters, currencies, table):
    """Insert rows into rankings table for returned currencies."""
    for currency in currencies:
        quotes = currency['quote'][parameters['convert']]
        rank = currency['cmc_rank']
        name = currency['name']
        ticker = currency['symbol']
        price = round(float(quotes['price']), 3)

        if (quotes['volume_24h']) is None:
            volume = 0
        else:
            volume = int(quotes['volume_24h'])
        volume_string = '{:,}'.format(volume)

        if quotes['market_cap'] is None:
            market_cap = 0
        else:
            market_cap = int(quotes['market_cap'])
        market_cap_string = '{:,}'.format(market_cap)

        if quotes['percent_change_1h'] is None:
            hour_change = 0
        else:
            hour_change = round(quotes['percent_change_1h'], 2)

            if hour_change >= 0:
                hour_change = Back.GREEN + str(hour_change) + '%' + Style.RESET_ALL
            else:
                hour_change = Back.RED + str(hour_change) + '%' + Style.RESET_ALL

        if quotes['percent_change_24h'] is None:
            day_change = 0
        else:
            day_change = round(quotes['percent_change_24h'], 2)

            if day_change >= 0:
                day_change = Back.GREEN + str(day_change) + '%' + Style.RESET_ALL
            else:
                day_change = Back.RED + str(day_change) + '%' + Style.RESET_ALL

        if quotes['percent_change_7d'] is None:
            week_change = 0
        else:
            week_change = round(quotes['percent_change_7d'], 2)

            if week_change >= 0:
                week_change = Back.GREEN + str(week_change) + '%' + Style.RESET_ALL
            else:
                week_change = Back.RED + str(week_change) + '%' + Style.RESET_ALL

        table.add_row([rank,
                       name + ' (' + ticker + ')',
                       str(price),
                       market_cap_string,
                       volume_string,
                       str(hour_change),
                       str(day_change),
                       str(week_change)
                       ])
    return table


def populate_portfolio_table(parameters, currencies, table, amount_owned):
    """Insert rows into portfolio table for selected currencies."""
    portfolio_value = 0.00

    for currency, number_of_coins in zip(currencies, amount_owned):
        quotes = currency['quote'][parameters['convert']]
        name = currency['name']
        ticker = currency['symbol']
        price = round(float(quotes['price']), 3)

        if quotes['percent_change_1h'] is None:
            hour_change = 0
        else:
            hour_change = round(quotes['percent_change_1h'], 2)

            if hour_change >= 0:
                hour_change = Back.GREEN + str(hour_change) + '%' + Style.RESET_ALL
            else:
                hour_change = Back.RED + str(hour_change) + '%' + Style.RESET_ALL

        if quotes['percent_change_24h'] is None:
            day_change = 0
        else:
            day_change = round(quotes['percent_change_24h'], 2)

            if day_change >= 0:
                day_change = Back.GREEN + str(day_change) + '%' + Style.RESET_ALL
            else:
                day_change = Back.RED + str(day_change) + '%' + Style.RESET_ALL

        if quotes['percent_change_7d'] is None:
            week_change = 0
        else:
            week_change = round(quotes['percent_change_7d'], 2)

            if week_change >= 0:
                week_change = Back.GREEN + str(week_change) + '%' + Style.RESET_ALL
            else:
                week_change = Back.RED + str(week_change) + '%' + Style.RESET_ALL

        amount_owned = coin_holdings.get(number_of_coins)
        value = float(price) * float(amount_owned)
        value_string = '{:,}'.format(round(value, 2))
        portfolio_value += value
        portfolio_value_string = '{:,}'.format(round(portfolio_value, 2))
        table.add_row([name + ' (' + ticker + ')',
                       amount_owned,
                       value_string,
                       str(price),
                       str(hour_change),
                       str(day_change),
                       str(week_change)
                       ])
    return table, portfolio_value_string


def input_portfolio():
    returned_tickers = coin_list_api_call()

    while True:
        user_ticker_entry = input('Enter coin ticker (q to quit): ').upper()

        if user_ticker_entry.lower() == 'q':
            break

        if user_ticker_entry not in returned_tickers:
            while user_ticker_entry not in returned_tickers:
                user_ticker_entry = input('Enter a valid coin ticker (q to quit): ').upper()

        list_of_coins.append(user_ticker_entry)
        amount_entry = input('Enter number of coins owned (q to quit): ')  # TODO: add validation to check for numerical amount input - delete last coin entry if amount = q
        amounts_owned.append(amount_entry)

    return list_of_coins, amounts_owned


def prompt_user(input):
    """Ask user if they wish to make another menu selection."""
    valid = ['y', 'n']
    new_selection = input('Make another selection? (y/n): ').lower().strip()

    if new_selection == 'n':
        exit()
    elif new_selection not in valid:
        print()
        print('Please enter a valid input (y/n)')
        print()
        prompt_user(input)


# MAIN PROGRAM START
while True:
    print()
    print('CoinMarketCap API Explorer')
    print()
    print('1 - Top 100 by market cap')
    print('2 - Top 100 by 24 hour price change')
    print('3 - Top 100 by 24 hour volume')
    print('4 - My portfolio')  # TODO: ask if user wants to create fresh pf or import from csv + create export to csv functionality
    print('5 - Change currency')
    print('0 - Exit')
    print()

    user_choice = input('Select an option: ').strip()
    valid_choices = ['1', '2', '3', '4', '5', '0']
    rankings_choices = ['1', '2', '3']

    if user_choice not in valid_choices:
        user_choice = input('Select a valid option (0-5): ').strip()

    if user_choice in rankings_choices:
        parameters_returned, currencies_returned = rankings_api_call(user_choice)
        rankings_table = PrettyTable(['Rank',
                                      'Asset',
                                      'Price (' + parameters_returned['convert'] + ')',
                                      'Market Cap (' + parameters_returned['convert'] + ')',
                                      'Volume (' + parameters_returned['convert'] + ')',
                                      'Hourly Change',
                                      'Daily Change',
                                      'Weekly Change'])
        print(populate_rankings_table(parameters_returned, currencies_returned, rankings_table))

    if user_choice == '4':
        list_of_coins = []
        amounts_owned = []
        read_from_csv = input('Read from CSV? (y/n): ').lower().strip()

        # TODO: handle for if CSV is empty or in wrong format
        if read_from_csv == 'y':
            with open('coin_holdings.csv', 'r') as csv_file:
                lines = csv_file.readlines()

                for line in lines:
                    data = line.split(',')
                    data[0] = data[0].upper()
                    data[1] = data[1].strip()
                    list_of_coins.append(data[0])
                    amounts_owned.append(data[1])

            csv_file.close()

        if read_from_csv == 'n':
            list_of_coins, amounts_owned = input_portfolio()

            with open('coin_holdings.csv', 'w') as csv_file:
                writer = csv.writer(csv_file)
                writer.writerows(zip(list_of_coins, amounts_owned))
            print('Saving to coin_holdings.csv...')
            print()
            csv_file.close()

        coin_holdings = dict(zip(list_of_coins, amounts_owned))
        portfolio_api_call(list_of_coins)
        coin, parameters_returned, currencies_returned = portfolio_api_call(list_of_coins)
        portfolio_table = PrettyTable(['Asset',
                                       'Amount Owned',
                                       'Value (' + parameters_returned['convert'] + ')',
                                       'Price (' + parameters_returned['convert'] + ')',
                                       'Hourly Change',
                                       'Daily Change',
                                       'Weekly Change'])
        portfolio_table, portfolio_value = populate_portfolio_table(parameters_returned, currencies_returned,
                                                                    portfolio_table, coin_holdings)
        print(portfolio_table)
        print('Total Portfolio Value (' + convert + '): ' + Back.GREEN + portfolio_value + Style.RESET_ALL)

    if user_choice == '5':
        convert = input('Enter currency ticker: ')  # TODO: add full CMC ISO 8601 currency support

    if user_choice == '0':
        break

    prompt_user(input)
