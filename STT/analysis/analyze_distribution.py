from importlib.metadata import distribution
import os
import json
from pydub import AudioSegment
import operator


def video_duration (path):
    audio = AudioSegment.from_file(path)
    audio.duration_seconds == (len(audio) / 1000.0)
    return audio.duration_seconds

htm_root = './final'
audio_root = './audio'
distribution_result = []
for root, dirs, files in os.walk (htm_root):
    for dir_name in dirs:
        # print ('-' * 30)
        # print('directory :', dir_name) #category
        category_dir = htm_root + "/" + dir_name
        audio_category_dir = audio_root + "/" + dir_name
        files = os.listdir(category_dir)
        for file in files:
            duration = 0
            vid = file.split('.')[0]
            audio_fn = vid + '.wav'
            audio_file = os.path.join(audio_category_dir, audio_fn)
            # print (audio_file)
            total_length = video_duration (audio_file)
            caption_json = os.path.join(category_dir, file)
            with open(caption_json) as f:
                raw_caption = json.load(f)
            for ind in range (len (raw_caption) + 1):
                # if (ind == 0 or ind == len (raw_caption) - 1):
                #     continue
                if (ind == 0):
                    continue
                    # gap = (raw_caption[ind]['start'] - 0)
                elif (ind == len (raw_caption)):
                    continue
                    # gap = total_length - raw_caption[ind - 1]['end']
                else:
                    last_sentence = raw_caption[ind - 1]
                    gap = (raw_caption[ind]['start'] - last_sentence['end'])
                if (gap > 0):
                    duration += gap
            

            distribution_result.append ({'video_id': file.split('.')[0], 'total': round (total_length, 3), 'no_audio': round (duration, 3), 'portion': round (duration / total_length, 3)})


print (len (distribution_result))

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

    if (video['portion'] > 0.214):
        vids.append (video['video_id'])

    # print (video)

print ("total length : ", round (total_length, 3))
print ("time w/o audio : ", round (total_duration, 3))
print ("average portion : ", round (total_duration / total_length, 3))
# for vid in vids:
#     print (vid)

# max_dur = 0
# max_vid = ''
# for video in distribution_result:
#     if (video['portion'] > max_dur):
#         max_dur = video['portion']
#         max_vid = video['video_id']

# print (max_dur)
# print (max_vid)
# print ('max_duration : ', max (duration_list))
# print ('min duration : ', min (duration_list))
# print ('max_portion : ', max (portion_list))
# print ('min_portion : ', min (portion_list))

sorted_distribution_list = sorted(distribution_result, key=lambda k: k['portion'])
# for item in sorted_distribution_list:
#     print (item)
# print (sorted_distribution_list)

output_file = './portion_analysis_exclude.json'
with open (output_file, "w") as json_file:
    json.dump (sorted_distribution_list, json_file)