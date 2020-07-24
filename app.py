import json

from colorama import Back, Style
from prettytable import PrettyTable
from requests import Session


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

response = session.get(listings_url, params=parameters)
data = json.loads(response.text)
currencies = data['data']

while True:
    print()
    print('CoinMarketCap API Explorer')
    # Display global market cap here
    print()
    print('1 - Top 100 by market cap')
    print('2 - Top 100 by 24 hour price change')
    print('3 - Top 100 by 24 hour volume')
    # print('4 - Change currency')
    # Add option to change how many currencies are viewed - add parameters['limit'] into strings above
    print('0 - Exit')
    print()
    user_choice = input('Select an option: ')  # Add validation here

    if user_choice == '1':
        parameters['sort'] = 'market_cap'

    if user_choice == '2':
        parameters['sort'] = 'percent_change_24h'

    if user_choice == '3':
        parameters['sort'] = 'volume_24h'

    if user_choice == '0':
        break

    response = session.get(listings_url, params=parameters)
    data = json.loads(response.text)
    currencies = data['data']

    table = PrettyTable(['Rank', 'Asset', 'Price (' + parameters['convert'] + ')',
                         'Market Cap', 'Volume', 'Hourly Change',
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
        hour_change = round(quotes['percent_change_1h'], 2)
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

        table.add_row([rank,
                       name + ' (' + ticker + ')',
                       str(price),
                       market_cap_string,
                       volume_string,
                       str(hour_change),
                       str(day_change),
                       str(week_change)])

    print()
    print(table)
    print()

    user_choice = input('Make another selection? (y/n): ')  # Add validation here

    if user_choice == 'n':
        break
