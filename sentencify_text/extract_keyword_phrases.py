from cgitb import text
import enum
from tracemalloc import start
import time
import json
import gspread
from gspread.cell import Cell
from oauth2client.service_account import ServiceAccountCredentials
import os


spreadsheet_url_list = {
    "Arts and Entertainment" : "https://docs.google.com/spreadsheets/d/1Ydt8vGijF6MrKvLaCOnIq0vducaJO_j1O2pQmFal5gw/edit#gid=0",
    "Cars & Other Vehicles" : "https://docs.google.com/spreadsheets/d/1MPe14tDgfOaWSVaLE9ivS3Fvqo6RXv3wIpwzko7BwcM/edit#gid=0",
    "Computers and Electronics" : "https://docs.google.com/spreadsheets/d/1jV8licHUKEPGka-lIBiQYxtquDcXEd2ER0QyAYmSbvQ/edit#gid=0",
    "Education and Communications" : "https://docs.google.com/spreadsheets/d/1962NnuDfZpUw1vQXH-J8i1OBUStwBaaDP7yzyoHOupY/edit#gid=0",
    "Food and Entertaining" : "https://docs.google.com/spreadsheets/d/1-qUwdkYAmiWr2pRK4JNFl-Mqjh0_6j-un0lPS9XGQso/edit#gid=0",
    "Health" : "https://docs.google.com/spreadsheets/d/1d-pkD8WY2ZqyVyVihZKENUgvQKZVM7ZA2knV3yyzKnE/edit#gid=0",
    "Hobbies and Crafts" : "https://docs.google.com/spreadsheets/d/1d02AceGaLHL_C1qIdl_l6doE9WYZuBzqj3XPD1vVFqA/edit#gid=0",
    "Holidays and Traditions" : "https://docs.google.com/spreadsheets/d/1R4guptruK65carVVeJ_l32ElslBgJJtYPty8GQfkXZY/edit#gid=0",
    "Home and Garden" : "https://docs.google.com/spreadsheets/d/17MCFoO53b661LpvbglUm3-ar8wC5X9DM8LwslU9vXSE/edit#gid=0",
    "Personal Care and Style" : "https://docs.google.com/spreadsheets/d/1ognIlIu1WAbdWsz9MQAODT20HQHNyqYSZXKaycT3HyI/edit#gid=0",
    "Pets and Animals" : "https://docs.google.com/spreadsheets/d/1CkIrtT0tnlyh4b_h3qeYxkE015G0t5YlVeZx9KYOC9w/edit#gid=0",
    "Sports and Fitness" : "https://docs.google.com/spreadsheets/d/1MaBTASNLjnFifbylUfdL8ZuH6TUx1tIiy6U9wDTyw9I/edit#gid=0"
}

category_list = ["Arts and Entertainment", "Cars & Other Vehicles", "Computers and Electronics", "Education and Communications", "Food and Entertaining", "Health", "Hobbies and Crafts", "Holidays and Traditions", "Home and Garden", "Personal Care and Style", "Pets and Animals", "Sports and Fitness"]


scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]
json_file_name = 'videomap-taxonomy-f38ec095e98c.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    json_file_name, scope)
gc = gspread.authorize(credentials)

category = category_list[11]
keyword = "outline"
rs = []

# for category in spreadsheet_url_list.keys():
#     spreadsheet_url = spreadsheet_url_list[category]
#     doc = gc.open_by_url(spreadsheet_url)

#     worksheet_list = doc.worksheets()

#     for ws in worksheet_list:
#         phrase_list = ws.col_values(1)
#         info_list = ws.col_values(7)
#         if info_list != []:
#             for idx, val in enumerate (info_list):
#                 if val == keyword:
#                     phrase = phrase_list[idx]
#                     rs.append (phrase)

spreadsheet_url = spreadsheet_url_list[category]
doc = gc.open_by_url(spreadsheet_url)

worksheet_list = doc.worksheets()

for ws in worksheet_list:
    phrase_list = ws.col_values(1)
    info_list = ws.col_values(8)
    if info_list != []:
        for idx, val in enumerate (info_list):
            if val == keyword:
                phrase = phrase_list[idx]
                rs.append (phrase)

if (len(rs) == 0):
    print ("keyword: ", keyword)
    print (category, ": no keyword")
else:
    print ("keyword: ", keyword)
    print (category)
    print ("number of info phrases: ", len (rs))
    for phrase in rs:
        print (phrase)

