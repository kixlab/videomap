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

# video lists in each date
# vids_0805 = ['ZT1dvq6yacQ', 'h281yamVFDc', '2Xyfgwj92v0', 'z1Xv6Pa0toE', 'kPGwDxo5Yf4', 'ntYwKXN82QU', 'ZORD4y7dL08', 'AnWGek4P_dY', 'OcjCNqfRgP0', 'dJ_qCDWNvXU', '0TLQg_b1v5Q', 'jGsEBwiKnCI']
# vids_0808 = ['VEplLGXFLFw', '5AU2vJU-QJM', 'mwpb65gm1e0', 'T622Ec77ZPY', 'bg3orsnRCVE', 's4coMAU80U4', '-szevr-BRZE', '7IcOJEEObA0']
# vids_0809 = ['WoDZQRGyuHA', 'VDMOFa8iRqo', '1Ni8KOzRzuI', 'kNsjE4HO7tE', 'EYL1tYGwYY0', 'yYOysPt5gic', 'oe7Cz-dxSBY', '9mjXFA1TMTI']
# vids_0810 = ['HFp5uH12wkc', '7oXrT1CqLCY', 'KLLqGcgxQEw', '-wlSMSl02Xs', 'wvC3_Rs4mXs', 'mQjCKgEPs8k', 'sM81wJ7GDrI', 'ygRQRgR11Zg']
# vids_0811 = ['uUBVc8Ugz0k', '6CJryveLzvI', 'zMqzjMrxNR0', 'jhAklPzn0XQ', 'Xh_Awznyc7s', 'uMgpr6X5asI', 'Czi_ZirnzRo', 'IICwmc4WX2E']
# vids_0812 = ['bxXXCP0AE5A', 'BzxPDw6ezEc', 'Vrz25x3qnTY', 'mj1Fu3-XQpI', 'Nu_By3eTpoc', 'ZY11rbwCaMM', 'UZJ0nmB3epQ', 'QzS7Z80poKo', 'jHsbUTwIl1A', 'AbhW9YbQ0fM']
# vids_0814 = ['GFd7kLvhc2Q', 'Eeu5uL6r2rg', '2xXPSfQBP-w', 'pn81__TovpY', 'sij_wNj0doI', 'CdZQF4DDAxM', 'ZeVRqW2J3UY', 'xTARWxkTJw0', '8cV5x4jP7EU', 'bwxvH99sLqw']
# vids_0815 = ['cGn_oZPotZA', 'bQKTjz0JKhg', '73lxEIKyX8M', 'k0koOhfXv_s', 'yeT52sDtYEU', 'ZmTxw3UbMO4', 'BotYnPhByWg', 'UriwETsgsqg', 'PyWZYHy17As', 'WcD8bG2VB_s']
# vids_0816 = ['0fxL8v2dMho', 'mUq6l7N6zuk', 'yu-G9kEKdTo', 'SXQHgJHYQgc', 'eDG1c6a6uqc', '4WaXJs9RR3E', 'Y84sqS2Nljs', 'kz5dJ9SCu4M', 'djvLEfwwQPU', 'b2EZggyT5O4']

# video list for creation
# vids_creation_1 = ['mZZJYDfmgeg', 'XN3N5K2axpw', 'WIIjq2GexIw', '2OoebJA2mnE', '-xCtbeecgKQ', '-6tnn1G1dRg', '0SMzqWV6xxs', '_Yb6xLqvsf0', 'nnzPJv5XIws', 'Rcsy2HRuiyA', 'Ag6D8RGQnjw', 'CxdRXDN1fkA']
# vids_creation_2 = ['yJ7VzfG2ONo', 'JNznnqX6SsE', 'dKUomyn1TYQ', 'A_qivvTkijw', 'S0luUzNRtq0', 'eyD2iwXOeFM', 'Cvv1wiqKMHc', 'EnjZHOb6qNE', 'r6JmI35r5E8', 'ta5IB2wy6ic', 'rqBiByEbMHc', '2YGEDsl7PO8']
# vids_creation_3 = ['tb1L7Rsm1U8', 'T1j7Yq5-cIs', 'ihCwjLj31hY', '8DgsLNa3ums', 'N3c81EPZ51Q', 'e3StC_4qemI', 'Df9F8ettY8k', 'ntwi2Unh3JQ', 'ysHg9vOMe_4', 'XFYHIg8U--4', 'm0H56KpKLHA', '1dALzTPQWJg']

