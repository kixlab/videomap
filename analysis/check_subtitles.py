from youtube_transcript_api import YouTubeTranscriptApi
from nltk.tokenize import sent_tokenize
# from rpunct import RestorePuncts

# Testing functions


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


def save_as_text(video_id, script):
    with open('./../data/'+video_id+'.txt', 'w') as f:
        for sentence in script:
            f.write(sentence)
            f.write('\n')


video_id = "9Jja-kf5z4U"
transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
transcript = transcript_list.find_manually_created_transcript([
    'en-US'])
transcript = transcript.fetch()
print(transcript)
print(transcript[-1]["start"])
transcript = expand_sentence(transcript)
print(transcript)
# rpunct = RestorePuncts()
# transcript = rpunct.punctuate(transcript)
# script_list = tokenize(transcript)
# script_list = tokenize(transcript)
# print(len(script_list))

# save_as_text(video_id, script_list)
