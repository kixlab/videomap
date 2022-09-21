from importlib.metadata import distribution
import os
import json
from pydub import AudioSegment

def video_duration (path):
    audio = AudioSegment.from_file(path)
    audio.duration_seconds == (len(audio) / 1000.0)
    return audio.duration_seconds

# get time distribution w/ narration and w/o narration
def get_time_distribution ():
    return 0

script_root = './data/processed/'
audio_root = './data/audio/'
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

            
                audio_fn = vid + '.wav'
                audio_file = os.path.join(audio_category_dir, audio_fn)
                # print (audio_file)
                total_length = video_duration (audio_file)
                
                script_json = os.path.join(category_dir, file)
                with open(script_json) as f:
                    script = json.load(f)

                duration = 0
                for line in script:
                    duration += (line['end'] - line['start'])
                    # if (ind == 0 or ind == len (script)):
                    #     continue
                    # if (ind == 0):
                    #     gap = (script[ind]['start'] - 0)
                    # elif (ind == len (script)):
                    #     gap = total_length - script[ind - 1]['end']
                    # else:
                    #     last_sentence = script[ind - 1]
                    #     gap = (script[ind]['start'] - last_sentence['end'])

                    # if (gap > 0):
                    #     duration += gap
                    

                distribution_result.append ({'video_id': vid, 'total': round (total_length, 3), 'audio': round (duration, 3), 'audio_portion': round (duration / total_length, 3), 'no_audio_portion': round (1-(duration / total_length), 3)})

        # print (len (distribution_result))

    total_length = 0
    total_duration = 0


    vids = []
    for video in distribution_result:
        total_length += video['total']
        total_duration += video['audio']
        # print (video)

    print ("total length : ", round (total_length, 3))
    print ("time w/ audio : ", round (total_duration, 3))
    print ("average portion : ", round (total_duration / total_length, 3))

    sorted_distribution_list = sorted(distribution_result, key=lambda k: k['audio_portion'])
        # for item in sorted_distribution_list:
        #     print (item)
        # print (len(sorted_distribution_list))


    output_file = './data/final/audio_portion/audio_portion_total.json'
    with open (output_file, "w") as json_file:
        json.dump (sorted_distribution_list, json_file)