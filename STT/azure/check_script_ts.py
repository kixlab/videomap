######### this is for checking whether list of word with timestamp matches lexcial script ######

import json
import os

input_root = "./transcript/"    #script file path
save_root = "./final/"   #output file path
category_name = ['Arts and Entertainment', 'Cars & Other Vehicles', 'Computers and Electronics', 'Education and Communications', 'Food and Entertaining', 'Health', 'Hobbies and Crafts', 'Holidays and Traditions', 'Home and Garden', 'Personal Care and Style', 'Pets and Animals', 'Sports and Fitness']

# list of video id
# sel_vids = ['VEplLGXFLFw', '5AU2vJU-QJM', 'mwpb65gm1e0', 'T622Ec77ZPY', 'bg3orsnRCVE', 's4coMAU80U4', '-szevr-BRZE', '7IcOJEEObA0', 'WoDZQRGyuHA', 'VDMOFa8iRqo', '1Ni8KOzRzuI', 'kNsjE4HO7tE']
sel_vids = ['5AU2vJU-QJM']

# check whether word list and lexical script matches
def match_script_ts (cat_dir, vid):
    print (vid)
    fp = cat_dir + '/' + vid
    script_path = fp + '.json'
    ts_path = fp + '_ts.json'

    with open(script_path, 'r') as s:
        script= json.load(s)

    with open(ts_path, 'r') as t:
        ts = json.load(t)

    # parse lexical script into word
    words = []
    for segment in script:
        words_tmp = segment['segment'].split (' ')
        for word in words_tmp:
            if (word != ''):
                words.append (word)

    # 1. fist compare the length bw word list and decomposed script
    ts_word_length = len (ts)
    script_word_length = len (words)
    if (ts_word_length == script_word_length):
        print ("number of words matched")
        print ("ts word number: ", ts_word_length)
        print ("script word number: ", script_word_length)

    else:
        print ('XXXXXXX')
        print ("number of words NOT matched")
        print ("ts word number: ", ts_word_length)
        print ("script word number: ", script_word_length)

    # 2. compare one by one 
    ts_ind = 0
    for word in words:
        if (word.lower() != ts[ts_ind]['word'].lower()):
            print ('not matched word', ts_ind)
            print (word)
            print (ts[ts_ind]['word'])
            break
        ts_ind += 1
    print ("all words matched")


if __name__ == "__main__":
    for root, dirs, files in os.walk (input_root):
        for dir_name in dirs:
            print ('-' * 30)
            print ('directory :', dir_name)
            category_dir = input_root + dir_name
            save_category_dir = save_root + dir_name
            files = os.listdir(category_dir)
            for file in files:
                vid = file.split('.')[0]
                if vid in sel_vids:
                    match_script_ts (category_dir, vid)