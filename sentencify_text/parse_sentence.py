from cgitb import text
from tracemalloc import start
from filters.sentencify import Sentencify
import time
import json
import gspread
from gspread.cell import Cell
from oauth2client.service_account import ServiceAccountCredentials
import os

processor = Sentencify()  # it will use cuda if torch.cuda.is_available()

# example input data

# text_segments = [
#     "lay the tomatoes on the tray",
#     "and these go into the oven for about 90",
#     "minutes if you turn the oven down really",
#     "low you can leave them in overnight"]
# start_timestamps = [33.45, 36.84, 39.69, 41.67]
# end_timestamps =   [39.69, 41.67, 43.77, 45.59]

spreadsheet_url_lsit = ["https://docs.google.com/spreadsheets/d/1Ydt8vGijF6MrKvLaCOnIq0vducaJO_j1O2pQmFal5gw/edit#gid=0",
                        "https://docs.google.com/spreadsheets/d/1MPe14tDgfOaWSVaLE9ivS3Fvqo6RXv3wIpwzko7BwcM/edit#gid=0",
                        "https://docs.google.com/spreadsheets/d/1jV8licHUKEPGka-lIBiQYxtquDcXEd2ER0QyAYmSbvQ/edit#gid=0",
                        "https://docs.google.com/spreadsheets/d/1962NnuDfZpUw1vQXH-J8i1OBUStwBaaDP7yzyoHOupY/edit#gid=0",
                        "https://docs.google.com/spreadsheets/d/1-qUwdkYAmiWr2pRK4JNFl-Mqjh0_6j-un0lPS9XGQso/edit#gid=0",
                        "https://docs.google.com/spreadsheets/d/1d02AceGaLHL_C1qIdl_l6doE9WYZuBzqj3XPD1vVFqA/edit#gid=0",
                        "https://docs.google.com/spreadsheets/d/1d02AceGaLHL_C1qIdl_l6doE9WYZuBzqj3XPD1vVFqA/edit#gid=0",
                        "https://docs.google.com/spreadsheets/d/1d-pkD8WY2ZqyVyVihZKENUgvQKZVM7ZA2knV3yyzKnE/edit#gid=0",
                        "https://docs.google.com/spreadsheets/d/17MCFoO53b661LpvbglUm3-ar8wC5X9DM8LwslU9vXSE/edit#gid=0",
                        "https://docs.google.com/spreadsheets/d/1ognIlIu1WAbdWsz9MQAODT20HQHNyqYSZXKaycT3HyI/edit#gid=0",
                        "https://docs.google.com/spreadsheets/d/1CkIrtT0tnlyh4b_h3qeYxkE015G0t5YlVeZx9KYOC9w/edit#gid=0",
                        "https://docs.google.com/spreadsheets/d/1MaBTASNLjnFifbylUfdL8ZuH6TUx1tIiy6U9wDTyw9I/edit#gid=0"]

