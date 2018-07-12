'''
Learning Python Startup Project - Get cyptocurrencies Price Notices
Date: 2018-07-10
Author: Kelvin Liang
Reference: https://realpython.com/python-bitcoin-ifttt/

'''

# for read & write price history to Google Sheets
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Original Projects
import requests
import time
# from datetime import datetime
import datetime

BITCOIN_PRICE_HIGH_THRESHOLD = 7500
BITCOIN_PRICE_LOW_THRESHOLD = 6500
BITCOIN_API_URL='https://api.coinmarketcap.com/v1/ticker/bitcoin/'
ETHEREUM_API_URL='https://api.coinmarketcap.com/v1/ticker/ethereum/'

'''
Hide one paramater 'IFTTT_WEBHOOKS_URL', please add by yourself due to privacy issue.
It should similar like the line below:
IFTTT_WEBHOOKS_URL='https://maker.ifttt.com/trigger/{}/with/key/{your key}'

'''


def get_latest_info(URL):
    try:
        response = requests.get(URL)
        response_json = response.json()
    except Exception as e:
        print(e)
    else:
        print("Info from CoinMarket API retrieved.")
    finally:
        pass

    # Getting Price Update info
    response = {
                'last_updated': datetime.datetime.fromtimestamp(int(response_json[0]['last_updated'])).strftime('%Y-%m-%d %H:%M:%S'),
                'percent_change_1h': float(response_json[0]['percent_change_1h']),
                'percent_change_24h': float(response_json[0]['percent_change_24h']),
                'percent_change_7d': float(response_json[0]['percent_change_7d']),
                'price_usd': float(response_json[0]['price_usd'])
                }

    return response

def post_ifttt_webhook(event, value):
    # the payload that will be sent to IFTTT service
    data = {'value1': value}
    # inserts our desrie event
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    # Send a HTTP POST request to the webhook URL
    requests.post(ifttt_event_url, json=data)

def format_history(history):
    rows = []
    for record in history:
        # Formats the date into a string: '24.02.2018 15:01'
        bname = record[0]['name']
        bdate = record[0]['date']
        bprice = record[0]['price']

        row = '<b>{}</b> {}: $<b>{}</b>'.format(bname, bdate, bprice)
        rows.append(row)

        ename = record[1]['name']
        edate = record[1]['date']
        eprice = record[1]['price']

        row = '<b>{}</b> {}: $<b>{}</b>'.format(ename, edate, eprice)
        rows.append(row)

    # Use a <br> (break) tag to create a new line
    # Join the rows delimited by <br> tag: row1<br>row2<br>row3
    return '<br>'.join(rows)


def append_values_googlesheets(value, workbook, sheetname):
        # use creds to create a client to interact with the Google Drive API
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']

        creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
        client = gspread.authorize(creds)

        # Find a workbook by name and open the sheet your specify
        sh = client.open(workbook)
        sheet = sh.worksheet(sheetname)
        response = sheet.append_row(value)
        # print(response)
        return response


def main():
    history = []

    while True:

        # retrieve info from API JSON
        bitcoin_info = get_latest_info(BITCOIN_API_URL)
        brecord = [
                    bitcoin_info['last_updated'],
                    bitcoin_info['price_usd'],
                    bitcoin_info['percent_change_1h'],
                    bitcoin_info['percent_change_24h'],
                    bitcoin_info['percent_change_7d']
                ]
        ethereum_info = get_latest_info(ETHEREUM_API_URL)
        erecord = [
                    ethereum_info['last_updated'],
                    ethereum_info['price_usd'],
                    ethereum_info['percent_change_1h'],
                    ethereum_info['percent_change_24h'],
                    ethereum_info['percent_change_7d']
                  ]
        print(bitcoin_info)
        print(ethereum_info)

        try:
            append_values_googlesheets(brecord, 'price_history', 'bitcoin')
            append_values_googlesheets(erecord, 'price_history', 'ethereum')
        except Exception as e:
            print("Something went wrong!")
            print(e)
            time.sleep(1*30)
            pass
        else:
            print("Records Saved.")
            # add to bitcoin history for messages
            history.append(
                        [
                            {'name': 'Bitcoin',
                                'date': bitcoin_info['last_updated'],
                                'price': bitcoin_info['price_usd']},
                            {'name': 'Ethereum',
                                'date': ethereum_info['last_updated'],
                                'price': ethereum_info['price_usd']}
                         ]
                        )
        finally:
            print("Continue to next record ....")
            pass

        # Send an emegency notification
        if bitcoin_info['price_usd'] > BITCOIN_PRICE_HIGH_THRESHOLD or bitcoin_info['price_usd'] < BITCOIN_PRICE_LOW_THRESHOLD:
            post_ifttt_webhook('bitcoin_price_emergency', bitcoin_info['price_usd'])

        # Send a Telegram notification
        # Once we have 5 items in our history send an update
        if len(history) == 5:
            messages = format_history(history)
            post_ifttt_webhook('bitcoin_price_update', messages)
            # Reset history
            history = []

        # sleep for 5 mins
        time.sleep(5*60)


if __name__ == '__main__':
    main()
