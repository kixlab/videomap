import os
import json
from pydub import AudioSegment
from re import L
import gspread
from gspread.cell import Cell
from oauth2client.service_account import ServiceAccountCredentials
import time

ROOT_DIR = './data/transcript/'
SAVE_DIR = './data/processed/'
AUDIO_DIR = './data/audio/'

TYPES = {'opening', 'closing', 'goal', 'motivation', 'briefing', 'subgoal', 'instruction', 'tool', 'warning', 'tip', 'justification', 'effect', 'status', 'context', 'tool specification', 'outcome', 'reflection', 'side note', 'self-promo', 'bridge', 'filler'}
CATEGORIES = {'greeting', 'overview', 'step', 'supplementary', 'explanation', 'description', 'conclusion', 'misc.'}
SECTIONS = {'intro', 'procedure', 'outro', 'misc.'}

section_hierarchy = {
    "intro": ["opening", "overview"],
    "procedure": ["step", "supplementary", "explanation", "description"],
    "outro": ["closing", "conclusion"],
    "misc.": ["misc."]
}

cat_hierarchy = {
    "greeting": ["opening", "closing"],
    "overview": ["goal", "motivation", "briefing"],
    "step": ["subgoal", "instruction", "tool"],
    "supplementary": ["warning", "tip"],
    "explanation": ["justification", "effect"],
    "description": ["status", "context", "tool specification"],
    "conclusion": ["outcome", "reflection"],
    "misc.": ["side note", "self-promo", "bridge", "filler"]
}


annotation_final_url_list = {
    # "Arts and Entertainment" : "https://docs.google.com/spreadsheets/d/19KLEoEAeD4HTF2qHCjiDEWIDh9D5Vwjgl3dj1yA3MwQ/edit#gid=0",
    # "Cars & Other Vehicles" : "https://docs.google.com/spreadsheets/d/1S8N3GXHAVzF5hMhbFjGdcadaJoEF_ev0EAU5XZWdSqo/edit#gid=0",
    # "Computers and Electronics" : "https://docs.google.com/spreadsheets/d/1nyi1ggt2rc5eDLY-ulWoWcMMQiRQqib5wifOO9PHnoo/edit#gid=0",
    # "Education and Communications" : "https://docs.google.com/spreadsheets/d/1H1ftoPm2rNiQbIC2TgI3vStWAiuQmXogSeJIjWyCD9s/edit#gid=0",
    # "Food and Entertaining" : "https://docs.google.com/spreadsheets/d/1TDBm5oWqOtp9lMU5hBAmgKc01yXgIjcjawHIyMjEP3k/edit#gid=0",
    # "Health" : "https://docs.google.com/spreadsheets/d/1B7qVxewUmkdHffVJeL5wZCJjG5ruBOxmihi-UspCDW4/edit#gid=0",
    "Hobbies and Crafts" : "https://docs.google.com/spreadsheets/d/16C5V9JHOTL-S3zT2yaX6dETZiEqxhPBheHwgfRRvnvs/edit#gid=0",
    # "Holidays and Traditions" : "https://docs.google.com/spreadsheets/d/1_tfTP4YUtC4WExwxp6yDrNdHgEkLipvx4H2dhgXCSOk/edit#gid=0",
    # "Home and Garden" : "https://docs.google.com/spreadsheets/d/1qixstHOqTMfcy5SqlBnuqUhrRTA8uYGrDFQKzdi5VEw/edit#gid=0",
    # "Personal Care and Style" : "https://docs.google.com/spreadsheets/d/1QZj_URTln1ltgTofkoaOZpFYO0MrdY7OjM4U9he_PDI/edit#gid=0",
    # "Pets and Animals" : "https://docs.google.com/spreadsheets/d/1Ic_-CCBy4J9S1q9Jx9g9EsrHvksxf3avaJWIFGZVAZ8/edit#gid=0",
    # "Sports and Fitness" : "https://docs.google.com/spreadsheets/d/1wmVT6OY4n43b3CcNtIGhLCKNzkk8c6LnRbvznhDQ2HM/edit#gid=0", 
}

