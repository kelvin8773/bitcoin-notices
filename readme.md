# Learning Python Startup project - Get Bitcoin Price Notices

Thanks for following authors's article:
- [Rok Novosel (English) - Python Project for Beginners: Bitcoin Price Notifications ](https://realpython.com/python-bitcoin-ifttt/)
- [Python数据科学 (Chinese) - 给Python初学者的最好练手项目](https://juejin.im/post/5ac42bcd5188255c887bd81e)


### Introduction

A very good startup project for learning python.

As Rok Suggested in his article, beside following every step in the articles, I will continue adding new features into this project to make it more practical for the real world projects.

Currently added Features:

1. Send Notices to Telegram. (2018-07-03)
2. Save Prices history to Google Sheets. (2018-07-10)

To continue ....


### Getting Start  

1. clone this project to your local drive.
2. register IFTTT to get "IFTTT_WEBHOOKS_URL", then export it in your environment.

```
export IFTTT_WEBHOOKS_URL='https://maker.ifttt.com/trigger/{}/with/key/{Your Key}'
```
3. register google sheet API for save records in your google sheet.
[get credentials.json file](http://gspread.readthedocs.io/en/latest/oauth2.html)

4. Run `python start-script.py` to start the program.

5. Start from there, you continue add whatever features you can think of to this project.

Enjoy!

Kelvin

### Other Reference Links
[gspread for google sheets documents](http://gspread.readthedocs.io/en/latest/#main-interface)
