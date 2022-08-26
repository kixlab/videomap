import os
import json
from re import L
import gspread
from gspread.cell import Cell
from oauth2client.service_account import ServiceAccountCredentials

# -------------------------------------- #
# upload stt results for annotating study #
# -------------------------------------- #

ROOT_DIR = './data/transcript/'
SAVE_DIR = './data/processed/'

type_hierarchy = {
    "greeting": ["opening", "closing"],
    "overview": ["goal", "motivation", "briefing"],
    "step": ["subgoal", "instruction", "tool"],
    "supplementary": ["warning", "tip"],
    "explanation": ["justification", "effect"],
    "description": ["status", "context"],
    "conclusion": ["outcome", "reflection"],
    "misc.": ["side note", "self-promo", "bridge", "filler"]
}

# annotation folder sheet url
annotation_url_list = {
    "Arts and Entertainment" : "https://docs.google.com/spreadsheets/d/1J2MGMJV6IzPbbk3977qkPrAn3oPvP9Seijnhv_q6T3o/edit#gid=0",
    "Cars & Other Vehicles" : "https://docs.google.com/spreadsheets/d/1z-69U6L64xeSs0hYCzbKaeHUdyaLkL96_adbuqiJgAU/edit#gid=0",
    "Computers and Electronics" : "https://docs.google.com/spreadsheets/d/1hJssaIb1UUsU1oIKo_f9y0yKpJZs4sOE2Xnn0xrGvJg/edit#gid=0",
    "Education and Communications" : "https://docs.google.com/spreadsheets/d/147OH4e32Cq_Ck1tchfSaqlXDqOtbe8UoGKlm2NIv-CI/edit#gid=0",
    "Food and Entertaining" : "https://docs.google.com/spreadsheets/d/1Ol9vbQbs7r9WdKIyfSxHPf4uMJnbz5HM9q9ycvlJlcs/edit#gid=0",
    "Health" : "https://docs.google.com/spreadsheets/d/1Ggy4xg6vHXjoXwdI2KyRWnbPhMa_9XZKpVA5Won5FME/edit#gid=0",
    "Hobbies and Crafts" : "https://docs.google.com/spreadsheets/d/18ncJdLNYhU_5pjHraUEmTmOj0z7az2PXJTIcBTM4Qao/edit#gid=0",
    "Holidays and Traditions" : "https://docs.google.com/spreadsheets/d/11FtXuT3EVHa_Dnl5dQ4L2HWS9kEbNKgMWo3oIyjT07Y/edit#gid=0",
    "Home and Garden" : "https://docs.google.com/spreadsheets/d/1SFRBrJihrQvbOoIVdFiSBAHAZRgHQ60serfe8ab58o4/edit#gid=0",
    "Personal Care and Style" : "https://docs.google.com/spreadsheets/d/1MdYGz2gVMd6-_Oor_NhQEMYDCLNQLB7uj_hEOkPoJLA/edit#gid=0",
    "Pets and Animals" : "https://docs.google.com/spreadsheets/d/1m9e0m-Tcgn2eG2i4u6aYP3VJCY7i_bJ7KOzvgIZj2NA/edit#gid=0",
    "Sports and Fitness" : "https://docs.google.com/spreadsheets/d/1Ks9TvkliBd_D-MNfEq2tlQQWxFDQ9mZNcp951or1O8Q/edit#gid=0",
    "Tutorial": "https://docs.google.com/spreadsheets/d/17X9jVbUvmzptkdf_WnLdizXKm2yLFXY4Dtdv27RaABw/edit#gid=0",
}

