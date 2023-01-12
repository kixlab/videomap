import os
import json
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.interpolate import UnivariateSpline
from scipy.signal import savgol_filter


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



# get test statistics from the analysis of each video
# min/max
def analyze_detail_info (data):
    types = {}
    categories = {}

    tad = 0
    avg_ad = 41910.270000000004 / 120
    for script in data:
        max = 0
        max_cat = ''
        # time portion
        # tad += script['audio_duration']
        ad = script['audio_duration']
        for level in script['time_portion']:

            for item in script['time_portion'][level]:
                item_obj = script['time_portion'][level][item]
                if level == 'types':
                    if (item not in types.keys()):
                        types[item] = [item_obj['time']]
                    else:
                        types[item].append(item_obj['time'] )
                        # types[item]['portion'] += item_obj['portion']

                elif level == 'categories':
                    # if max < item_obj['time']:
                    #     max = item_obj['time']
                    #     max_cat = item
                    if (item not in categories.keys()):
                        categories[item] = [item_obj['time']]
                    else:
                        categories[item].append(item_obj['time'])
                        # categories[item]['portion'] += item_obj['portion']

        # print ('*****')
        # print (script ['vid'])
        # print (max_cat)
    times = {'types': types, 'categories': categories, }

    print (tad)
    for level in times:
        print ('**************')
        print (level)
        for item in times[level]:
            print (item)
            tmp = times[level][item]
            for i in range (120 - len(tmp)):
                tmp.append (0)

            print (len(tmp))
            # print (tmp)
            tmp = np.array (tmp)
            tmp = tmp / avg_ad
            print (np.round(np.mean(tmp) * 100, 3))
            print (np.round(np.std(tmp) * 100, 3))
            # print (np.std (tmp))
            # times[level][item]['time'] = times[level][item]['time']
    # types = {}
    # categories = {}

    # for script in data:
    #     for level in script['time_portion']:
    #         for item in script['time_portion'][level]:
    #             item_obj = script['time_portion'][level][item]
    #             if level == 'types':
    #                 if item not in types.keys():
    #                     types[item] = []
    #                 types[item].append (item_obj['time'] / script['audio_duration'])

    #             elif level == 'categories':
    #                 if item not in categories.keys():
    #                     categories[item] = []
    #                 categories[item].append (item_obj['time'] / script['audio_duration'])

    # for i in types.keys():
    #     empty_len = 120-len(types[i])
    #     for j in range (empty_len):
    #         types[i].append (0)
    #     print (i)
    #     print (types[i])

    #     tmp = np.array (types[i])
    #     print (i)
    #     print (np.round(np.mean (tmp), 3))
    #     print (np.round (np.std (tmp), 3))
        # print (i, ' : ', 'min ', min(types[i]), ' max ', max(types[i]))

    # print ('**************************')
    # for i in categories.keys():
    #     empty_len = 120-len(categories[i]) + 1
    #     for j in range (empty_len):
    #         categories[i].append (0)
    #     tmp = np.array (categories[i])
    #     print (i)
    #     print (np.round (np.mean (tmp), 3))
    #     print (np.round (np.std (tmp), 3))
        # print (i, ' : ', 'min ', min(categories[i]), ' max ', max(categories[i]))

    # types_df = pd.DataFrame (types)
    # categories_df = pd.DataFrame (categories)
    # print (types_df.head())



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
        ad = script['audio_duration']
        for level in script['time_portion']:

            for item in script['time_portion'][level]:
                item_obj = script['time_portion'][level][item]
                if level == 'types':
                    if (item not in types.keys()):
                        types[item] = {'time': [item_obj['time'] / ad]}
                    else:
                        types[item]['time'].append(item_obj['time'] / ad)
                        # types[item]['portion'] += item_obj['portion']

                elif level == 'categories':
                    if (item not in categories.keys()):
                        categories[item] = {'time': [item_obj['time'] / ad]}
                    else:
                        categories[item]['time'].append(item_obj['time'] / ad)
                        # categories[item]['portion'] += item_obj['portion']

                # else:
                #     if (item not in sections.keys()):
                #         sections[item] = {'time': item_obj['time']}
                #     else:
                #         sections[item]['time'] += item_obj['time']
                        # sections[item]['portion'] += item_obj['portion']

    times = {'types': types, 'categories': categories, 'sections': sections}

    type_tot = 0
    cat_tot = 0
    for level in times:
        print ('********')
        print (level)
        for item in times[level]:
            print (item)
            time_portion_list = times[level][item]['time']
            for i in range (48 - len (time_portion_list)):
                time_portion_list.append (0)
            time_portion_np = np.array(time_portion_list)
            # print (np.round (np.min (time_portion_np)* 100, 2))
            # print (np.round (np.max (time_portion_np)* 100, 2))
            time_avg = np.mean (time_portion_np)
            times_std = np.std (time_portion_np)
            times[level][item]['time'] = time_avg
            if (level == 'types'):
                type_tot += time_avg
            if (level == 'categories'):
                cat_tot += time_avg


            # print (np.round (time_avg * 100, 3))
            # print (np.round (times_std * 100, 3))
            # times[level][item]['portion'] = round (times[level][item]['portion'] / total_videos, 2)

    print ('type :', type_tot)
    print ('cat: ', cat_tot)

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

    types_data['time'] = [item * 1000 for item in data['time']]
    categories_data['time'] = [item * 1000 for item in data['time']]
    sections_data['time'] = [item * 1000 for item in data['time']]

    for t in data['types'].keys():
        types_data[t] = data['types'][t]
    for c in data['categories'].keys():
        categories_data[c] = data['categories'][c]
    for s in data['sections'].keys():
        sections_data[s] = data['sections'][s]

    types_df = pd.DataFrame(types_data)
    categories_df = pd.DataFrame (categories_data)
    sections_df = pd.DataFrame (sections_data)

    # columns to delete
    types_df = types_df.drop(['none'], axis = 1)
    categories_df = categories_df.drop(['none'], axis = 1)
    sections_df = sections_df.drop(['none'], axis = 1)

    categories_df.set_index('time', inplace=True)
    sections_df.set_index('time', inplace=True)

    categories_df = categories_df[['greeting', 'overview', 'step', 'supplementary', 'explanation', 'description', 'conclusion', 'misc.']]
    sections_df = sections_df[['intro', 'procedure', 'outro', 'misc.']]

    categories_df.rename(columns = {'greeting':'Greeting', 'overview':'Overview', 'step': 'Method', 'supplementary': 'Supplementary', 'explanation':'Explanation', 'description': 'Description', 'conclusion': 'Conclusion', 'misc.': 'Misc.'}, inplace=True)
    sections_df.rename(columns={'intro': 'Intro', 'procedure': 'Procedure', 'outro': 'Outro', 'misc.': 'Misc.'})


    new_cat_df = pd.DataFrame()
    new_index = np.linspace(0, 1000, 1000)
    new_cat_df['Greeting'] = savgol_filter(categories_df['Greeting'], 60, 2)
    new_cat_df['Overview'] = savgol_filter(categories_df['Overview'], 60, 2)
    new_cat_df['Method'] = savgol_filter(categories_df['Method'], 60, 2)
    new_cat_df['Supplementary'] = savgol_filter(categories_df['Supplementary'], 60, 2)
    new_cat_df['Explanation'] = savgol_filter(categories_df['Explanation'], 60, 2)
    new_cat_df['Description'] = savgol_filter(categories_df['Description'], 60, 2)
    new_cat_df['Conclusion'] = savgol_filter(categories_df['Conclusion'], 60, 2)
    new_cat_df['Misc.'] = savgol_filter(categories_df['Misc.'], 60, 2)
    new_cat_df.index = new_index

    # plt.subplot (1, 2, 1)
    # plt.plot(sections_df)
    # plt.ylabel ('Number of Labels', fontsize=25)
    # plt.xlabel ('Normalized Time (sec)', fontsize=25)
    # plt.xticks (fontsize=23)
    # plt.yticks (fontsize=23)
    # plt.ylim (0, 115)
    # plt.legend(['Intro', 'Procedure', 'Outro', 'Misc.'], fontsize=20)

    # plt.subplot (1, 2, 2)
    plt.plot(new_cat_df)
    # plt.ylabel ('Number of Labels', fontsize=22)
    plt.xlabel ('Normalized Time (sec)', fontsize=25)
    plt.xticks (fontsize=23)
    plt.yticks (fontsize=23)
    plt.ylim (0, 115)
    plt.legend(['Greeting', 'Overview', 'Method', 'Supplementary', 'Explanation', 'Description', 'Conclusion', 'Misc.'], fontsize=20, ncol=2, loc="upper right")



    plt.tight_layout()
    plt.show()

    # save as csv
    # types_df.to_csv ('./data/final/types_df.csv')
    # categories_df.to_csv ('./data/final/categories_df.csv')
    # sections_df.to_csv ('./data/final/sections_df.csv'

    # sections_df['intro'].plot (style = 'r--', label= "line")
    # sections_df['intro'].ewm(span=1000).mean().plot(style='b', label="ema")

    # types_dfm = types_df.melt('time', var_name = 'type', value_name='counts')
    # categories_dfm = categories_df.melt('time', var_name = 'category', value_name='counts')
    # sections_dfm = sections_df.melt('time', var_name = 'section', value_name='counts')


    # print (types_dfm.head())
    # print (categories_dfm.head())
    # print (sections_dfm.head())

    # sns.kdeplot(data=types_dfm, x="time", y="counts", hue="type")
    # sns.kdeplot(data=categories_dfm, x="time", y="counts", hue="category")
    # sns.kdeplot(data=sections_dfm, x="time", y="counts", hue="section")

    # histogram
    # sns.displot (sections_dfm, x="time", hue="section", kind='kde', multiple='stack')

    # line
    # sns.lineplot (data = types_dfm, x="time", y="counts", hue="type")
    # sns.lineplot (data = categories_dfm, x="time", y="counts", hue="category")
    # sns.lineplot (data = sections_dfm, x="time", y="counts", hue="section")

    # step_df = categories_df[['time', 'step']]
    #histogram
    # sns.histplot(data=step_df, x="step", bins=100, kde=True)

    # kernel density
    # sns.displot (sections_dfm, x="time", y="counts", hue="section", kde=True)

    # sns.displot(data=categories_dfm, x="time", y="counts", hue="category", kind="kde")
    # sns.rugplot(data=sections_dfm, x="time", y="counts", hue="section")

    # plt.show()
    # plt.savefig ('./data/figures/category_time.png')

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

