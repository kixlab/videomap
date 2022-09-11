import os
import json
from xml.dom.minidom import Element
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


# ----------------------------------------------------#
# --------------- Helper functions -------------------#
# ----------------------------------------------------#

TYPES = {'opening', 'closing', 'goal', 'motivation', 'briefing', 'subgoal', 'instruction', 'tool', 'warning', 'tip', 'justification', 'effect', 'status', 'context', 'tool specification', 'outcome', 'reflection', 'side note', 'self-promo', 'bridge', 'filler', 'none'}
CATEGORIES = {'greeting', 'overview', 'step', 'supplementary', 'explanation', 'description', 'conclusion', 'misc.', 'none'}
SECTIONS = {'intro', 'procedure', 'outro', 'misc.', 'none'}


def read_json (fp):
    with open (fp, 'r') as s:
        script = json.load (s)
    return script

def write_json (fp, script):
    with open(fp, "w") as json_file:
        json.dump(script, json_file)


# analyze total videos
# input data = [script1, script2, ...]
def analyze_total (data):
    total_videos = len (data)

    types = {}
    categories = {}
    sections = {}

    type_total = 0
    vids = []

    for script in data:
        vids.append (script['vid'])
        type_total += script['total']
        # label count
        for level in script['count']:

            for item in script['count'][level]:
                item_obj = script['count'][level][item]
                if level == 'types':
                    if (item not in types.keys()):
                        types[item] = {'count': item_obj['count'], 'portion': 0}
                    else:
                        types[item]['count'] += item_obj['count']
                        # types[item]['portion'] += item_obj['portion']

                elif level == 'categories':
                    if (item not in categories.keys()):
                        categories[item] = {'count': item_obj['count'], 'portion': 0}
                    else:
                        categories[item]['count'] += item_obj['count']
                        # categories[item]['portion'] += item_obj['portion']

                else:
                    if (item not in sections.keys()):
                        sections[item] = {'count': item_obj['count'], 'portion': 0}
                    else:
                        sections[item]['count'] += item_obj['count']
                        # sections[item]['portion'] += item_obj['portion']

    counts = {'types': types, 'categories': categories, 'sections': sections}
    for level in counts:
        for item in counts[level]:
            count = counts[level][item]['count']
            portion = count / type_total
            counts[level][item]['count'] = count / total_videos
            counts[level][item]['portion'] = portion


    types = {}
    categories = {}
    sections = {}

    audio_duration_total = 0

    for script in data:
        # time portion
        audio_duration_total += script['audio_duration']
        for level in script['time_portion']:

            for item in script['time_portion'][level]:
                item_obj = script['time_portion'][level][item]
                if level == 'types':
                    if (item not in types.keys()):
                        types[item] = {'time': item_obj['time']}
                    else:
                        types[item]['time'] += item_obj['time']
                        # types[item]['portion'] += item_obj['portion']

                elif level == 'categories':
                    if (item not in categories.keys()):
                        categories[item] = {'time': item_obj['time']}
                    else:
                        categories[item]['time'] += item_obj['time']
                        # categories[item]['portion'] += item_obj['portion']

                else:
                    if (item not in sections.keys()):
                        sections[item] = {'time': item_obj['time']}
                    else:
                        sections[item]['time'] += item_obj['time']
                        # sections[item]['portion'] += item_obj['portion']

    times = {'types': types, 'categories': categories, 'sections': sections}

    for level in times:
        for item in times[level]:
            times[level][item]['time'] = times[level][item]['time'] / audio_duration_total
            # times[level][item]['portion'] = round (times[level][item]['portion'] / total_videos, 2)

    unique_types = 0
    unique_cats = 0
    unique_sections = 0
    for script in data:
        unique_types += script['unique_count']['types']['number']
        unique_cats += script['unique_count']['categories']['number']
        unique_sections += script['unique_count']['sections']['number']

    unique_counts = {'types': round (unique_types/total_videos, 2), 'categories': round(unique_cats/total_videos, 2), 'sections': round(unique_sections/total_videos, 2)}

    data_obj = {"vids": vids, "total_count": type_total, "audio_duration": audio_duration_total, 'count': counts, 'time_portion': times, "unique_count": unique_counts}
    return data_obj


