######### this is for checking whether list of word with timestamp matches lexcial script ######

import json
import os

input_root = "./transcript/"    #script file path
save_root = "./final/"   #output file path
category_name = ['Arts and Entertainment', 'Cars & Other Vehicles', 'Computers and Electronics', 'Education and Communications', 'Food and Entertaining', 'Health', 'Hobbies and Crafts', 'Holidays and Traditions', 'Home and Garden', 'Personal Care and Style', 'Pets and Animals', 'Sports and Fitness']


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

# new_vids = ['YmHGiLGINV4', 'u00iLnvVgFc', 'cvZMHEu_Ojk', '1oiCLxngvBo', 'mmGVeV-BvhU']
new_vids = ['T5MbMuoNQ1k', 'ynmdOz_D1R4']

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
            return
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
                if vid in new_vids:
                    match_script_ts (category_dir, vid)