# talking 78
talking_vids = ['mZZJYDfmgeg', '1oiCLxngvBo', 'PyWZYHy17As', 'Nu_By3eTpoc', 'u00iLnvVgFc', '2OoebJA2mnE', '-xCtbeecgKQ', '-6tnn1G1dRg', 'T622Ec77ZPY', '9mjXFA1TMTI', 'jhAklPzn0XQ', 'QzS7Z80poKo', 'bwxvH99sLqw', 'mUq6l7N6zuk', '0SMzqWV6xxs', 'nnzPJv5XIws', 'ZORD4y7dL08', 'Czi_ZirnzRo', 'GFd7kLvhc2Q', '73lxEIKyX8M', 'eDG1c6a6uqc', 'Rcsy2HRuiyA', 'Ag6D8RGQnjw', 'CxdRXDN1fkA', 'VDMOFa8iRqo', 'kz5dJ9SCu4M', 'yJ7VzfG2ONo', 'JNznnqX6SsE', 'dKUomyn1TYQ', 'h281yamVFDc', '6CJryveLzvI', 'ZY11rbwCaMM', 'xTARWxkTJw0', 'WcD8bG2VB_s', '5ywy531EMNA', '0TLQg_b1v5Q', 'Vrz25x3qnTY', 'sij_wNj0doI', 'BotYnPhByWg', 'A_qivvTkijw', 'S0luUzNRtq0', 'HFp5uH12wkc', 'ynmdOz_D1R4', 'r6JmI35r5E8', '7IcOJEEObA0', '-wlSMSl02Xs', 'IICwmc4WX2E', 'Eeu5uL6r2rg', 'mwpb65gm1e0', 'zMqzjMrxNR0', 'UZJ0nmB3epQ', 'T5MbMuoNQ1k', '0fxL8v2dMho', '8DgsLNa3ums', 'e3StC_4qemI', 'ntYwKXN82QU', 's4coMAU80U4', '7oXrT1CqLCY', 'uMgpr6X5asI', 'AbhW9YbQ0fM', 'bQKTjz0JKhg', 'SXQHgJHYQgc', 'ntwi2Unh3JQ', 'ysHg9vOMe_4', 'OcjCNqfRgP0', 'WoDZQRGyuHA', 'wvC3_Rs4mXs', 'bxXXCP0AE5A', '2xXPSfQBP-w', 'yeT52sDtYEU', 'Y84sqS2Nljs', 'XFYHIg8U--4', '1dALzTPQWJg', 'jGsEBwiKnCI', 'kNsjE4HO7tE', 'mj1Fu3-XQpI', 'CdZQF4DDAxM', 'b2EZggyT5O4']
# non talking 42
non_talking_vids = ['XN3N5K2axpw', 'WIIjq2GexIw', 'ZT1dvq6yacQ', 'uUBVc8Ugz0k', 'ZeVRqW2J3UY', '_Yb6xLqvsf0', '-szevr-BRZE', 'KLLqGcgxQEw', 'dJ_qCDWNvXU', 'mQjCKgEPs8k', 'BzxPDw6ezEc', 'pn81__TovpY', 'ZmTxw3UbMO4', '5AU2vJU-QJM', 'yYOysPt5gic', 'ta5IB2wy6ic', 'rqBiByEbMHc', 'sM81wJ7GDrI', 'djvLEfwwQPU', 'eyD2iwXOeFM', 'kPGwDxo5Yf4', 'bg3orsnRCVE', 'Xh_Awznyc7s', 'cGn_oZPotZA', 'Cvv1wiqKMHc', 'EnjZHOb6qNE', 'AnWGek4P_dY', 'k0koOhfXv_s', '4WaXJs9RR3E', 'tb1L7Rsm1U8', 'T1j7Yq5-cIs', 'ihCwjLj31hY', '2Xyfgwj92v0', 'N3c81EPZ51Q', 'Df9F8ettY8k', 'm0H56KpKLHA', 'ygRQRgR11Zg', 'UriwETsgsqg', 'z1Xv6Pa0toE', '1Ni8KOzRzuI', 'yu-G9kEKdTo', 'oe7Cz-dxSBY']