def analyze_type_with_time (data):
    iter = 1000

    types_data = {}
    categories_data = {}
    sections_data = {}

    for t in TYPES:
        types_data[t] = [0 for _ in range (iter)]

    for c in CATEGORIES:
        categories_data[c] = [0 for _ in range (iter)]

    for s in SECTIONS:
        sections_data[s] = [0 for _ in range (iter)]

    time = [i/1000 for i in range (1000)]

    for script in data:
        norm_ts_data = script['normalzied_ts']
        for i, item in enumerate(norm_ts_data):
            types_data[item['type']][i]+= 1
            categories_data[item['category']][i]+=1
            sections_data[item['section']][i]+=1

    return {'time': time, 'types': types_data, 'categories': categories_data, 'sections': sections_data}

def visualize_time_data (data):

    types_data = {}
    categories_data = {}
    sections_data = {}

    types_data['time'] = data['time']
    categories_data['time'] = data['time']
    sections_data['time'] = data['time']

    for t in data['types'].keys():
        types_data[t] = data['types'][t]
    for c in data['categories'].keys():
        categories_data[c] = data['categories'][c]
    for s in data['sections'].keys():
        sections_data[s] = data['sections'][s]

    types_df = pd.DataFrame(types_data)
    categories_df = pd.DataFrame (categories_data)
    sections_df = pd.DataFrame (sections_data)

    types_dfm = types_df.melt('time', var_name = 'type', value_name='counts')
    categories_dfm = categories_df.melt('time', var_name = 'category', value_name='counts')
    sections_dfm = sections_df.melt('time', var_name = 'section', value_name='counts')

    # sns.kdeplot(data=types_dfm, x="time", y="counts", hue="type")
    # sns.kdeplot(data=categories_dfm, x="time", y="counts", hue="category")
    # sns.kdeplot(data=sections_dfm, x="time", y="counts", hue="section")

    # histogram
    # sns.displot (sections_dfm, x="time", y="counts", hue="section", bins=100)

    # line
    sns.replot (data = sections_dfm, x="time", y="counts", kind="line")

    # kernel density
    # sns.displot (sections_dfm, x="time", y="counts", hue="section", kde=True)

    # sns.displot(data=categories_dfm, x="time", y="counts", hue="category", kind="kde")
    # sns.rugplot(data=sections_dfm, x="time", y="counts", hue="section")

    plt.show()
            


ROOT_DIR = './data/analysis/'
SAVE_DIR = './data/final/'

