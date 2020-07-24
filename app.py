import json

from colorama import Back, Style
from prettytable import PrettyTable
from requests import Session


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


def user_portfolio():
    """Create portfolio table showing holdings and performance."""
    portfolio_listings_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
      'symbol': '',
      'convert': 'GBP',
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': 'CHANGE THIS TO YOUR CMC API KEY',
    }

    session = Session()
    session.headers.update(headers)

    list_of_coins = []
    amounts_owned = []
    coin_holdings = dict(zip(list_of_coins, amounts_owned))

    while True:

        coin_entry = input('Enter coin ticker (q to quit): ')

        if coin_entry.lower() == 'q':
            break

        list_of_coins.append(coin_entry)

        amount_entry = input('Enter number of coins owned: ')

        if amount_entry.lower() == 'q':
            break

        amounts_owned.append(amount_entry)

    coin_holdings = dict(zip(list_of_coins, amounts_owned))
    portfolio_value = 0.00
    last_updated = 0
    portfolio_table = PrettyTable(['Asset', 'Amount Owned',
                                   'Value (' + parameters['convert'] + ')',
                                   'Price (' + parameters['convert'] + ')',
                                   'Hourly Change', 'Daily Change',
                                   'Weekly Change'])

    for coin in list_of_coins:
        parameters['symbol'] = list_of_coins[list_of_coins.index(coin)]
        response = session.get(portfolio_listings_url, params=parameters)
        data = json.loads(response.text)

        currency = data['data'][parameters['symbol']]
        quotes = currency['quote'][parameters['convert']]
        name = currency['name']
        ticker = currency['symbol']
        last_updated = currency['last_updated']
        amount_owned = coin_holdings.get(coin)
        price = round(float(quotes['price']), 3)
        value = float(price) * float(amount_owned)
        hour_change = round(quotes['percent_change_1h'], 2)
        day_change = round(quotes['percent_change_24h'], 2)
        week_change = round(quotes['percent_change_7d'], 2)

        if hour_change is not None:
            if hour_change > 0:
                hour_change = Back.GREEN + str(hour_change) + '%' + Style.RESET_ALL
            else:
                hour_change = Back.RED + str(hour_change) + '%' + Style.RESET_ALL

        if day_change is not None:
            if day_change > 0:
                day_change = Back.GREEN + str(day_change) + '%' + Style.RESET_ALL
            else:
                day_change = Back.RED + str(day_change) + '%' + Style.RESET_ALL

        if week_change is not None:
            if week_change > 0:
                week_change = Back.GREEN + str(week_change) + '%' + Style.RESET_ALL
            else:
                week_change = Back.RED + str(week_change) + '%' + Style.RESET_ALL

        portfolio_value += value
        value_string = '{:,}'.format(round(value, 2))

        portfolio_table.add_row([name + ' (' + ticker + ')',
                                 amount_owned,
                                 value_string,
                                 str(price),
                                 str(hour_change),
                                 str(day_change),
                                 str(week_change)
                                 ])

    print(portfolio_table)
    print()

    portfolio_value_string = '{:,}'.format(round(portfolio_value, 2))
    # last_updated_string = datetime.fromtimestamp(last_updated).strftime('%B %d, %Y at %I:%M%p')  TODO: Fix this

    print('Total Portfolio Value (' + parameters['convert'] + '): ' + Back.GREEN + portfolio_value_string +
          Style.RESET_ALL)
    print('Last Updated: ' + last_updated)  # TODO: Make this more readable


while True:

    listings_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {
      'start': 1,
      'limit': 100,
      'convert': 'GBP',
      'sort': 'market_cap',
    }
    headers = {
      'Accepts': 'application/json',
      # TODO: Change this before uploading to GitHub
      'X-CMC_PRO_API_KEY': 'CHANGE THIS TO YOUR CMC API KEY',
    }

    session = Session()
    session.headers.update(headers)

    print()
    print('CoinMarketCap API Explorer')
    print()
    print('1 - View my portfolio')  # TODO: If csv exists, import from there, else prompt user to enter - CREATE EXPORT TO CSV FUNCTIONALITY
    print('2 - Top 100 by market cap')
    print('3 - Top 100 by 24 hour price change')
    print('4 - Top 100 by 24 hour volume')
    print('5 - Change currency')
    print('0 - Exit')
    print()

    user_choice = input('Select an option: ')
    valid_choices = ['1', '2', '3', '4', '5', '0']

    if user_choice not in valid_choices:
        user_choice = input('Select a valid option (0-5): ')

    if user_choice == '1':
        user_portfolio()

    if user_choice == '2':
        parameters['sort'] = 'market_cap'

    if user_choice == '3':
        parameters['sort'] = 'percent_change_24h'

    if user_choice == '4':
        parameters['sort'] = 'volume_24h'

    if user_choice == '5':
        parameters['convert'] = input('Enter currency ticker: ')  # TODO: Add full CMC ISO 8601 currency support

    if user_choice == '0':
        break

    response = session.get(listings_url, params=parameters)
    data = json.loads(response.text)
    currencies = data['data']

    rankings_table = PrettyTable(['Rank', 'Asset', 'Price (' + parameters['convert'] + ')',
                                  'Market Cap (' + parameters['convert'] + ')',
                                  'Volume (' + parameters['convert'] + ')',
                                  'Hourly Change', 'Daily Change', 'Weekly Change'])

    print()

    for currency in currencies:
        rank = currency['cmc_rank']
        name = currency['name']
        ticker = currency['symbol']
        quotes = currency['quote'][parameters['convert']]
        price = round(float(quotes['price']), 3)
        volume = int(quotes['volume_24h'])

        if quotes['market_cap'] is None:
            market_cap = 0
        else:
            market_cap = int(quotes['market_cap'])

        if quotes['percent_change_1h'] is None:
            hour_change = 0
        else:
            hour_change = round(quotes['percent_change_1h'], 2)

            if hour_change > 0:
                hour_change = Back.GREEN + str(hour_change) + '%' + Style.RESET_ALL
            else:
                hour_change = Back.RED + str(hour_change) + '%' + Style.RESET_ALL

        if quotes['percent_change_24h'] is None:
            day_change = 0
        else:
            day_change = round(quotes['percent_change_24h'], 2)

            if day_change > 0:
                day_change = Back.GREEN + str(day_change) + '%' + Style.RESET_ALL
            else:
                day_change = Back.RED + str(day_change) + '%' + Style.RESET_ALL

        if quotes['percent_change_7d'] is None:
            week_change = 0
        else:
            week_change = round(quotes['percent_change_7d'], 2)

            if week_change > 0:
                week_change = Back.GREEN + str(week_change) + '%' + Style.RESET_ALL
            else:
                week_change = Back.RED + str(week_change) + '%' + Style.RESET_ALL

        if volume is not None:
            volume_string = '{:,}'.format(volume)

        if market_cap is not None:
            market_cap_string = '{:,}'.format(market_cap)

        rankings_table.add_row([rank,
                                name + ' (' + ticker + ')',
                                str(price),
                                market_cap_string,
                                volume_string,
                                str(hour_change),
                                str(day_change),
                                str(week_change)])

    if 2 <= int(user_choice) < 6:
        print()
        print(rankings_table)
        print()

    prompt_user(input)