### task type ###
# 82
create = ['mZZJYDfmgeg', 'XN3N5K2axpw', 'WIIjq2GexIw', 'ZT1dvq6yacQ', 'uUBVc8Ugz0k', 'Nu_By3eTpoc', 'ZeVRqW2J3UY', 'nnzPJv5XIws', '-szevr-BRZE', 'KLLqGcgxQEw', 'GFd7kLvhc2Q', '73lxEIKyX8M', 'eDG1c6a6uqc', 'Rcsy2HRuiyA', 'Ag6D8RGQnjw', 'CxdRXDN1fkA', 'dJ_qCDWNvXU', 'VDMOFa8iRqo', 'mQjCKgEPs8k', 'pn81__TovpY', 'ZmTxw3UbMO4', 'kz5dJ9SCu4M', 'yJ7VzfG2ONo', 'JNznnqX6SsE', 'dKUomyn1TYQ', 'h281yamVFDc', '5AU2vJU-QJM', 'yYOysPt5gic', '6CJryveLzvI', 'ZY11rbwCaMM', 'xTARWxkTJw0', 'WcD8bG2VB_s', 'ta5IB2wy6ic', '5ywy531EMNA', 'sM81wJ7GDrI', '1Ni8KOzRzuI', 'sij_wNj0doI', 'A_qivvTkijw', 'S0luUzNRtq0', 'eyD2iwXOeFM', 'kPGwDxo5Yf4', 'bg3orsnRCVE', 'HFp5uH12wkc', 'Xh_Awznyc7s', 'cGn_oZPotZA', 'ynmdOz_D1R4', 'Cvv1wiqKMHc', 'EnjZHOb6qNE', 'r6JmI35r5E8', 'AnWGek4P_dY', '7IcOJEEObA0', '-wlSMSl02Xs', 'IICwmc4WX2E', 'Eeu5uL6r2rg', 'k0koOhfXv_s', '4WaXJs9RR3E', 'T1j7Yq5-cIs', 'ihCwjLj31hY', '2Xyfgwj92v0', 'oe7Cz-dxSBY', 'UZJ0nmB3epQ', 'T5MbMuoNQ1k', 'N3c81EPZ51Q', 's4coMAU80U4', '7oXrT1CqLCY', 'uMgpr6X5asI', 'AbhW9YbQ0fM', 'bQKTjz0JKhg', 'SXQHgJHYQgc', 'Df9F8ettY8k', 'ntwi2Unh3JQ', 'ysHg9vOMe_4', 'OcjCNqfRgP0', 'WoDZQRGyuHA', 'bxXXCP0AE5A', 'yeT52sDtYEU', 'Y84sqS2Nljs', 'XFYHIg8U--4', 'jGsEBwiKnCI', 'kNsjE4HO7tE', 'UriwETsgsqg', 'b2EZggyT5O4']
# 27
fix = ['1oiCLxngvBo', 'PyWZYHy17As', '2OoebJA2mnE', '-xCtbeecgKQ', 'z1Xv6Pa0toE', 'T622Ec77ZPY', '9mjXFA1TMTI', 'jhAklPzn0XQ', 'QzS7Z80poKo', 'bwxvH99sLqw', 'mUq6l7N6zuk', 'ZORD4y7dL08', 'Czi_ZirnzRo', 'BzxPDw6ezEc', 'yu-G9kEKdTo', 'tb1L7Rsm1U8', 'mwpb65gm1e0', 'zMqzjMrxNR0', '0fxL8v2dMho', '8DgsLNa3ums', 'e3StC_4qemI', 'ntYwKXN82QU', '2xXPSfQBP-w', 'm0H56KpKLHA', '1dALzTPQWJg', 'ygRQRgR11Zg', 'mj1Fu3-XQpI']
# 11
use = ['u00iLnvVgFc', '-6tnn1G1dRg', '0SMzqWV6xxs', '_Yb6xLqvsf0', 'rqBiByEbMHc', '0TLQg_b1v5Q', 'Vrz25x3qnTY', 'BotYnPhByWg', 'djvLEfwwQPU', 'wvC3_Rs4mXs', 'CdZQF4DDAxM']