# creation folder sheet url
creation_url_list = {
    "Arts and Entertainment" : "https://docs.google.com/spreadsheets/d/1ph_wb_kCzhBR6lRyyv1dNyKc1XSf08lXpYFW72E5vxY/edit#gid=0",
    "Cars & Other Vehicles" : "https://docs.google.com/spreadsheets/d/1lQp0oLgORhVes3v7PIs5RZhYQ4d1mMM169YdTqDTn5w/edit#gid=0",
    "Computers and Electronics" : "https://docs.google.com/spreadsheets/d/1lkdoBQLMdKAJQfgvW0S7V1dVUQ_VdMRTLxBc91HWH2s/edit#gid=0",
    "Education and Communications" : "https://docs.google.com/spreadsheets/d/1y7BSPcDSHP9rpy4KhTfT60PDPE1d6QHVYWZnDKRUkcA/edit#gid=0",
    "Food and Entertaining" : "https://docs.google.com/spreadsheets/d/1mfM4WlbLiMvNYZ3cOK3uW9STZrfNVMfn6A1KKhDDOzU/edit#gid=0",
    "Health" : "https://docs.google.com/spreadsheets/d/1Xj8_efKCi1gYPqV3pTKXzZQ6fSfNdrNzX2T0Nps8sD0/edit#gid=0",
    "Hobbies and Crafts" : "https://docs.google.com/spreadsheets/d/1kuCAeJpCUrYbYxkMnFEA_dr4nudRhy9s1Js4K3mAhI4/edit#gid=0",
    "Holidays and Traditions" : "https://docs.google.com/spreadsheets/d/1P4-bZtp-UTYV7xO-LK0xgWLNV4PAD-uc-CuYUX_B3Yc/edit#gid=0",
    "Home and Garden" : "https://docs.google.com/spreadsheets/d/1V_HVlxXqD0-GBSMlWsU3vMHlF1F6CUVIoH2YLxC4p0A/edit#gid=0",
    "Personal Care and Style" : "https://docs.google.com/spreadsheets/d/1QqUL7U_AkEG4lqX2NJVn4KqFBdaJnGR5Bdunmf_0GbU/edit#gid=0",
    "Pets and Animals" : "https://docs.google.com/spreadsheets/d/1Hoy8pIOGqSlaj1OxYhq8nyqxUT37Ke62s8lBUzp1xF4/edit#gid=0",
    "Sports and Fitness" : "https://docs.google.com/spreadsheets/d/14yvQZPG3dHeoZvnP_D1hEVxjciakYGcMCWJw0u0H5XE/edit#gid=0",
}

vids = ['GFd7kLvhc2Q', 'Eeu5uL6r2rg', '2xXPSfQBP-w', 'pn81__TovpY', 'sij_wNj0doI', 'CdZQF4DDAxM']

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
        words_tmp = line['Script'].split (' ')
        for word in words_tmp:
            if (word != ''):
                words.append (word)


    ts_ind = 0
    ts_modified = []
    for word in words:
        ts_ele = ts[ts_ind]
        if (word.lower() != ts[ts_ind]['word'].lower()):
            if (ts_ind+1 < len(ts)):
                ts_combined = ts[ts_ind]['word'] + ts[ts_ind + 1]['word']
                if (word.lower() == ts_combined.lower()):
                    ts_ind += 1
                    ts_ele = {"word": ts_combined, "start": ts[ts_ind]['start'], "end": ts[ts_ind+1]['end']}
            else:
                print ('not matched word', ts_ind)
                print (word)
                print (ts[ts_ind]['word'])
                return
        ts_modified.append (ts_ele)
        ts_ind += 1

    # if ts word left after comparison
    if (ts_ind != len(ts)):
        if (len (ts[ts_ind]['word']) > 1):
            print ("ts left: ", ts[ts_ind]['word'])
            return


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

        ts_sentence = ts[ts_ind : ts_ind + words_len]
        ts_start = ts_sentence[0]
        ts_end = ts_sentence[-1]
        if (script[0].lower() == ts_start['word'].lower()):
            start = ts_sentence[0]['start']
        else:
            print (script)
            for tmp in ts_sentence:
                print (tmp['word']) 
            print ('start not matched')
            return

        if (script[-1].lower().strip() == ts_end['word'].lower().strip()):
            end = ts_sentence[-1]['end']
        else:
            print ('-' * 30)
            print (script)
            for tmp in ts_sentence:
                print (tmp['word']) 
            print ('end not matched')
            return

        low_label = line['Final']
        for type in type_hierarchy:
            if low_label in type_hierarchy[type]:
                high_label = type
        script_obj = {'start': start, 'end': end, 'script': line['Script'], 'low_label': low_label, 'high_label': high_label}
        script_modified.append (script_obj)

        ts_ind += words_len

    # print (script_modified)
    return script_modified

def write_json (fp, script):
    with open(fp, "w") as json_file:
        json.dump(script, json_file)


if __name__ == "__main__":
    for category in annotation_url_list.keys():
        print ('-' * 30)
        print (category)
        spreadsheet_url = annotation_url_list [category]
        doc = gc.open_by_url (spreadsheet_url)
        worksheet_list = doc.worksheets()
        category_dir = ROOT_DIR + category + '/'

        save_category_dir = SAVE_DIR + category + '/'
        if not os.path.exists (SAVE_DIR + category):
            os.makedirs (SAVE_DIR + category)
 
        for ws in worksheet_list:
            if (ws.title in vids):
                print (ws)
                ws_dicts = ws.get_all_records()

                ts_path = category_dir + ws.title + '_ts.json'
                with open (ts_path, 'r') as t:
                    ts = json.load (t)
                
                ts_modified = check_script_ts (ws_dicts, ts)
                processed_script = match_script_ts (ws_dicts, ts_modified)
                
                save_fp = save_category_dir + ws.title + '.json'
                write_json (save_fp, processed_script)