### styles ###
# 1st
first_vids = ['1oiCLxngvBo', 'uUBVc8Ugz0k', '2OoebJA2mnE', '-xCtbeecgKQ', 'z1Xv6Pa0toE', '9mjXFA1TMTI', 'QzS7Z80poKo', 'bwxvH99sLqw', 'ZORD4y7dL08', '-szevr-BRZE', 'KLLqGcgxQEw', 'Czi_ZirnzRo', '73lxEIKyX8M', 'eDG1c6a6uqc', 'Rcsy2HRuiyA', 'CxdRXDN1fkA', 'dJ_qCDWNvXU', 'BzxPDw6ezEc', 'h281yamVFDc', '5AU2vJU-QJM', 'rqBiByEbMHc', 'sM81wJ7GDrI', 'sij_wNj0doI', 'BotYnPhByWg', 'A_qivvTkijw', 'S0luUzNRtq0', 'kPGwDxo5Yf4', 'bg3orsnRCVE', 'Xh_Awznyc7s', 'cGn_oZPotZA', 'Cvv1wiqKMHc', 'AnWGek4P_dY', '7IcOJEEObA0', 'IICwmc4WX2E', 'Eeu5uL6r2rg', 'k0koOhfXv_s', '4WaXJs9RR3E', 'T1j7Yq5-cIs', 'ihCwjLj31hY', '2Xyfgwj92v0', 'zMqzjMrxNR0', 'AbhW9YbQ0fM', 'Df9F8ettY8k', 'ntwi2Unh3JQ', 'ysHg9vOMe_4', 'OcjCNqfRgP0', 'bxXXCP0AE5A', 'Y84sqS2Nljs', 'm0H56KpKLHA', 'ygRQRgR11Zg', 'kNsjE4HO7tE', 'CdZQF4DDAxM']
# 3rd
third_vids = ['mZZJYDfmgeg', 'WIIjq2GexIw', 'ZT1dvq6yacQ', 'PyWZYHy17As', 'u00iLnvVgFc', '-6tnn1G1dRg', 'jhAklPzn0XQ', 'mUq6l7N6zuk', 'Ag6D8RGQnjw', 'VDMOFa8iRqo', 'mQjCKgEPs8k', 'pn81__TovpY', 'kz5dJ9SCu4M', 'yJ7VzfG2ONo', 'JNznnqX6SsE', 'dKUomyn1TYQ', 'yYOysPt5gic', 'ZY11rbwCaMM', 'WcD8bG2VB_s', '5ywy531EMNA', '0TLQg_b1v5Q', 'Vrz25x3qnTY', 'eyD2iwXOeFM', 'ynmdOz_D1R4', 'r6JmI35r5E8', '-wlSMSl02Xs', 'UZJ0nmB3epQ', 'N3c81EPZ51Q', 'e3StC_4qemI', 'ntYwKXN82QU', 's4coMAU80U4', '7oXrT1CqLCY', 'uMgpr6X5asI', 'bQKTjz0JKhg', 'SXQHgJHYQgc', 'wvC3_Rs4mXs', '2xXPSfQBP-w', 'yeT52sDtYEU', 'XFYHIg8U--4', '1dALzTPQWJg', 'jGsEBwiKnCI', 'mj1Fu3-XQpI', 'b2EZggyT5O4']
# both
view_both_vids = ['ZeVRqW2J3UY', 'T622Ec77ZPY', 'ZmTxw3UbMO4', '6CJryveLzvI', 'xTARWxkTJw0', 'ta5IB2wy6ic', '1Ni8KOzRzuI', 'djvLEfwwQPU', 'HFp5uH12wkc', 'EnjZHOb6qNE', 'tb1L7Rsm1U8', 'mwpb65gm1e0', 'oe7Cz-dxSBY', 'T5MbMuoNQ1k', '0fxL8v2dMho', '8DgsLNa3ums', 'WoDZQRGyuHA', 'UriwETsgsqg']
# screencast
screencast_vids = ['XN3N5K2axpw', 'Nu_By3eTpoc', '0SMzqWV6xxs', '_Yb6xLqvsf0', 'nnzPJv5XIws', 'GFd7kLvhc2Q', 'yu-G9kEKdTo']