### categories ###
ane = ['mZZJYDfmgeg', 'XN3N5K2axpw', 'WIIjq2GexIw', '1oiCLxngvBo', 'ZT1dvq6yacQ', 'PyWZYHy17As', 'uUBVc8Ugz0k', 'Nu_By3eTpoc', 'ZeVRqW2J3UY', 'u00iLnvVgFc']
cnov = ['2OoebJA2mnE', '-xCtbeecgKQ', '-6tnn1G1dRg', 'z1Xv6Pa0toE', 'T622Ec77ZPY', '9mjXFA1TMTI', 'jhAklPzn0XQ', 'QzS7Z80poKo', 'bwxvH99sLqw', 'mUq6l7N6zuk']
cne = ['0SMzqWV6xxs', '_Yb6xLqvsf0', 'nnzPJv5XIws', 'ZORD4y7dL08', '-szevr-BRZE', 'KLLqGcgxQEw', 'Czi_ZirnzRo', 'GFd7kLvhc2Q', '73lxEIKyX8M', 'eDG1c6a6uqc']
enc = ['Rcsy2HRuiyA', 'Ag6D8RGQnjw', 'CxdRXDN1fkA', 'dJ_qCDWNvXU', 'VDMOFa8iRqo', 'mQjCKgEPs8k', 'BzxPDw6ezEc', 'pn81__TovpY', 'ZmTxw3UbMO4', 'kz5dJ9SCu4M']
fne = ['yJ7VzfG2ONo', 'JNznnqX6SsE', 'dKUomyn1TYQ', 'h281yamVFDc', '5AU2vJU-QJM', 'yYOysPt5gic', '6CJryveLzvI', 'ZY11rbwCaMM', 'xTARWxkTJw0', 'WcD8bG2VB_s']
health = ['ta5IB2wy6ic', 'rqBiByEbMHc', '5ywy531EMNA', 'sM81wJ7GDrI', '0TLQg_b1v5Q', '1Ni8KOzRzuI', 'Vrz25x3qnTY', 'sij_wNj0doI', 'BotYnPhByWg', 'djvLEfwwQPU']
hnc = ['A_qivvTkijw', 'S0luUzNRtq0', 'eyD2iwXOeFM', 'kPGwDxo5Yf4', 'bg3orsnRCVE', 'HFp5uH12wkc', 'Xh_Awznyc7s', 'cGn_oZPotZA', 'ynmdOz_D1R4', 'yu-G9kEKdTo']
hnt = ['Cvv1wiqKMHc', 'EnjZHOb6qNE', 'r6JmI35r5E8', 'AnWGek4P_dY', '7IcOJEEObA0', '-wlSMSl02Xs', 'IICwmc4WX2E', 'Eeu5uL6r2rg', 'k0koOhfXv_s', '4WaXJs9RR3E']
hng = ['tb1L7Rsm1U8', 'T1j7Yq5-cIs', 'ihCwjLj31hY', '2Xyfgwj92v0', 'mwpb65gm1e0', 'oe7Cz-dxSBY', 'zMqzjMrxNR0', 'UZJ0nmB3epQ', 'T5MbMuoNQ1k', '0fxL8v2dMho']
pcns = ['8DgsLNa3ums', 'N3c81EPZ51Q', 'e3StC_4qemI', 'ntYwKXN82QU', 's4coMAU80U4', '7oXrT1CqLCY', 'uMgpr6X5asI', 'AbhW9YbQ0fM', 'bQKTjz0JKhg', 'SXQHgJHYQgc']
pna = ['Df9F8ettY8k', 'ntwi2Unh3JQ', 'ysHg9vOMe_4', 'OcjCNqfRgP0', 'WoDZQRGyuHA', 'wvC3_Rs4mXs', 'bxXXCP0AE5A', '2xXPSfQBP-w', 'yeT52sDtYEU', 'Y84sqS2Nljs']
snf = ['XFYHIg8U--4', 'm0H56KpKLHA', '1dALzTPQWJg', 'ygRQRgR11Zg', 'jGsEBwiKnCI', 'kNsjE4HO7tE', 'mj1Fu3-XQpI', 'CdZQF4DDAxM', 'UriwETsgsqg', 'b2EZggyT5O4']


