import gspread
from oauth2client.service_account import ServiceAccountCredentials


# use creds to create a client to interact with the Google Drive API
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

creds = ServiceAccountCredentials.from_json_keyfile_name('Update-Bitcoin-Price.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open the first sheet
# Make sure you use the right name here.
sh = client.open("price_history")

sheet = sh.worksheet('bitcoin')
bcprice = ['09.07.2018 19:50', '$6780.27']

sheet.append_row(bcprice)
values = sheet.get_all_values()
print(values)