# static/move
static_move_vids = ['1oiCLxngvBo', 'Nu_By3eTpoc', 'ZeVRqW2J3UY', '2OoebJA2mnE', '-xCtbeecgKQ', 'z1Xv6Pa0toE', 'T622Ec77ZPY', '9mjXFA1TMTI', 'jhAklPzn0XQ', 'QzS7Z80poKo', 'bwxvH99sLqw', 'mUq6l7N6zuk', '0SMzqWV6xxs', 'nnzPJv5XIws', 'ZORD4y7dL08', '-szevr-BRZE', 'KLLqGcgxQEw', 'Czi_ZirnzRo', 'GFd7kLvhc2Q', '73lxEIKyX8M', 'eDG1c6a6uqc', 'Rcsy2HRuiyA', 'Ag6D8RGQnjw', 'CxdRXDN1fkA', 'dJ_qCDWNvXU', 'BzxPDw6ezEc', 'ZmTxw3UbMO4', 'h281yamVFDc', '6CJryveLzvI', 'xTARWxkTJw0', 'WcD8bG2VB_s', 'ta5IB2wy6ic', 'rqBiByEbMHc', 'sM81wJ7GDrI', '0TLQg_b1v5Q', '1Ni8KOzRzuI', 'Vrz25x3qnTY', 'sij_wNj0doI', 'BotYnPhByWg', 'djvLEfwwQPU', 'eyD2iwXOeFM', 'kPGwDxo5Yf4', 'bg3orsnRCVE', 'HFp5uH12wkc', 'Xh_Awznyc7s', 'cGn_oZPotZA', 'ynmdOz_D1R4', 'yu-G9kEKdTo', 'r6JmI35r5E8', 'AnWGek4P_dY', '7IcOJEEObA0', '-wlSMSl02Xs', 'IICwmc4WX2E', 'Eeu5uL6r2rg', 'k0koOhfXv_s', '4WaXJs9RR3E', 'tb1L7Rsm1U8', 'T1j7Yq5-cIs', 'ihCwjLj31hY', 'mwpb65gm1e0', 'oe7Cz-dxSBY', 'zMqzjMrxNR0', 'UZJ0nmB3epQ', 'T5MbMuoNQ1k', 'N3c81EPZ51Q', 'e3StC_4qemI', 's4coMAU80U4', '7oXrT1CqLCY', 'uMgpr6X5asI', 'AbhW9YbQ0fM', 'bQKTjz0JKhg', 'SXQHgJHYQgc', 'ysHg9vOMe_4', 'OcjCNqfRgP0', 'WoDZQRGyuHA', 'bxXXCP0AE5A', 'Y84sqS2Nljs', 'm0H56KpKLHA', 'ygRQRgR11Zg', 'kNsjE4HO7tE', 'mj1Fu3-XQpI', 'CdZQF4DDAxM', 'UriwETsgsqg', 'b2EZggyT5O4']
# view/zoom change
view_zoom_change_vids = ['mZZJYDfmgeg', 'XN3N5K2axpw', 'WIIjq2GexIw', 'ZT1dvq6yacQ', 'PyWZYHy17As', 'uUBVc8Ugz0k', 'u00iLnvVgFc', '-6tnn1G1dRg', '_Yb6xLqvsf0', 'VDMOFa8iRqo', 'mQjCKgEPs8k', 'pn81__TovpY', 'kz5dJ9SCu4M', 'yJ7VzfG2ONo', 'JNznnqX6SsE', 'dKUomyn1TYQ', '5AU2vJU-QJM', 'yYOysPt5gic', 'ZY11rbwCaMM', '5ywy531EMNA', 'A_qivvTkijw', 'S0luUzNRtq0', 'Cvv1wiqKMHc', 'EnjZHOb6qNE', '2Xyfgwj92v0', '0fxL8v2dMho', '8DgsLNa3ums', 'ntYwKXN82QU', 'Df9F8ettY8k', 'ntwi2Unh3JQ', 'wvC3_Rs4mXs', '2xXPSfQBP-w', 'yeT52sDtYEU', 'XFYHIg8U--4', '1dALzTPQWJg', 'jGsEBwiKnCI']

