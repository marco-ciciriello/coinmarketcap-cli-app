import json

from colorama import Back, Style
from prettytable import PrettyTable
from requests import Session


def prompt_user(input):
    valid = ['y', 'n']
    user_choice = input('Make another selection? (y/n): ').lower().strip()

    if user_choice == 'n':
        exit()
    elif user_choice not in valid:
        print('Please enter a valid input (y/n)')
        prompt_user(input)


def user_portfolio():
    portfolio_listings_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
      'symbol': '',
      'convert': 'GBP',
    }
    headers = {
      'Accepts': 'application/json',
      'X-CMC_PRO_API_KEY': 'CHANGE THIS TO YOUR COINMARKETCAP API KEY',
    }

    session = Session()
    session.headers.update(headers)

    list_of_coins = ['BTC', 'ETH', 'LTC', 'MIOTA', 'LINK']
    amounts_owned = [2, 3.33, 43.36, 22058, 1695]
    coin_holdings = dict(zip(list_of_coins, amounts_owned))
    portfolio_value = 0.00
    last_updated = 0
    portfolio_table = PrettyTable(['Asset', 'Amount Owned',
                                   'Value (' + parameters['convert'] + ')',
                                   'Price (' + parameters['convert'] + ')',
                                   'Hourly Change',
                                   'Daily Change', 'Weekly Change'])

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

        if hour_change > 0:
            hour_change = Back.GREEN + str(hour_change) + '%' + Style.RESET_ALL
        else:
            hour_change = Back.RED + str(hour_change) + '%' + Style.RESET_ALL

        if day_change > 0:
            day_change = Back.GREEN + str(day_change) + '%' + Style.RESET_ALL
        else:
            day_change = Back.RED + str(day_change) + '%' + Style.RESET_ALL

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
    # last_updated_string = datetime.fromtimestamp(last_updated).strftime('%B %d, %Y at %I:%M%p')

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
      'X-CMC_PRO_API_KEY': 'CHANGE THIS TO YOUR COINMARKETCAP API KEY',
    }

    session = Session()
    session.headers.update(headers)

    print()
    print('CoinMarketCap API Explorer')
    # Display global market cap here
    print()
    print('1 - View my portfolio')
    print('2 - Top 100 by market cap')
    print('3 - Top 100 by 24 hour price change')
    print('4 - Top 100 by 24 hour volume')
    print('5 - Change currency')
    # TODO: Add option to change how many currencies are viewed - add parameters['limit'] into strings above
    print('0 - Exit')
    print()
    user_choice = input('Select an option: ')  # TODO: Add validation here

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
                                  'Volume (' + parameters['convert'] + ')', 'Hourly Change',
                                  'Daily Change', 'Weekly Change'])

    print()

    for currency in currencies:
        rank = currency['cmc_rank']
        name = currency['name']
        ticker = currency['symbol']
        quotes = currency['quote'][parameters['convert']]
        price = round(float(quotes['price']), 3)

        if quotes['market_cap'] is None:
            market_cap = 0
        else:
            market_cap = int(quotes['market_cap'])

        volume = int(quotes['volume_24h'])

        if quotes['percent_change_7d'] is None:
            hour_change = 0
        else:
            hour_change = round(quotes['percent_change_1h'], 2)

        if quotes['percent_change_7d'] is None:
            day_change = 0
        else:
            day_change = round(quotes['percent_change_24h'], 2)

        if quotes['percent_change_7d'] is None:
            week_change = 0
        else:
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
