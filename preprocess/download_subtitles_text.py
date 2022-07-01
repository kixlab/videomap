from youtube_transcript_api import YouTubeTranscriptApi
# from nltk.tokenize import sent_tokenize
# from rpunct import RestorePuncts
import csv
import json
import os


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
            # duration = transcript[-1]["start"]
            # transcript = expand_sentence(transcript)
            # rpunct = RestorePuncts()
            # transcript = rpunct.punctuate(transcript)
            # transcript = tokenize(transcript)
            return transcript
        except:
            try:
                transcript = transcript_list.find_generated_transcript([
                    'en'])
                transcript = transcript.fetch()
                # duration = transcript[-1]["start"]
                # transcript = expand_sentence(transcript)
                # rpunct = RestorePuncts()
                # transcript = rpunct.punctuate(transcript)
                # transcript = tokenize(transcript)
                return transcript
            except:
                return "error", 0

    except Exception as e:
        return "error", 0


def save_as_text(video_id, script):
    with open('./../data_script/'+video_id+'.txt', 'w') as f:
        for sentence in script:
            f.write(sentence)
            f.write('\n')


def save_as_json(video_id, script):
    with open('./../data_script/'+video_id+'.json', 'w') as f:
        json.dump(script, f)


def save_as_category_json(video_id, category, script):
    MYDIR = "./../data_script/"+category
    CHECK_FOLDER = os.path.isdir(MYDIR)
    if not CHECK_FOLDER:
        os.makedirs(MYDIR)
    with open('./../data_script/'+category+"/"+video_id+'.json', 'w') as f:
        json.dump(script, f)


def download_subtitles_from_howto100m():
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

    with open('./../data_script/0_meta.json', 'w') as fp:
        json.dump(video_meta_info, fp)
    with open('./../data_script/0_category.json', 'w') as fp:
        json.dump(video_category_info, fp)
    f.close()


def download_subtitles_from_list():
    video_ids = ["BotYnPhByWg", "djvLEfwwQPU"]
    # video_ids = ["yJ7VzfG2ONo", "tb1L7Rsm1U8", "Rcsy2HRuiyA"]
    for vid in video_ids:
        script = generate_transcript(vid)
        save_as_json(vid, script)


def download_subtitles_from_text():
    video_category_info = {}
    with open('./data/selected_video_list.txt', 'r') as f:
        videos = f.readlines()
        for video in videos:
            video = video.strip()
            if video == "" or video == "\t":
                continue
            blank = video.find("\t")
            video_id = video[:blank]
            category = video[blank+1:]
            # if not category in video_category_info:
            #     video_category_info[category] = [video_id]
            # else:
            #     video_list = video_category_info[category]
            #     video_list.append(video_id)
            #     video_category_info[category] = video_list

            script = generate_transcript(video_id)
            save_as_category_json(video_id, category, script)


def main():
    download_subtitles_from_list()


if __name__ == "__main__":
    main()
