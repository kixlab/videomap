from youtube_transcript_api import YouTubeTranscriptApi
from nltk.tokenize import sent_tokenize
from rpunct import RestorePuncts
import csv
import json


def expand_sentence(transcript):
    script = ""
    for info in transcript:
        text = info["text"]
        start = info["start"]
        duration = info["duration"]
        script += text
        script += " "
    script = script.replace('\n', ' ')
    return script


def tokenize(script):
    script_list = sent_tokenize(script)
    return script_list


def generate_transcript(video_id):
    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        # transcript_list = YouTubeTranscriptApi.get_transcripts("9Jja-kf5z4U",  languages=['en-US'])
        try:

            transcript = transcript_list.find_generated_transcript(['en-US'])
            # transcript = transcript_list.find_manually_created_transcript(['en-US'])
            transcript = transcript.fetch()
            duration = transcript[-1]["start"]
            transcript = expand_sentence(transcript)
            rpunct = RestorePuncts()
            transcript = rpunct.punctuate(transcript)
            script_list = tokenize(transcript)
            return script_list, duration
        except:
            try:
                transcript = transcript_list.find_generated_transcript([
                    'en'])
                transcript = transcript.fetch()
                duration = transcript[-1]["start"]
                transcript = expand_sentence(transcript)
                rpunct = RestorePuncts()
                transcript = rpunct.punctuate(transcript)
                script_list = tokenize(transcript)
                return script_list, duration
            except:
                return "error", 0

    except Exception as e:
        return "error", 0


def save_as_text(video_id, script):
    with open('./../data/'+video_id+'.txt', 'w') as f:
        for sentence in script:
            f.write(sentence)
            f.write('\n')


f = open('./../HowTo100M/HowTo100M_v1.csv', 'r')
rdr = csv.reader(f)
video_meta_info = {}
video_category_info = {}
count = 0
target_count_per_category = 10

for line in rdr:
    if count == 0:
        count += 1
        continue
    if line[1] in video_category_info and len(video_category_info[line[1]]) == target_count_per_category:
        continue
    if count == 12*target_count_per_category+1:
        break
    script, duration = generate_transcript(line[0])
    if script == "error":
        continue
    save_as_text(line[0], script)
    video_info = {}
    video_info["category_1"] = line[1]
    video_info["category_2"] = line[2]
    video_info["rank"] = line[3]
    video_info["task_id"] = line[4]
    video_info["sentence_count"] = len(script)
    video_info["rough_duration"] = duration
    video_meta_info[line[0]] = video_info
    count += 1

    if not line[1] in video_category_info:
        video_category_info[line[1]] = [line[0]]
    else:
        video_list = video_category_info[line[1]]
        video_list.append(line[0])
        video_category_info[line[1]] = video_list

with open('./../data/0_meta.json', 'w') as fp:
    json.dump(video_meta_info, fp)
with open('./../data/0_category.json', 'w') as fp:
    json.dump(video_category_info, fp)
f.close()
