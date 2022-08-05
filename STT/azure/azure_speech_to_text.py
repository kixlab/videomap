############
# This file is for extracting script and timestamp for audio (wav) file
# If you have no mp3 or wav file, make sure you call function 'download_mp3 (fp, vid)' to download the mp3 file
# After downloading mp3 file, convert it to wav file 
# check helper functions to process audio files
# there should be empty category folders in input_root location
# e.g. ./../audio/Arts and Entertainment, ./../audio/Cars & Other Vehicles, etc

## output
# There are 2 output json files
# 1. [video_id].json : contains lexical segments
# 2. [video_id]_ts.json : contains words with timestamp

# Two files will be saved in category folders in save_root location
# e.g. ./transcript/Arts and Entertainment, ./transcript/Cars & Other Vehicles, etc

############

from pydub import AudioSegment
from pytube import YouTube
import time
import os
import json
import wave
import azure.cognitiveservices.speech as speechsdk


# microsoft azure key and region for suing API
subscription = "f5f1533f669947bba6dbe5f7bf15929f"
region = "eastus"

# input audio root, save root
input_root = './../audio/'
save_root = './transcript/'


# video lists to extract script

# first_vids = ['ZT1dvq6yacQ', 'h281yamVFDc', '2Xyfgwj92v0', 'z1Xv6Pa0toE', 'kPGwDxo5Yf4', 'ntYwKXN82QU', 'ZORD4y7dL08', 'AnWGek4P_dY', 'OcjCNqfRgP0', 'dJ_qCDWNvXU', '0TLQg_b1v5Q', 'jGsEBwiKnCI']
second_vids = ['VEplLGXFLFw', '5AU2vJU-QJM', 'mwpb65gm1e0', 'T622Ec77ZPY', 'bg3orsnRCVE', 's4coMAU80U4', '-szevr-BRZE', '7IcOJEEObA0', 'WoDZQRGyuHA', 'VDMOFa8iRqo', '1Ni8KOzRzuI', 'kNsjE4HO7tE']
# third_vids = ['EYL1tYGwYY0', 'yYOysPt5gic', 'oe7Cz-dxSBY', 'HCi5TT5JNCU', 'HFp5uH12wkc', '7oXrT1CqLCY', 'KLLqGcgxQEw', 'R7fBwFAq7TI', 'wvC3_Rs4mXs', 'mQjCKgEPs8k', 'sM81wJ7GDrI', 'ygRQRgR11Zg']

vids = ['T622Ec77ZPY']

# download video from youtube
def download_mp3(fp, vid):
    try:
        yt = YouTube("youtu.be/" + vid)
    except:
        print("Connection Error")

    mp3files = yt.streams.filter(only_audio=True).first()

    try:
        mp3files.download(fp, vid+".mp3")
    except:
        print("Some Error!")

# helper functions for processing wav file
def mp3_to_wav(audio_file_name):
    if audio_file_name.split('.')[1] == 'mp3':
        sound = AudioSegment.from_file(audio_file_name)
        audio_file_name = audio_file_name.split('.')[0] + '.wav'
        sound.export(audio_file_name, format="wav")

def frame_rate_channel(audio_file_name):
    with wave.open(audio_file_name, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        return frame_rate, channels

def modify_frame_rate (audio_file_name, frame_rate):
    sound = AudioSegment.from_file(audio_file_name)
    sound = sound.set_frame_rate(frame_rate)
    sound.export(audio_file_name, format="wav")

def stereo_to_mono(audio_file_name):
    sound = AudioSegment.from_file(audio_file_name)
    sound = sound.set_channels(1)
    sound.export(audio_file_name, format="wav")

# helper function to change time unit
def change_sec_unit (input_time):
    return input_time / 10000000

# extract script from azure stt
def recognize_from_file (vid, audio_cat, save_cat):
    audio_fp = audio_cat + '/' + vid + '.wav'
    script_save_fp = save_cat + '/' + vid + '.json'
    ts_save_fp = save_cat + '/' + vid + '_ts.json'
    # print (audio_fp, script_save_fp, ts_save_fp)

    speech_config = speechsdk.SpeechConfig(subscription=subscription, region=region)
    speech_config.speech_recognition_language="en-US"
    speech_config.request_word_level_timestamps ()
    speech_config.output_format = speechsdk.OutputFormat (1)


    audio_config = speechsdk.audio.AudioConfig(filename=audio_fp)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    # Variable to monitor status
    done = False

    # Service callback for recognition text 
    transcript_lexical_list = []
    confidence_list = []
    words = []
    def parse_azure_result(evt):
        response = json.loads(evt.result.json)
        confidence_list_temp = [item.get('Confidence') for item in response['NBest']]
        max_confidence_index = confidence_list_temp.index(max(confidence_list_temp))
        confidence_list.append(response['NBest'][max_confidence_index]['Confidence'])
        transcript_lexical_list.append({"segment": response['NBest'][max_confidence_index]['Lexical']})
        words.extend(response['NBest'][max_confidence_index]['Words'])

    
    # Service callback that stops continuous recognition upon receiving an event `evt`
    def stop_cb(evt):
        print('CLOSING on {}'.format(evt))
        speech_recognizer.stop_continuous_recognition()
        nonlocal done
        done = True

        # change time unit and remove unnecessary entity
        modified_ts = []
        for t in words:
            word = t['Word']
            start = round (change_sec_unit(t['Offset']), 3)
            end = round (change_sec_unit (t['Offset'] + t['Duration']), 3)
            t_obj = {"word" : word, 'start': start, 'end': end}
            modified_ts.append (t_obj)

        with open (script_save_fp, "w") as script:
            json.dump (transcript_lexical_list, script)

        with open (ts_save_fp, "w") as timestamp:
            json.dump (modified_ts, timestamp)

        print("task complete")



    # Connect callbacks to the events fired by the speech recognizer
    # speech_recognizer.recognizing.connect(lambda evt: print('RECOGNIZING: {}'.format(evt)))
    speech_recognizer.recognized.connect(parse_azure_result)
    # speech_recognizer.session_started.connect(lambda evt: print('SESSION STARTED: {}'.format(evt)))
    # speech_recognizer.session_stopped.connect(lambda evt: print('SESSION STOPPED {}'.format(evt)))
    # speech_recognizer.canceled.connect(lambda evt: print('CANCELED {}'.format(evt)))
    # stop continuous recognition on either session stopped or canceled events
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Start continuous speech recognition
    speech_recognizer.start_continuous_recognition()
    while not done:
        time.sleep(.5)
        
if __name__ == "__main__":
    for root, dirs, files in os.walk (input_root):
        for dir_name in dirs:
            print ('-' * 30)
            print ('directory :', dir_name)
            audio_category_dir = input_root + dir_name
            save_category_dir = save_root + dir_name
            files = os.listdir(audio_category_dir)
            for file in files:
                vid = file.split('.')[0]
                extension = file.split('.')[1]
                if (extension != 'wav'):
                    continue
                if (vid in vids):
                    print (vid)

                    # preprocess audio file before extracting script
                    audio_fp = audio_category_dir + '/' + file
                    fr, c = frame_rate_channel (audio_fp)
                    if (fr != 16000):
                        modify_frame_rate (audio_fp, 16000)
                    if (c > 1):
                        stereo_to_mono (audio_fp)

                    recognize_from_file (vid, audio_category_dir, save_category_dir)