## 42 videos for IRR ##
irr_vids = ['Nu_By3eTpoc', 'ZeVRqW2J3UY', 'u00iLnvVgFc', 'QzS7Z80poKo', 'bwxvH99sLqw', 'mUq6l7N6zuk', 'Czi_ZirnzRo', 'GFd7kLvhc2Q', '73lxEIKyX8M', 'eDG1c6a6uqc', 'BzxPDw6ezEc', 'pn81__TovpY', 'ZmTxw3UbMO4', 'kz5dJ9SCu4M', 'ZY11rbwCaMM', 'xTARWxkTJw0', 'WcD8bG2VB_s', 'Vrz25x3qnTY', 'sij_wNj0doI', 'BotYnPhByWg', 'djvLEfwwQPU', 'cGn_oZPotZA', 'ynmdOz_D1R4', 'yu-G9kEKdTo', 'IICwmc4WX2E', 'Eeu5uL6r2rg', 'k0koOhfXv_s', '4WaXJs9RR3E', 'UZJ0nmB3epQ', 'T5MbMuoNQ1k', '0fxL8v2dMho', 'AbhW9YbQ0fM', 'bQKTjz0JKhg', 'SXQHgJHYQgc', 'bxXXCP0AE5A', '2xXPSfQBP-w', 'yeT52sDtYEU', 'Y84sqS2Nljs', 'mj1Fu3-XQpI', 'CdZQF4DDAxM', 'UriwETsgsqg', 'b2EZggyT5O4']