# talking
talking_vids = ['mZZJYDfmgeg', '1oiCLxngvBo', 'PyWZYHy17As', 'Nu_By3eTpoc', 'u00iLnvVgFc', '2OoebJA2mnE', '-xCtbeecgKQ', '-6tnn1G1dRg', 'T622Ec77ZPY', '9mjXFA1TMTI', 'jhAklPzn0XQ', 'QzS7Z80poKo', 'bwxvH99sLqw', 'mUq6l7N6zuk', '0SMzqWV6xxs', 'nnzPJv5XIws', 'ZORD4y7dL08', 'Czi_ZirnzRo', 'GFd7kLvhc2Q', '73lxEIKyX8M', 'eDG1c6a6uqc', 'Rcsy2HRuiyA', 'Ag6D8RGQnjw', 'CxdRXDN1fkA', 'VDMOFa8iRqo', 'kz5dJ9SCu4M', 'yJ7VzfG2ONo', 'JNznnqX6SsE', 'dKUomyn1TYQ', 'h281yamVFDc', '6CJryveLzvI', 'ZY11rbwCaMM', 'xTARWxkTJw0', 'WcD8bG2VB_s', '5ywy531EMNA', '0TLQg_b1v5Q', 'Vrz25x3qnTY', 'sij_wNj0doI', 'BotYnPhByWg', 'A_qivvTkijw', 'S0luUzNRtq0', 'HFp5uH12wkc', 'ynmdOz_D1R4', 'r6JmI35r5E8', '7IcOJEEObA0', '-wlSMSl02Xs', 'IICwmc4WX2E', 'Eeu5uL6r2rg', 'mwpb65gm1e0', 'zMqzjMrxNR0', 'UZJ0nmB3epQ', 'T5MbMuoNQ1k', '0fxL8v2dMho', '8DgsLNa3ums', 'e3StC_4qemI', 'ntYwKXN82QU', 's4coMAU80U4', '7oXrT1CqLCY', 'uMgpr6X5asI', 'AbhW9YbQ0fM', 'bQKTjz0JKhg', 'SXQHgJHYQgc', 'ntwi2Unh3JQ', 'ysHg9vOMe_4', 'OcjCNqfRgP0', 'WoDZQRGyuHA', 'wvC3_Rs4mXs', 'bxXXCP0AE5A', '2xXPSfQBP-w', 'yeT52sDtYEU', 'Y84sqS2Nljs', 'XFYHIg8U--4', '1dALzTPQWJg', 'jGsEBwiKnCI', 'kNsjE4HO7tE', 'mj1Fu3-XQpI', 'CdZQF4DDAxM', 'b2EZggyT5O4']
# dubbing
dubbing_vids = ['XN3N5K2axpw', 'WIIjq2GexIw', 'ZT1dvq6yacQ', 'uUBVc8Ugz0k', 'ZeVRqW2J3UY', '_Yb6xLqvsf0', '-szevr-BRZE', 'KLLqGcgxQEw', 'dJ_qCDWNvXU', 'mQjCKgEPs8k', 'BzxPDw6ezEc', 'pn81__TovpY', 'ZmTxw3UbMO4', '5AU2vJU-QJM', 'yYOysPt5gic', 'ta5IB2wy6ic', 'rqBiByEbMHc', 'sM81wJ7GDrI', 'djvLEfwwQPU', 'eyD2iwXOeFM', 'kPGwDxo5Yf4', 'bg3orsnRCVE', 'Xh_Awznyc7s', 'cGn_oZPotZA', 'Cvv1wiqKMHc', 'EnjZHOb6qNE', 'AnWGek4P_dY', 'k0koOhfXv_s', '4WaXJs9RR3E', 'tb1L7Rsm1U8', 'T1j7Yq5-cIs', 'ihCwjLj31hY', '2Xyfgwj92v0', 'N3c81EPZ51Q', 'Df9F8ettY8k', 'm0H56KpKLHA', 'ygRQRgR11Zg', 'UriwETsgsqg']
# both
narration_both_vids = ['z1Xv6Pa0toE', '1Ni8KOzRzuI', 'yu-G9kEKdTo', 'oe7Cz-dxSBY']


