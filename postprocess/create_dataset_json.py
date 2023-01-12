### Aggregate every file into one json dataset.
### Before run this code, postprocessing should be done with postprocess.py 
### and all data should be stored in ./data/processed/ with ./data/processed/{category}/{video id}.json format

import os
import json
from pydub import AudioSegment

# manually added....
# vid: production date
date_dict = {'mZZJYDfmgeg': '20180815', 'XN3N5K2axpw': '20180510', 'WIIjq2GexIw': '20170203', '1oiCLxngvBo': '20190117', 'ZT1dvq6yacQ': '20170117', 'PyWZYHy17As': '20180927', 'uUBVc8Ugz0k': '20170829', 'Nu_By3eTpoc': '20170717', 'ZeVRqW2J3UY': '20170326', 'u00iLnvVgFc': '20190207', '2OoebJA2mnE': '20180703', '-xCtbeecgKQ': '20180620', '-6tnn1G1dRg': '20180518', 'z1Xv6Pa0toE': '20180514', 'T622Ec77ZPY': '20180504', '9mjXFA1TMTI': '20180414', 'jhAklPzn0XQ': '20180425', 'QzS7Z80poKo': '20180804', 'bwxvH99sLqw': '20180217', 'mUq6l7N6zuk': '20180426', '0SMzqWV6xxs': '20180724', '_Yb6xLqvsf0': '20180425', 'nnzPJv5XIws': '20171028', 'ZORD4y7dL08': '20170815', '-szevr-BRZE': '20170715', 'KLLqGcgxQEw': '20170531', 'Czi_ZirnzRo': '20170307', 'GFd7kLvhc2Q': '20170304', '73lxEIKyX8M': '20170217', 'eDG1c6a6uqc': '20170520', 'Rcsy2HRuiyA': '20180130', 'Ag6D8RGQnjw': '20180725', 'CxdRXDN1fkA': '20180710', 'dJ_qCDWNvXU': '20171204', 'VDMOFa8iRqo': '20171113', 'mQjCKgEPs8k': '20170711', 'BzxPDw6ezEc': '20170623', 'pn81__TovpY': '20170103', 'ZmTxw3UbMO4': '20170508', 'kz5dJ9SCu4M': '20170419', 'yJ7VzfG2ONo': '20180515', 'JNznnqX6SsE': '20190205', 'dKUomyn1TYQ': '20190121', 'h281yamVFDc': '20190116', '5AU2vJU-QJM': '20190115', 'yYOysPt5gic': '20190111', '6CJryveLzvI': '20181221', 'ZY11rbwCaMM': '20181219', 'xTARWxkTJw0': '20180203', 'WcD8bG2VB_s': '20180919', 'ta5IB2wy6ic': '20170302', 'rqBiByEbMHc': '20170327', '5ywy531EMNA': '20181004', 'sM81wJ7GDrI': '20170531', '0TLQg_b1v5Q': '20170405', '1Ni8KOzRzuI': '20170526', 'Vrz25x3qnTY': '20170724', 'sij_wNj0doI': '20170830', 'BotYnPhByWg': '20171005', 'djvLEfwwQPU': '20170613', 'A_qivvTkijw': '20190214', 'S0luUzNRtq0': '20190130', 'eyD2iwXOeFM': '20190123', 'kPGwDxo5Yf4': '20180822', 'bg3orsnRCVE': '20180817', 'HFp5uH12wkc': '20180816', 'Xh_Awznyc7s': '20180805', 'cGn_oZPotZA': '20180218', 'ynmdOz_D1R4': '20190213', 'yu-G9kEKdTo': '20180504', 'Cvv1wiqKMHc': '20170909', 'EnjZHOb6qNE': '20170705', 'r6JmI35r5E8': '20170603', 'AnWGek4P_dY': '20170114', '7IcOJEEObA0': '20170202', '-wlSMSl02Xs': '20171124', 'IICwmc4WX2E': '20170212', 'Eeu5uL6r2rg': '20170325', 'k0koOhfXv_s': '20170307', '4WaXJs9RR3E': '20170625', 'tb1L7Rsm1U8': '20180314', 'T1j7Yq5-cIs': '20190208', 'ihCwjLj31hY': '20190203', '2Xyfgwj92v0': '20190203', 'mwpb65gm1e0': '20190128', 'oe7Cz-dxSBY': '20190124', 'zMqzjMrxNR0': '20190120', 'UZJ0nmB3epQ': '20190116', 'T5MbMuoNQ1k': '20190218', '0fxL8v2dMho': '20181228', '8DgsLNa3ums': '20170518', 'N3c81EPZ51Q': '20170517', 'e3StC_4qemI': '20170415', 'ntYwKXN82QU': '20170327', 's4coMAU80U4': '20170326', '7oXrT1CqLCY': '20170220', 'uMgpr6X5asI': '20170126', 'AbhW9YbQ0fM': '20170124', 'bQKTjz0JKhg': '20170119', 'SXQHgJHYQgc': '20170105', 'Df9F8ettY8k': '20190115', 'ntwi2Unh3JQ': '20181001', 'ysHg9vOMe_4': '20181230', 'OcjCNqfRgP0': '20180810', 'WoDZQRGyuHA': '20180210', 'wvC3_Rs4mXs': '20171201', 'bxXXCP0AE5A': '20171003', '2xXPSfQBP-w': '20170911', 'yeT52sDtYEU': '20170630', 'Y84sqS2Nljs': '20180924', 'XFYHIg8U--4': '20180717', 'm0H56KpKLHA': '20180708', '1dALzTPQWJg': '20180524', 'ygRQRgR11Zg': '20180121', 'jGsEBwiKnCI': '20180523', 'kNsjE4HO7tE': '20180315', 'mj1Fu3-XQpI': '20171218', 'CdZQF4DDAxM': '20171115', 'UriwETsgsqg': '20170923', 'b2EZggyT5O4': '20170410'}