## Creation 48 / Annotation datasets
creation = ['mZZJYDfmgeg', 'XN3N5K2axpw', 'WIIjq2GexIw', '2OoebJA2mnE', '-xCtbeecgKQ', '-6tnn1G1dRg', '0SMzqWV6xxs', '_Yb6xLqvsf0', 'nnzPJv5XIws', 'Rcsy2HRuiyA', 'Ag6D8RGQnjw', 'CxdRXDN1fkA', 'yJ7VzfG2ONo', 'JNznnqX6SsE', 'dKUomyn1TYQ', 'ta5IB2wy6ic', 'rqBiByEbMHc', '5ywy531EMNA', 'A_qivvTkijw', 'S0luUzNRtq0', 'eyD2iwXOeFM', 'Cvv1wiqKMHc', 'EnjZHOb6qNE', 'r6JmI35r5E8', 'tb1L7Rsm1U8', 'T1j7Yq5-cIs', 'ihCwjLj31hY', '8DgsLNa3ums', 'N3c81EPZ51Q', 'e3StC_4qemI', 'Df9F8ettY8k', 'ntwi2Unh3JQ', 'ysHg9vOMe_4', 'XFYHIg8U--4', 'm0H56KpKLHA', '1dALzTPQWJg', 'PyWZYHy17As', '9mjXFA1TMTI', 'KLLqGcgxQEw', 'VDMOFa8iRqo', 'yYOysPt5gic', '1Ni8KOzRzuI', 'HFp5uH12wkc', '-wlSMSl02Xs', 'oe7Cz-dxSBY', '7oXrT1CqLCY', 'wvC3_Rs4mXs', 'kNsjE4HO7tE']
annotation = ['1oiCLxngvBo', 'ZT1dvq6yacQ', 'uUBVc8Ugz0k', 'Nu_By3eTpoc', 'ZeVRqW2J3UY', 'u00iLnvVgFc', 'z1Xv6Pa0toE', 'T622Ec77ZPY', 'jhAklPzn0XQ', 'QzS7Z80poKo', 'bwxvH99sLqw', 'mUq6l7N6zuk', 'ZORD4y7dL08', '-szevr-BRZE', 'Czi_ZirnzRo', 'GFd7kLvhc2Q', '73lxEIKyX8M', 'eDG1c6a6uqc', 'dJ_qCDWNvXU', 'mQjCKgEPs8k', 'BzxPDw6ezEc', 'pn81__TovpY', 'ZmTxw3UbMO4', 'kz5dJ9SCu4M', 'h281yamVFDc', '5AU2vJU-QJM', '6CJryveLzvI', 'ZY11rbwCaMM', 'xTARWxkTJw0', 'WcD8bG2VB_s', 'sM81wJ7GDrI', '0TLQg_b1v5Q', 'Vrz25x3qnTY', 'sij_wNj0doI', 'BotYnPhByWg', 'djvLEfwwQPU', 'kPGwDxo5Yf4', 'bg3orsnRCVE', 'Xh_Awznyc7s', 'cGn_oZPotZA', 'ynmdOz_D1R4', 'yu-G9kEKdTo', 'AnWGek4P_dY', '7IcOJEEObA0', 'IICwmc4WX2E', 'Eeu5uL6r2rg', 'k0koOhfXv_s', '4WaXJs9RR3E', '2Xyfgwj92v0', 'mwpb65gm1e0', 'zMqzjMrxNR0', 'UZJ0nmB3epQ', 'T5MbMuoNQ1k', '0fxL8v2dMho', 'ntYwKXN82QU', 's4coMAU80U4', 'uMgpr6X5asI', 'AbhW9YbQ0fM', 'bQKTjz0JKhg', 'SXQHgJHYQgc', 'OcjCNqfRgP0', 'WoDZQRGyuHA', 'bxXXCP0AE5A', '2xXPSfQBP-w', 'yeT52sDtYEU', 'Y84sqS2Nljs', 'ygRQRgR11Zg', 'jGsEBwiKnCI', 'mj1Fu3-XQpI', 'CdZQF4DDAxM', 'UriwETsgsqg', 'b2EZggyT5O4']