### Step 1 ###
# parse input json file into input data format
htm_root = './../data_script/selected'
dir_index = 0
for root, dirs, files in os.walk(htm_root):
    for dir_name in dirs:
        # print(dir_name) #category
        category_dir = htm_root + "/"+dir_name
        files = os.listdir(category_dir)
        for file in files:
            caption_json = os.path.join(category_dir, file)
            tic = time.time()
            print('loading caption from json file')
            with open(caption_json) as f:
                raw_caption = json.load(f)
            print(f'loading completed, takes {time.time()-tic} seconds')

            text_segments = []
            start_timestamps = []
            end_timestamps = []
            for chunk in raw_caption:
                text_segments.append(chunk['text'])
                start_timestamps.append(chunk['start'])
                end_timestamps.append(chunk['start'] + chunk['duration'])

            ### Step 2 ###
            # can also interpolate the start/end timestamps for output sentences
            sentences, new_start, new_end = processor.punctuate_and_cut(
                text_segments, start_timestamps, end_timestamps)

            print(list(zip(sentences, new_start, new_end)))
            # >>> [('lay the tomatoes on the tray and these go into the oven for about 90 minutes', 33.45, 40.20), ('if you turn the oven down really low you can leave them in overnight', 40.20, 45.59)]

            ### Step 3 ###
            ### create google sheet and copy the parsed sentences in the sheet ###
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive',
            ]

            json_file_name = 'videomap-taxonomy-f38ec095e98c.json'

            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                json_file_name, scope)
            gc = gspread.authorize(credentials)

            spreadsheet_url = spreadsheet_url_lsit[dir_index]

            # spreadsheet_url = 'https://docs.google.com/spreadsheets/d/17XwIQ0lOYu9lecklbSmlNhyy5i_7o4i1DWJDvNqDgEM/edit#gid=0'
            # https://docs.google.com/spreadsheets/d/1Ydt8vGijF6MrKvLaCOnIq0vducaJO_j1O2pQmFal5gw/edit#gid=0
            # https://docs.google.com/spreadsheets/d/1MPe14tDgfOaWSVaLE9ivS3Fvqo6RXv3wIpwzko7BwcM/edit#gid=0
            # https://docs.google.com/spreadsheets/d/1jV8licHUKEPGka-lIBiQYxtquDcXEd2ER0QyAYmSbvQ/edit#gid=0
            # https://docs.google.com/spreadsheets/d/1962NnuDfZpUw1vQXH-J8i1OBUStwBaaDP7yzyoHOupY/edit#gid=0
            # https://docs.google.com/spreadsheets/d/1-qUwdkYAmiWr2pRK4JNFl-Mqjh0_6j-un0lPS9XGQso/edit#gid=0
            # https://docs.google.com/spreadsheets/d/1d02AceGaLHL_C1qIdl_l6doE9WYZuBzqj3XPD1vVFqA/edit#gid=0
            # https://docs.google.com/spreadsheets/d/1d02AceGaLHL_C1qIdl_l6doE9WYZuBzqj3XPD1vVFqA/edit#gid=0
            # https://docs.google.com/spreadsheets/d/1d-pkD8WY2ZqyVyVihZKENUgvQKZVM7ZA2knV3yyzKnE/edit#gid=0
            # https://docs.google.com/spreadsheets/d/17MCFoO53b661LpvbglUm3-ar8wC5X9DM8LwslU9vXSE/edit#gid=0
            # https://docs.google.com/spreadsheets/d/1ognIlIu1WAbdWsz9MQAODT20HQHNyqYSZXKaycT3HyI/edit#gid=0
            # https://docs.google.com/spreadsheets/d/1CkIrtT0tnlyh4b_h3qeYxkE015G0t5YlVeZx9KYOC9w/edit#gid=0
            # https://docs.google.com/spreadsheets/d/1MaBTASNLjnFifbylUfdL8ZuH6TUx1tIiy6U9wDTyw9I/edit#gid=0

            doc = gc.open_by_url(spreadsheet_url)

            worksheet = doc.worksheet(file)

            cells = []
            cells.append(Cell(row=1, col=1, value='Script'))
            cells.append(Cell(row=1, col=2, value='Start'))
            cells.append(Cell(row=1, col=3, value='End'))
            cells.append(Cell(row=1, col=4, value='Saelyne'))
            cells.append(Cell(row=1, col=5, value='Sangkyung'))
            cells.append(Cell(row=1, col=6, value='Juhoon'))
            cells.append(Cell(row=1, col=8, value='End (Visual)'))
            cells.append(Cell(row=1, col=9, value='Saelyne'))
            cells.append(Cell(row=1, col=10, value='Sangkyung'))
            cells.append(Cell(row=1, col=11, value='Juhoon'))

            for index in range(len(sentences)):
                cells.append(Cell(row=index+2, col=1, value=sentences[index]))
                cells.append(Cell(row=index+2, col=2, value=new_start[index]))
                cells.append(Cell(row=index+2, col=3, value=new_end[index]))

            worksheet.update_cells(cells)
        dir_index += 1
