import json
import os

input_root = "./transcript/"    #script file path
save_root = "./final/"   #output file path
category_name = ['Arts and Entertainment', 'Cars & Other Vehicles', 'Computers and Electronics', 'Education and Communications', 'Food and Entertaining', 'Health', 'Hobbies and Crafts', 'Holidays and Traditions', 'Home and Garden', 'Personal Care and Style', 'Pets and Animals', 'Sports and Fitness']

# list of video id
# vids = ['ZT1dvq6yacQ', 'h281yamVFDc', '2Xyfgwj92v0', 'z1Xv6Pa0toE', 'kPGwDxo5Yf4', 'ntYwKXN82QU', 'ZORD4y7dL08', 'AnWGek4P_dY', 'OcjCNqfRgP0', 'dJ_qCDWNvXU', '0TLQg_b1v5Q', 'jGsEBwiKnCI']

def change_sec_unit (input_time):
    return input_time / 10000000

## automatic punctuation으로 parse -> .을 기준으로 자르니 잘리지 말아야할 .도 삭제되어 word가 더 많아지는 경우가 생김
## manually modify하기 위해서 어떤 비디오, 어떤 부분에 그런 문제가 있는지 확인
def check_script_ts (cat_dir, vid):
    fp = cat_dir + '/' + vid
    script_path = fp + '.json'
    ts_path = fp + '_ts.json'
    ts_modified_path = fp + '_ts_modified.json'

    with open(script_path, 'r') as s:
        script= json.load(s)

    with open(ts_modified_path, 'r') as t:
        ts = json.load(t)

    # modified_ts = []
    # for t in ts:
    #     word = t['Word']
    #     start = round (change_sec_unit(t['Offset']), 3)
    #     end = round (change_sec_unit (t['Offset'] + t['Duration']), 3)
    #     t_obj = {"word" : word, 'start': start, 'end': end}
    #     modified_ts.append (t_obj)

    # with open (ts_modified_path, 'w') as t:
    #     json.dump (modified_ts, t)



    
    # ts_ind = 0
    # print (vid)
    # for s in script:
    #     print (s['sentence'])
    #     sentence = s['sentence'].split(' ')

    #     for word in sentence:
    #         # print ('w: ', word)
    #         # word에서 마지막이 . 이면 이전 부분만 사용
    #         if (len (word) == 0):
    #             ts_ind += 1
    #             continue

    #         if (word[-1] == '.' or word[-1] == ',' or word[-1] == '?'):
    #             word = word[:-1]
    #         # print ('w: ', word)
            
    #         word_ts = ts[ts_ind]['Word']
    #         # ts의 단어와 script의 단어가 다를 경우
    #         if (word.strip().lower() != word_ts.strip().lower()):
    #             # .com처럼 dot이 포함되어 있는 경우
    #             if ('.' in word):
    #                 word_ts = ts[ts_ind]['Word'] + '.' + ts[ts_ind + 2]['Word']
    #                 if (word.strip().lower() == word_ts.strip().lower()):
    #                     ts_ind += 2
    #                 else:
    #                     print ('wrong sentence: ', s)
    #                     print ('word: ', word)
    #                     print ('word_ts:', word_ts)
    #                     return
    #             else:
    #                 print ('wrong sentence: ', s)
    #                 print ('word: ', word)
    #                 print ('word_ts:', word_ts)
    #                 return
    #         else:
    #             ts_ind += 1


    
    ts_ind = 0
    start_ts = []
    end_ts = []
    print (vid)
    for s in script:
        print (s['sentence'])
        sentence = s['sentence'].split(' ')

        # modify each word without empty space and with lower cass
        # cut the last character if it is . / , / ?
        modified_sentence = []
        for word in sentence:
            word = word.strip().lower()
            if (word[-1] == '.' or word[-1] == ',' or word[-1] == '?'):
                word = word[:-1]

            modified_sentence.append (word)

        if (len (modified_sentence) == 0):
            continue

        start_word = modified_sentence[0]
        end_word = modified_sentence[-1]
    
        start = 0
        end = 0

        current_ts = ts[ts_ind]
        if (start_word == current_ts['word'].strip().lower()):
            start = current_ts['start']
            start_ts.append (start)
            print ('-' * 20,  'matched')
            print (current_ts)
            print (start_word)
        else:
            print ("start not matched")
            print (current_ts)
            print (start_word)
            return

        # if (len (modified_sentence) > 1):
        #     ts_ind += 1
        ts_ind += len (modified_sentence) - 1

        while (True):
            current_ts = ts[ts_ind]
            if (end_word == current_ts['word'].strip().lower()):
                end = current_ts['end']
                end_ts.append (end)
                break
            else:
                ts_ind += 1
        
        ts_ind += 1

        print (start_ts)
        print (end_ts)



        # for ind, word in enumerate (sentence):
        #     # print ('w: ', word)
        #     # word에서 마지막이 . 이면 이전 부분만 사용
        #     if (len (word) == 0):
        #         ts_ind += 1
        #         continue

        #     if (word[-1] == '.' or word[-1] == ',' or word[-1] == '?'):
        #         word = word[:-1]
        #     # print ('w: ', word)

        #     word_ts = ts[ts_ind]['word']
        #     if (ind == 0):
        #         if (word.strip().lower() != word_ts.strip().lower()):
        #             start = word_ts['start']
        #             ts_ind += 1
        #             continue
        #         else:
        #             print ("start not matched")
        #             return

        #     while ((word.strip().lower() != word_ts.strip().lower()) or word != ):
        #         ts_ind += 1
            
        #     if (word.strip().lower() != word_ts.strip().lower()):
        #         ts_ind += 1
        #         continue
        #     else:


        #     if (word.strip().lower() != word_ts.strip().lower()):

        #     # ts의 단어와 script의 단어가 다를 경우
        #     if (word.strip().lower() != word_ts.strip().lower()):
        #         # .com처럼 dot이 포함되어 있는 경우
        #         if ('.' in word):
        #             word_ts = ts[ts_ind]['Word'] + '.' + ts[ts_ind + 2]['Word']
        #             if (word.strip().lower() == word_ts.strip().lower()):
        #                 ts_ind += 2
        #             else:
        #                 print ('wrong sentence: ', s)
        #                 print ('word: ', word)
        #                 print ('word_ts:', word_ts)
        #                 return
        #         else:
        #             print ('wrong sentence: ', s)
        #             print ('word: ', word)
        #             print ('word_ts:', word_ts)
        #             return
        #     else:
        #         ts_ind += 1

    # print ("Match")
    # print ("-" * 30)


                    
def modify_script_with_ts (category, vid):    
    fp = input_root + category + '/' + vid

    script_path = fp + '.json'
    ts_path = fp + '_ts.json'

    with open(script_path, 'r') as s:
        script= json.load(s)

    with open(ts_path, 'r') as t:
        ts = json.load(t)

    modified_script = []
    script_len = 0
    for s in script:
        text = s['sentence']
        sentence = text.split(' ')
        sentence_len = len (sentence)
        sentence_ts = ts[script_len : script_len + sentence_len]
        script_len += sentence_len
        start = sentence_ts[0]['Offset']
        end = sentence_ts[-1]['Offset'] + sentence_ts[-1]['Duration']

        sen_obj = {'text': text, 'start': start, 'end': end}
        modified_script.append (sen_obj)

    return modified_script



if __name__ == "__main__":
    vids = ['OcjCNqfRgP0']
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
                    check_script_ts (category_dir, vid)