# Audio duration
audio_q1 = ['yeT52sDtYEU', 'Xh_Awznyc7s', 'cGn_oZPotZA', 'ta5IB2wy6ic', '1Ni8KOzRzuI', 'sM81wJ7GDrI', '5ywy531EMNA', '4WaXJs9RR3E', 'EnjZHOb6qNE', '1dALzTPQWJg', 'UriwETsgsqg', 'zMqzjMrxNR0', 'tb1L7Rsm1U8', '8DgsLNa3ums', 's4coMAU80U4', 'AbhW9YbQ0fM', 'Czi_ZirnzRo', 'eDG1c6a6uqc', '73lxEIKyX8M', '1oiCLxngvBo', 'pn81__TovpY', 'BzxPDw6ezEc', 'CxdRXDN1fkA', 'mUq6l7N6zuk', 'T622Ec77ZPY', 'QzS7Z80poKo', '-6tnn1G1dRg', 'bwxvH99sLqw', 'JNznnqX6SsE', 'yJ7VzfG2ONo']
audio_q2 = ['2xXPSfQBP-w', 'OcjCNqfRgP0', 'S0luUzNRtq0', 'BotYnPhByWg', 'djvLEfwwQPU', '0TLQg_b1v5Q', '7IcOJEEObA0', 'IICwmc4WX2E', 'm0H56KpKLHA', 'UZJ0nmB3epQ', 'oe7Cz-dxSBY', 'N3c81EPZ51Q', 'bQKTjz0JKhg', 'KLLqGcgxQEw', 'ZORD4y7dL08', 'Nu_By3eTpoc', 'XN3N5K2axpw', 'mZZJYDfmgeg', 'dJ_qCDWNvXU', 'kz5dJ9SCu4M', 'Ag6D8RGQnjw', 'z1Xv6Pa0toE', '-xCtbeecgKQ', 'jhAklPzn0XQ', '5AU2vJU-QJM', 'yYOysPt5gic', 'WcD8bG2VB_s', 'ZY11rbwCaMM', 'dKUomyn1TYQ', '6CJryveLzvI']
audio_q3 = ['Y84sqS2Nljs', 'ysHg9vOMe_4', 'A_qivvTkijw', 'kPGwDxo5Yf4', 'HFp5uH12wkc', 'sij_wNj0doI', 'rqBiByEbMHc', 'Vrz25x3qnTY', 'AnWGek4P_dY', 'Eeu5uL6r2rg', '-wlSMSl02Xs', 'r6JmI35r5E8', 'k0koOhfXv_s', 'ygRQRgR11Zg', 'b2EZggyT5O4', 'CdZQF4DDAxM', 'mwpb65gm1e0', 'ihCwjLj31hY', 'e3StC_4qemI', '7oXrT1CqLCY', 'ntYwKXN82QU', '0SMzqWV6xxs', 'GFd7kLvhc2Q', '-szevr-BRZE', 'u00iLnvVgFc', 'mQjCKgEPs8k', 'Rcsy2HRuiyA', '9mjXFA1TMTI', 'h281yamVFDc', 'xTARWxkTJw0']
audio_q4 = ['wvC3_Rs4mXs', 'WoDZQRGyuHA', 'bxXXCP0AE5A', 'ntwi2Unh3JQ', 'Df9F8ettY8k', 'eyD2iwXOeFM', 'yu-G9kEKdTo', 'bg3orsnRCVE', 'ynmdOz_D1R4', 'Cvv1wiqKMHc', 'mj1Fu3-XQpI', 'kNsjE4HO7tE', 'XFYHIg8U--4', 'jGsEBwiKnCI', '0fxL8v2dMho', 'T1j7Yq5-cIs', 'T5MbMuoNQ1k', '2Xyfgwj92v0', 'uMgpr6X5asI', 'SXQHgJHYQgc', 'nnzPJv5XIws', '_Yb6xLqvsf0', 'ZT1dvq6yacQ', 'WIIjq2GexIw', 'uUBVc8Ugz0k', 'ZeVRqW2J3UY', 'PyWZYHy17As', 'VDMOFa8iRqo', 'ZmTxw3UbMO4', '2OoebJA2mnE']