### categories ###
# ane = ['mZZJYDfmgeg', 'XN3N5K2axpw', 'WIIjq2GexIw', '1oiCLxngvBo', 'ZT1dvq6yacQ', 'PyWZYHy17As', 'uUBVc8Ugz0k', 'Nu_By3eTpoc', 'ZeVRqW2J3UY', 'u00iLnvVgFc']
# cnov = ['2OoebJA2mnE', '-xCtbeecgKQ', '-6tnn1G1dRg', 'z1Xv6Pa0toE', 'T622Ec77ZPY', '9mjXFA1TMTI', 'jhAklPzn0XQ', 'QzS7Z80poKo', 'bwxvH99sLqw', 'mUq6l7N6zuk']
# cne = ['0SMzqWV6xxs', '_Yb6xLqvsf0', 'nnzPJv5XIws', 'ZORD4y7dL08', '-szevr-BRZE', 'KLLqGcgxQEw', 'Czi_ZirnzRo', 'GFd7kLvhc2Q', '73lxEIKyX8M', 'eDG1c6a6uqc']
# enc = ['Rcsy2HRuiyA', 'Ag6D8RGQnjw', 'CxdRXDN1fkA', 'dJ_qCDWNvXU', 'VDMOFa8iRqo', 'mQjCKgEPs8k', 'BzxPDw6ezEc', 'pn81__TovpY', 'ZmTxw3UbMO4', 'kz5dJ9SCu4M']
# fne = ['yJ7VzfG2ONo', 'JNznnqX6SsE', 'dKUomyn1TYQ', 'h281yamVFDc', '5AU2vJU-QJM', 'yYOysPt5gic', '6CJryveLzvI', 'ZY11rbwCaMM', 'xTARWxkTJw0', 'WcD8bG2VB_s']
# health = ['ta5IB2wy6ic', 'rqBiByEbMHc', '5ywy531EMNA', 'sM81wJ7GDrI', '0TLQg_b1v5Q', '1Ni8KOzRzuI', 'Vrz25x3qnTY', 'sij_wNj0doI', 'BotYnPhByWg', 'djvLEfwwQPU']
# hnc = ['A_qivvTkijw', 'S0luUzNRtq0', 'eyD2iwXOeFM', 'kPGwDxo5Yf4', 'bg3orsnRCVE', 'HFp5uH12wkc', 'Xh_Awznyc7s', 'cGn_oZPotZA', 'ynmdOz_D1R4', 'yu-G9kEKdTo']
# hnt = ['Cvv1wiqKMHc', 'EnjZHOb6qNE', 'r6JmI35r5E8', 'AnWGek4P_dY', '7IcOJEEObA0', '-wlSMSl02Xs', 'IICwmc4WX2E', 'Eeu5uL6r2rg', 'k0koOhfXv_s', '4WaXJs9RR3E']
# hng = ['tb1L7Rsm1U8', 'T1j7Yq5-cIs', 'ihCwjLj31hY', '2Xyfgwj92v0', 'mwpb65gm1e0', 'oe7Cz-dxSBY', 'zMqzjMrxNR0', 'UZJ0nmB3epQ', 'T5MbMuoNQ1k', '0fxL8v2dMho']
# pcns = ['8DgsLNa3ums', 'N3c81EPZ51Q', 'e3StC_4qemI', 'ntYwKXN82QU', 's4coMAU80U4', '7oXrT1CqLCY', 'uMgpr6X5asI', 'AbhW9YbQ0fM', 'bQKTjz0JKhg', 'SXQHgJHYQgc']
# pna = ['Df9F8ettY8k', 'ntwi2Unh3JQ', 'ysHg9vOMe_4', 'OcjCNqfRgP0', 'WoDZQRGyuHA', 'wvC3_Rs4mXs', 'bxXXCP0AE5A', '2xXPSfQBP-w', 'yeT52sDtYEU', 'Y84sqS2Nljs']
# snf = ['XFYHIg8U--4', 'm0H56KpKLHA', '1dALzTPQWJg', 'ygRQRgR11Zg', 'jGsEBwiKnCI', 'kNsjE4HO7tE', 'mj1Fu3-XQpI', 'CdZQF4DDAxM', 'UriwETsgsqg', 'b2EZggyT5O4']

if __name__ == "__main__":

    scripts = []

    # selected_dir = "Sports and Fitness"

    for root, dirs, files in os.walk (ROOT_DIR):
        for dir_name in dirs:
            # if (dir_name == selected_dir):
            if True:

                print ('*' * 30)
                print ('directory :', dir_name)

                cat_dir = os.path.join (ROOT_DIR, dir_name)
                files = os.listdir(cat_dir)
                for file in files:
                    vid = file.split('.')[0]
                    # if vid in narration_both_vids:
                    if True:
                        print (vid)
                        fp = os.path.join (cat_dir, file)
                        script_data = read_json (fp)
                        scripts.append (script_data)

    # analyzed_data = analyze_total (scripts)
    # fn = os.path.join (SAVE_DIR, 'analyzed_' + selected_dir + '.json')
    # write_json (fn, analyzed_data)

    time_type_data = analyze_type_with_time (scripts)
    visualize_time_data (time_type_data)


    # assertion
    # tot_por = 0
    # time_por = 0
    # for type in analyzed_data['count']['sections']:
    #     tot_por += analyzed_data['count']['sections'][type]['portion']
    # for type in analyzed_data['time_portion']['sections']:
    #     time_por += analyzed_data['time_portion']['sections'][type]['time']
    # print (tot_por)
    # print (time_por)



                    


