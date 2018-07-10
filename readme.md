### Python Learning Startup project - Get Bitcoin Price Notices

- Date: 2018-07-10
- Author: Kelvin Liang
- Email: Kelvin@kelvinoffice.com

Thanks for following authors's article
[Reference- Rok Novosel (English)](https://realpython.com/python-bitcoin-ifttt/)
[Reference- Python数据科学 (Chinese)](https://juejin.im/post/5ac42bcd5188255c887bd81e)


# Introduction

A very good startup project for learning python.

As Rok Suggested in his article, beside following every step in the articles, I will continue adding new features into this project to make it more practical for the real world projects.

Currently added Features:

1. Send Notices to Telegram. (2018-07-03)
2. Save Prices history to Google Sheets. (2018-07-10)

To continue ....


# To Getting Start  

1. clone this project to your local drive.
2. register IFTTT to get "IFTTT_WEBHOOKS_URL", then export it in your environment.

'''
export IFTTT_WEBHOOKS_URL='https://maker.ifttt.com/trigger/{}/with/key/{Your Key}'
'''
3. register google sheet API for save records in your google sheet.
[get credentials.json file](http://gspread.readthedocs.io/en/latest/oauth2.html)

4. Run "start-script.py" program.
'''
python start-script.py

'''



[Reference](https://realpython.com/python-bitcoin-ifttt/)