vids = ['XN3N5K2axpw', 'WIIjq2GexIw']
scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive',
]

json_file_name = 'videomap-taxonomy-f38ec095e98c.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    json_file_name, scope)

gc = gspread.authorize(credentials)

# check whether word list and lexical script matches
def check_script_ts (ws_dict, ts):

    # parse lexical script into word
    words = []
    for line in ws_dict:
        words_tmp = line['Script'].strip().split (' ')
        for word in words_tmp:
            if (word != ''):
                words.append (word.lower().strip())

    ts_ind = 0
    ts_modified = []
    for word in words:
        
        ts_ele = ts[ts_ind]
        ts_word = ts_ele['word'].lower().strip()

        if (word != ts_word):
            # print (ts_ind)
            # print (word.lower())
            # print (ts[ts_ind]['word'].lower())
            # print (ts[ts_ind]['start'])
            # return
            if (ts_ind+1 < len(ts)):
                ts_combined = ts_word + ts[ts_ind + 1]['word'].lower().strip()
                if (word == ts_combined.lower().strip()):
                    ts_ind += 1
                    ts_ele = {"word": ts_combined, "start": ts[ts_ind]['start'], "end": ts[ts_ind+1]['end']}
                else:
                    print (word)
                    print (ts_ele)
                    return False
            else:
                print ('not matched word', ts_ind)
                print (word)
                print (ts[ts_ind]['word'])
                print (ts[ts_ind]['start'])
                return False

        ts_modified.append (ts_ele)
        ts_ind += 1

    # if ts word left after comparison
    if (ts_ind < len(ts)):
        # if the left word is not K, i, ....
        if (len (ts[ts_ind]['word']) > 1):
            print ("ts left: ", ts[ts_ind]['word'])
            return False


    print ("all words matched")

    ts_word_length = len (ts_modified)
    script_word_length = len (words)
    if (ts_word_length == script_word_length):
        print ("number of words matched")
        print ("ts word number: ", ts_word_length)
        print ("script word number: ", script_word_length)

    else:
        print ("number of words NOT matched")
        print ("ts word number: ", ts_word_length)
        print ("script word number: ", script_word_length)

    return ts_modified

def match_script_ts (ws_dict, ts):
    script_modified = []

    ts_ind = 0
    for line in ws_dict:
        script = line['Script'].strip().split(' ')
        words_len = len (script)

        # print ('-' * 10)
        # print (line)
        # print (words_len)
        # print (ts_ind, ts_ind + words_len)
        # print (len(ts))

        ts_sentence = ts[ts_ind : ts_ind + words_len]
        ts_start = ts_sentence[0]
        ts_end = ts_sentence[-1]
        if (script[0].lower().strip() == ts_start['word'].lower().strip()):
            start = ts_sentence[0]['start']
        else:
            print (script)
            for tmp in ts_sentence:
                print (tmp['word']) 
            print ('start not matched')
            return False

        if (script[-1].lower().strip() == ts_end['word'].lower().strip()):
            end = ts_sentence[-1]['end']
        else:
            print (script)
            for tmp in ts_sentence:
                print (tmp['word']) 
            print ('end not matched')
            return False

        type = line['Final'].strip().lower()
        script_obj = {'start': start, 'end': end, 'script': line['Script'], 'type': type}
        script_modified.append (script_obj)

        ts_ind += words_len

    return script_modified

def write_json (fp, script):
    with open(fp, "w") as json_file:
        json.dump(script, json_file)