if __name__ == "__main__":

    scripts = []
    num_types = []

    # for audio distribution
    audio_durations_q1 = []
    audio_durations_q2 = []
    audio_durations_q3 = []
    audio_durations_q4 = []

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
                    # if vid in audio_q4:
                    if vid in creation:
                        print (vid) 
                        fp = os.path.join (cat_dir, file)
                        script_data = read_json (fp)
                        # if (script_data['audio_portion'] <= 0.8):
                        scripts.append (script_data)
                        num_types.append (script_data['total'])

                        # for audio distribution
                        # ad = script_data['audio_duration']
                        # if (ad <= 295.65):
                        #     audio_durations_q1.append (vid)
                        # elif (ad <= 341.13):
                        #     audio_durations_q2.append (vid)
                        # elif (ad <= 399.395):
                        #     audio_durations_q3.append (vid)
                        # else:
                        #     audio_durations_q4.append (vid)

    # print (len(scripts))
    # detail = analyze_detail_info (scripts)


    print (len(scripts))
    analyzed_data = analyze_total (scripts)
    fn = os.path.join (SAVE_DIR, 'analyzed_creation_dataset.json')
    write_json (fn, analyzed_data)


    # audio_durations = [audio_durations_q1, audio_durations_q2, audio_durations_q3, audio_durations_q4]
    # for i in range (4):
    #     print ('*********')
    #     print (audio_durations[i])

    ## For visualization
    # time_type_data = analyze_type_with_time (scripts)
    # visualize_time_data (time_type_data)

    # print (num_types)


    # assertion
    # tot_por = 0
    # time_por = 0
    # for type in analyzed_data['count']['sections']:
    #     tot_por += analyzed_data['count']['sections'][type]['portion']
    # for type in analyzed_data['time_portion']['sections']:
    #     time_por += analyzed_data['time_portion']['sections'][type]['time']
    # print (tot_por)
    # print (time_por)



                    


