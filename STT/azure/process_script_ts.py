######### 
# This is for processing raw lexical script and word timestamps 
# Using sentencify module in TAN, generate auto punctuation in lexical segments and add timestamps for each sentence
#########

import json
import os
from filters.sentencify import Sentencify

input_root = "./transcript/"    #script file path
save_root = "./final/"   #output file path

# category_names = ['Arts and Entertainment', 'Cars & Other Vehicles', 'Computers and Electronics', 'Education and Communications', 'Food and Entertaining', 'Health', 'Hobbies and Crafts', 'Holidays and Traditions', 'Home and Garden', 'Personal Care and Style', 'Pets and Animals', 'Sports and Fitness']

# list of video id
# vids = ['5AU2vJU-QJM', 'mwpb65gm1e0', 'T622Ec77ZPY', 'bg3orsnRCVE', 's4coMAU80U4', '-szevr-BRZE', '7IcOJEEObA0', 'WoDZQRGyuHA', 'VDMOFa8iRqo', '1Ni8KOzRzuI', 'kNsjE4HO7tE']
vids = ['VDMOFa8iRqo']

# input : list of text segments, timestamp for words
# output : list of object with text, start, end
# assertion : each word in text segments and words should be 1 to 1 matched
def ts_for_sentence (text_segments, ts_words):
    start = 0
    end = 0

    sentence_with_timestamp = []
    ts_ind = 0
    for text in text_segments:

        words_len = len (text.split(' '))
        start = ts_words[ts_ind]['start']
        end = ts_words[ts_ind + words_len - 1]['end']

        text_obj = {'sentence' : text, 'start': start, 'end': end}
        sentence_with_timestamp.append (text_obj)

        ts_ind += words_len

    return sentence_with_timestamp


# check whether word list and lexcial script matches
def process_script_ts (cat_dir, vid):
    print (vid)
    fp = cat_dir + '/' + vid
    script_path = fp + '.json'
    ts_path = fp + '_ts.json'

    with open(script_path, 'r') as s:
        script= json.load(s)

    with open(ts_path, 'r') as t:
        ts = json.load(t)


    # preprocess to use sentencify module
    text_segments = [s['segment'] for s in script]
    print (text_segments)

    # start_timestamps = [s['start'] for s in sentence_with_timestamp]
    # end_timestamps = [s['end'] for s in sentence_with_timestamp]

    # automatic punctuation model
    processor = Sentencify()
    punctuated_sentences, _, _ = processor.punctuate_and_cut (text_segments)
    print ("automatic punctuation complete")

    sentence_with_timestamp = ts_for_sentence (punctuated_sentences, ts)
    return sentence_with_timestamp

def write_json (fp, script):
    with open(fp, "w") as json_file:
        json.dump(script, json_file)




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
                if vid in vids:
                    sentences = process_script_ts (category_dir, vid)
                    save_fp = save_category_dir + '/' + vid + '.json'
                    write_json (save_fp, sentences)