# add high level label
# delete unncessary info (early, late, optional, ...)
def process_matched_script (script):
    for line in script:

        type = line['type'].strip()
        
        # delete early, late
        if 'early' in type or 'late' in type:
            type = 'instruction'
        
        # delete multiple, optional
        if '(' in type:
            type = type.split ('(')[0].strip()


        if '\x08' in type:
            type = type.strip('\x08').strip()

        # print (type)
        # print (line)
        assert type in TYPES

        for cat in cat_hierarchy:
            if type in cat_hierarchy[cat]:
                category = cat

        assert category in CATEGORIES

        # add section
        for sec in section_hierarchy:
            if category in section_hierarchy[sec] or type in section_hierarchy[sec]:
                section = sec

        assert section in SECTIONS

        line['type'] = type
        line['category'] = category
        line['section'] = section

    return script   
        

def video_duration (path):
    audio = AudioSegment.from_file(path)
    audio.duration_seconds == (len(audio) / 1000.0)
    return audio.duration_seconds

def simplify_script (script, duration):
    for i, line in enumerate (script):
        low_label = line['low_label'].strip()
        if '(' in low_label:
            line['low_label'] = low_label.split ('(')[0].strip()
        elif 'tool specification' == low_label:
            line['low_label'] = 'tool spec.'

        if (i == len(script)-1):
            next_start = duration
        else:
            next_start = script[i+1]['start'] 
        line['next_start'] = next_start
        line['index'] = i

    return script   


### sentence count ###

def count_sentences (ws):
    return len (ws.get_all_values()) - 1

# get count of sentence
def get_sentence():
    total_count = 0
    for category in annotation_final_url_list.keys():
        print ('-' * 30)
        print (category)
        spreadsheet_url = annotation_final_url_list [category]
        doc = gc.open_by_url (spreadsheet_url)
        worksheet_list = doc.worksheets()

        cat_count = 0
        for i, ws in enumerate(worksheet_list):
            ws_count = count_sentences (ws)
            cat_count += ws_count
            print (ws.title, ':', ws_count)
            # if (i < 3) or ws.title in vids:
            #     ws_count = count_sentences (ws)
            #     cat_count += ws_count
            #     print (ws.title, ':', ws_count)

        print (category, ':', cat_count)
        # to solve api issue
        time.sleep (15)

        total_count += cat_count
    print ("total count: ", total_count)

if __name__ == "__main__":

    error_vids = []

    for category in annotation_final_url_list.keys():
        print ('*' * 30)
        print (category)
        spreadsheet_url = annotation_final_url_list [category]
        doc = gc.open_by_url (spreadsheet_url)
        worksheet_list = doc.worksheets()
        category_dir = ROOT_DIR + category + '/'

        save_category_dir = SAVE_DIR + category + '/'
        if not os.path.exists (SAVE_DIR + category):
            os.makedirs (SAVE_DIR + category)

        audio_category_dir = AUDIO_DIR + category + '/'
 
        for ws in worksheet_list:
            # if (ws.title in vids):
            if True:
                print ('-' * 30)
                print (ws.title)
                ws_dicts = ws.get_all_records()
                ts_path = category_dir + ws.title + '_ts.json'

                
                with open (ts_path, 'r') as t:
                    ts = json.load (t)
                
                ts_modified = check_script_ts (ws_dicts, ts)
                if (not ts_modified): 
                    error_vids.append (ws.title)
                    continue

                matched_script = match_script_ts (ws_dicts, ts_modified)
                if (not matched_script): 
                    error_vids.append (ws.title)
                    continue
                processed_script = process_matched_script (matched_script)


                save_fp = save_category_dir + ws.title + '.json'
                write_json (save_fp, processed_script)

            # simplified script version for interface
            # audio_path = audio_category_dir + ws.title + '.wav'
            # duration = round(video_duration (audio_path), 2)
            # simplifed_script = simplify_script (processed_script, duration)
            
            # simplified_save_fp = save_category_dir + ws.title + '(simplified).json'
            # write_json (simplified_save_fp, simplifed_script)

    print (error_vids)