# ----------------------------------------------------#
# --------------- Helper functions -------------------#
# ----------------------------------------------------#

def read_json (fp):
    with open (fp, 'r') as s:
        script = json.load (s)
    return script

def write_json (fp, script):
    with open(fp, "w") as json_file:
        json.dump(script, json_file)

def video_duration (path):
    audio = AudioSegment.from_file(path)
    audio.duration_seconds == (len(audio) / 1000.0)
    return round(audio.duration_seconds, 2)

TYPES = {'opening', 'closing', 'goal', 'motivation', 'briefing', 'subgoal', 'instruction', 'tool', 'warning', 'tip', 'justification', 'effect', 'status', 'context', 'tool specification', 'outcome', 'reflection', 'side note', 'self-promo', 'bridge', 'filler'}
CATEGORIES = {'greeting', 'overview', 'method', 'supplementary', 'explanation', 'description', 'conclusion', 'miscellaneous'}
SECTIONS = {'intro', 'procedure', 'outro', 'miscellaneous'}

# modify script (e.g. step->method, strip, ..)
def modify_script (data):
    for line in data:
        line['script'] = line['script'].strip()
        line['type'] = line['type'].strip()
        line['category'] = line['category'].strip()
        # line['section'] = line['section'].strip()
        del line['section']

        if line['category'] == 'step':
            line['category'] = 'method'

        if line['category'] == 'misc.':
            line['category'] = "miscellaneous"

        # if line['section'] == 'misc.':
        #     line['section'] = 'miscellaneous'

    return data

# check whether all labels are correct
def check_validity (data):
    for line in data:
        assert line['type'] in TYPES
        assert line['category'] in CATEGORIES
        # assert line['section'] in SECTIONS


ROOT_DIR = './data/processed/'
SAVE_DIR ='./data/dataset/'
AUDIO_DIR = './data/audio/'

if __name__ == "__main__":

    dataset = []
    count = 0
    for root, dirs, files in os.walk (ROOT_DIR):
        for dir_name in dirs:
            print ('*' * 30)
            print (dir_name)

            cat_dir = os.path.join (ROOT_DIR, dir_name) 
            audio_cat_dir = os.path.join (AUDIO_DIR, dir_name)

            files = os.listdir(cat_dir)
            for file in files:
                vid = file.split('.')[0]
                print (vid)
                fp = os.path.join (cat_dir, file)
                audio_fp = os.path.join (audio_cat_dir, vid+'.wav')

                script_data = read_json (fp)
                script_data = modify_script(script_data)
                check_validity (script_data)

                duration = video_duration (audio_fp)

                fixed_script = {}
                fixed_script['id'] = vid
                fixed_script['publication_date'] = date_dict[vid]
                fixed_script['genre'] = dir_name
                fixed_script['duration'] = duration
                fixed_script['data'] = script_data
                dataset.append (fixed_script)
                count+=1

    print (count)
    write_json(SAVE_DIR+'HTM-TYPE_new.json', dataset)