new_vids = ['YmHGiLGINV4', 'u00iLnvVgFc', 'cvZMHEu_Ojk', '1oiCLxngvBo', 'mmGVeV-BvhU']
# input : list of text segments, timestamp for words
# output : list of object with text, start, end
# assertion : each word in text segments and words should be 1 to 1 matched
def ts_for_sentence (text_segments, ts_words):
    start = 0
    end = 0

    sentence_with_timestamp = []
    ts_ind = 0
    for text in text_segments:
        words = text.split (' ')
        words_len = len (words)

        ts_sentence = ts_words[ts_ind:ts_ind + words_len]
        # print (words)
        # print (ts_sentence)

        if (words_len != len (ts_sentence)):
            print ('length not matched')

        ts_start = ts_sentence[0]
        ts_end = ts_sentence[-1]
        if (words[0].lower() == ts_start['word'].lower()):
            start = ts_sentence[0]['start']
        else:
            print (words)
            for tmp in ts_sentence:
                print (tmp['word']) 
            print ('start not matched')
            return

        if (words[-1].lower().strip() == ts_end['word'].lower().strip()):
            end = ts_sentence[-1]['end']
        else:
            print ('-' * 30)
            print (words)
            print (ts_sentence)
            print (words[-1])
            print (ts_end['word'])
            print (words[-1] == ts_end['word'])
            # for tmp in ts_sentence:
            #     print (tmp['word']) 
            print ('end not matched')
            return

        # start = ts_words[ts_ind]['start']
        # end = ts_words[ts_ind + words_len - 1]['end']

        text_obj = {'sentence' : text, 'start': start, 'end': end}
        sentence_with_timestamp.append (text_obj)

        ts_ind += words_len
    print ("all matched")

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

    # preprocessing for removing space before '
    # e.g. doesn 't -> doesn't

    for ind, word_ts in enumerate(ts):
        if ("'" == word_ts['word'][0]):
            if (ind > 0):
                # print ("*" * 30)
                # print ("preprocessing for ", word_ts['word'])
                ts[ind-1]['word'] += word_ts['word']
                ts[ind-1]['end'] = word_ts['end']
                del ts[ind]     


    # preprocess to use sentencify module
    text_segments = [s['segment'] for s in script]

    # automatic punctuation model
    processor = Sentencify()
    punctuated_sentences, _, _ = processor.punctuate_and_cut (text_segments)
    print ("automatic punctuation complete")
    print ('-' * 30)

    # manual processing for eliminating split of '
    # e.g. doesn't -> doesn / 't, I'm -> I / 'm
    for ind, ps in enumerate (punctuated_sentences):
        ps_first = ps.strip().split(' ')[0]
        if ("'" == ps_first[0]):
            if (ind > 0):
                print ('*' * 20)
                print ("post processing for ' : ", ps)
                punctuated_sentences[ind-1] += ps_first
                punctuated_sentences[ind] = punctuated_sentences[ind][len (ps_first) :].strip()
                if (len (punctuated_sentences[ind]) == 0):
                    del punctuated_sentences[ind]

    # for p in punctuated_sentences:
    #     print (p)  

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
                if vid in new_vids:
                    sentences = process_script_ts (category_dir, vid)
                    save_fp = save_category_dir + '/' + vid + '.json'
                    write_json (save_fp, sentences)