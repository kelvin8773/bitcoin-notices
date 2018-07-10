'''
Learning Python Startup Project - Get Bitcoin Price Notices
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
from datetime import datetime

BITCOIN_PRICE_HIGH_THRESHOLD = 7500
BITCOIN_PRICE_LOW_THRESHOLD = 6500
BITCOIN_API_URL='https://api.coinmarketcap.com/v1/ticker/bitcoin/'

'''
Hide one paramater 'IFTTT_WEBHOOKS_URL', please add by yourself due to privacy issue.
It should similar like the line below:
IFTTT_WEBHOOKS_URL='https://maker.ifttt.com/trigger/{}/with/key/{your key}'

'''


def get_latest_bitcoin_price():
    response = requests.get(BITCOIN_API_URL)
    response_json = response.json()
    # convert the price to a floating point number
    return float(response_json[0]['price_usd'])

def post_ifttt_webhook(event, value):
    # the payload that will be sent to IFTTT service
    data = {'value1': value}
    # inserts our desrie event
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)
    # Send a HTTP POST request to the webhook URL
    requests.post(ifttt_event_url, json=data)

def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        # Formats the date into a string: '24.02.2018 15:01'
        date = bitcoin_price['date'].strftime('%Y-%m-%d %H:%M:%S')
        price = bitcoin_price['price']
        # <b> (bold) tag creates bolded text
        # 24.02.2018 15:09: $<b>10123.4</b>
        row = '{}: $<b>{}</b>'.format(date, price)
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
        sheet.append_row(value)


def main():
    bitcoin_history = []
    while True:
        price = get_latest_bitcoin_price()
        date = datetime.now()
        rowrecord = [date.strftime('%Y-%m-%d %I:%M:%S'), price]

        # Save price records to google sheets
        append_values_googlesheets(rowrecord, 'price_history', 'temp')

        # add to bitcoin history for messages
        bitcoin_history.append({'date': date, 'price': price})

        # Send an emegency notification
        if price > BITCOIN_PRICE_HIGH_THRESHOLD or price < BITCOIN_PRICE_LOW_THRESHOLD:
            post_ifttt_webhook('bitcoin_price_emergency', price)

        # Send a Telegram notification
        # Once we have 5 items in our bitcoin_history send an update
        if len(bitcoin_history) == 5:
            messages = format_bitcoin_history(bitcoin_history)
            print(messages)
            post_ifttt_webhook('bitcoin_price_update', messages)

            # Reset bitcoin history
            bitcoin_history = []

        # sleep for 5 mins
        time.sleep(5*60)


if __name__ == '__main__':
    main()
