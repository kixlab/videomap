import os
import json
from pydub import AudioSegment


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
    return audio.duration_seconds

# ----------------------------------------------------#
# ------------------ Analysis 1 ----------------------#
# ----------------------------------------------------#
TYPES = {'opening', 'closing', 'goal', 'motivation', 'briefing', 'subgoal', 'instruction', 'tool', 'warning', 'tip', 'justification', 'effect', 'status', 'context', 'tool specification', 'outcome', 'reflection', 'side note', 'self-promo', 'bridge', 'filler'}
CATEGORIES = {'greeting', 'overview', 'step', 'supplementary', 'explanation', 'description', 'conclusion', 'misc.'}
SECTIONS = {'intro', 'procedure', 'outro', 'misc.'}

# analyze count for each vid
# level = {type, category, section}
def analyze_count (data):
    total_count = len (data)
    # print (total_count)
    types = {}
    categories = {}
    sections = {}

    for line in data:
        type = line['type']
        category = line['category']
        section = line['section']

        # type
        if type not in types.keys():
            types[type] = {'count': 0}
            types[type]['count']=1
        else:
            types[type]['count']+=1

        # category
        if category not in categories.keys():
            categories[category] = {'count': 0}
            categories[category]['count']=1
        else:
            categories[category]['count']+=1   
        
        # section
        if section not in sections.keys():
            sections[section] = {'count': 0}
            sections[section]['count']=1
        else:
            sections[section]['count']+=1  

    counts = {'types': types, 'categories': categories, 'sections': sections}


    for level in counts:
        # types, cateogries, sections
        for item in counts[level]:
            count = counts[level][item]['count']
            portion = count / total_count
            counts[level][item]['portion'] = portion
    
    # print (count)
    return counts

# analyze time portion for each vid
# level = {type, category, section}
def analyze_time_portion (data):
    types = {}
    categories = {}
    sections = {}

    audio_duration = 0

    for line in data:
        type = line['type']
        category = line['category']
        section = line['section']
        line_duration = line['end'] - line['start']
        audio_duration += line_duration

        # type
        if type not in types.keys():
            types[type] = {'time': 0}
            types[type]['time']=line_duration
        else:
            types[type]['time']+=line_duration

        # category
        if category not in categories.keys():
            categories[category] = {'time': 0}
            categories[category]['time']=line_duration
        else:
            categories[category]['time']+=line_duration   
        
        # section
        if section not in sections.keys():
            sections[section] = {'time': 0}
            sections[section]['time']=line_duration
        else:
            sections[section]['time']+=line_duration

    times = {'types': types, 'categories': categories, 'sections': sections}
    for level in times:
        # types, cateogries, sections
        for item in times[level]:
            time = times[level][item]['time']
            portion = time / audio_duration
            times[level][item]['portion'] = portion
    
    # print (times)
    return audio_duration, times

# count unique number of types
# level = {type, category, section}
def get_unique_number (data):
    types = set()
    categories = set()
    sections = set()
    for line in data:
        type = line['type']
        category = line['category']
        section = line['section']

        assert type in TYPES
        assert category in CATEGORIES
        assert section in SECTIONS

        types.add (type)
        categories.add (category)
        sections.add (section)

    unique_count = {'types': {'items': list(types), 'number': len (types)}, 'categories': {'items': list(categories), 'number': len (categories)}, 'sections': {'items': list(sections), 'number': len (sections)}}
    
    return unique_count


# ----------------------------------------------------#
# ------------------ Analysis 3 ----------------------#
# ----------------------------------------------------#

def get_normalized_time (data, duration):
    
    ts_axis = [i/1000 for i in range (1000)]

    norm_ts_list = []
    for ts in ts_axis:
        norm_ts_obj = {}
        check = False
        for line in data:
            start = line['start'] / duration
            end = line['end'] / duration
            norm_ts_obj['norm_time'] = ts
            if start <= ts and ts < end:
                norm_ts_obj['type'] = line['type']
                norm_ts_obj['category'] = line['category']
                norm_ts_obj['section'] = line['section']
                check = True
                break
        if (not check):
            norm_ts_obj['type'] = 'none'
            norm_ts_obj['category'] = 'none'
            norm_ts_obj['section'] = 'none'

        norm_ts_list.append (norm_ts_obj)

    # print (norm_ts_list)
    return norm_ts_list


ROOT_DIR = './data/processed/'
SAVE_DIR = './data/analysis/'
AUDIO_DIR = './data/audio/'

vids = ['XFYHIg8U--4', 'm0H56KpKLHA', '1dALzTPQWJg', 'ygRQRgR11Zg', 'jGsEBwiKnCI', 'kNsjE4HO7tE', 'mj1Fu3-XQpI', 'CdZQF4DDAxM', 'UriwETsgsqg', 'b2EZggyT5O4']

if __name__ == "__main__":
    for root, dirs, files in os.walk (ROOT_DIR):
        for dir_name in dirs:

            print ('*' * 30)
            print ('directory :', dir_name)

            cat_dir = os.path.join (ROOT_DIR, dir_name)
            save_cat_dir = os.path.join (SAVE_DIR, dir_name)
            audio_cat_dir = os.path.join (AUDIO_DIR, dir_name)

            if not os.path.exists (save_cat_dir):
                os.makedirs (save_cat_dir)

            files = os.listdir(cat_dir)
            for file in files:
                vid = file.split('.')[0]

                # if vid in vids:
                if True:
                    print (vid)

                    fp = os.path.join (cat_dir, file)
                    script_data = read_json (fp)
                    # print (script_data)

                    audio_fp = os.path.join (audio_cat_dir, vid+'.wav')
                    duration = video_duration (audio_fp)


                    count = analyze_count (script_data)
                    audio_duration, time_portion = analyze_time_portion (script_data)
                    # unique count
                    unique_count = get_unique_number (script_data)


                    normalized_ts = get_normalized_time (script_data, duration)
                    analysis_data = {
                        'vid': vid, 
                        'total': len(script_data), 
                        'duration': duration, 
                        'audio_duration': audio_duration, 
                        'count': count, 
                        'time_portion': time_portion, 
                        'unique_count': unique_count,
                        'normalzied_ts': normalized_ts
                    }

                    save_fp = os.path.join (save_cat_dir, file)
                    write_json (save_fp, analysis_data)
                    




