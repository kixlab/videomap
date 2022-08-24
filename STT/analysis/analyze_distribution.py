from importlib.metadata import distribution
import os
import json
from pydub import AudioSegment
import operator

# newly selected videos to check time distribution
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

# # video list for creation
# vids_creation_1 = ['mZZJYDfmgeg', 'XN3N5K2axpw', 'WIIjq2GexIw', '2OoebJA2mnE', '-xCtbeecgKQ', '-6tnn1G1dRg', '0SMzqWV6xxs', '_Yb6xLqvsf0', 'nnzPJv5XIws', 'Rcsy2HRuiyA', 'Ag6D8RGQnjw', 'CxdRXDN1fkA']
# vids_creation_2 = ['yJ7VzfG2ONo', 'JNznnqX6SsE', 'dKUomyn1TYQ', 'A_qivvTkijw', 'S0luUzNRtq0', 'eyD2iwXOeFM', 'Cvv1wiqKMHc', 'EnjZHOb6qNE', 'r6JmI35r5E8', 'ta5IB2wy6ic', 'rqBiByEbMHc', '2YGEDsl7PO8']
# vids_creation_3 = ['tb1L7Rsm1U8', 'T1j7Yq5-cIs', 'ihCwjLj31hY', '8DgsLNa3ums', 'N3c81EPZ51Q', 'e3StC_4qemI', 'Df9F8ettY8k', 'ntwi2Unh3JQ', 'ysHg9vOMe_4', 'XFYHIg8U--4', 'm0H56KpKLHA', '1dALzTPQWJg']

# vids_annotation = vids_0805 + vids_0808 + vids_0809 + vids_0810 + vids_0811 + vids_0812 + vids_0814 + vids_0815 + vids_0816
# vids_creation = vids_creation_1 + vids_creation_2 + vids_creation_3

# vids_total = vids_annotation + vids_creation

# new_vids = ['YmHGiLGINV4', 'u00iLnvVgFc', 'cvZMHEu_Ojk', '1oiCLxngvBo', 'mmGVeV-BvhU']
new_vids = ['T5MbMuoNQ1k', 'ynmdOz_D1R4']

def video_duration (path):
    audio = AudioSegment.from_file(path)
    audio.duration_seconds == (len(audio) / 1000.0)
    return audio.duration_seconds

# get time distribution w/ narration and w/o narration
def get_time_distribution ():
    return 0

script_root = './../azure/final'
audio_root = './../audio'
distribution_result = []

if __name__ == "__main__":
    for root, dirs, files in os.walk (script_root):
        for dir_name in dirs:
            print ('-' * 30)
            print('directory :', dir_name) #category
            category_dir = script_root + "/" + dir_name
            audio_category_dir = audio_root + "/" + dir_name
            files = os.listdir(category_dir)
            for file in files:
                vid = file.split('.')[0]
                if vid in new_vids:
                    duration = 0
                    vid = file.split('.')[0]
                
                    audio_fn = vid + '.wav'
                    audio_file = os.path.join(audio_category_dir, audio_fn)
                    # print (audio_file)
                    total_length = video_duration (audio_file)
                    
                    script_json = os.path.join(category_dir, file)
                    with open(script_json) as f:
                        script = json.load(f)
                    for ind in range (len (script) + 1):
                        # if (ind == 0 or ind == len (script)):
                        #     continue
                        if (ind == 0):
                            gap = (script[ind]['start'] - 0)
                        elif (ind == len (script)):
                            gap = total_length - script[ind - 1]['end']
                        else:
                            last_sentence = script[ind - 1]
                            gap = (script[ind]['start'] - last_sentence['end'])

                        if (gap > 0):
                            duration += gap
                    

                    distribution_result.append ({'video_id': vid, 'total': round (total_length, 3), 'no_audio': round (duration, 3), 'portion': round (duration / total_length, 3)})

        # print (len (distribution_result))

        total_length = 0
        total_duration = 0

        duration_list = []
        portion_list = []

        vids = []
        for video in distribution_result:
            total_length += video['total']
            total_duration += video['no_audio']
            duration_list.append (video['no_audio'])
            portion_list.append (video['portion'])

            if (video['portion'] > 0.5):
                vids.append (video['video_id'])

            # print (video)

        print ("total length : ", round (total_length, 3))
        print ("time w/o audio : ", round (total_duration, 3))
        print ("average portion : ", round (total_duration / total_length, 3))

        sorted_distribution_list = sorted(distribution_result, key=lambda k: k['portion'])
        # for item in sorted_distribution_list:
        #     print (item)
        print (len(sorted_distribution_list))


        output_file = './new_selected_portion_analysis_include(0823).json'
        with open (output_file, "w") as json_file:
            json.dump (sorted_distribution_list, json_file)