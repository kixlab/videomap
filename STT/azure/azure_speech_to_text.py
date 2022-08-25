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

from turtle import down
from pydub import AudioSegment
from pytube import YouTube
import time
import os
import json
import wave
import azure.cognitiveservices.speech as speechsdk

# microsoft azure key and region for suing API
# sangkyung
# subscription = "f5f1533f669947bba6dbe5f7bf15929f"
# region = "eastus"

# saelyne
# subscription = "07f300fbfffa4ef19dc63ffb10337bc8"
# region = "eastus"

# juhoon
subscription = "73c70d0684014fcb9ef6c4f4b882ce55"
region = "eastus"

# input audio root, save root
input_root = './../audio/'
save_root = './transcript/'

# video lists for annotation in each date
# vids_0805 = ['ZT1dvq6yacQ', 'h281yamVFDc', '2Xyfgwj92v0', 'z1Xv6Pa0toE', 'kPGwDxo5Yf4', 'ntYwKXN82QU', 'ZORD4y7dL08', 'AnWGek4P_dY', 'OcjCNqfRgP0', 'dJ_qCDWNvXU', '0TLQg_b1v5Q', 'jGsEBwiKnCI']
# vids_0808 = ['VEplLGXFLFw', '5AU2vJU-QJM', 'mwpb65gm1e0', 'T622Ec77ZPY', 'bg3orsnRCVE', 's4coMAU80U4', '-szevr-BRZE', '7IcOJEEObA0']
# vids_0809 = ['WoDZQRGyuHA', 'VDMOFa8iRqo', '1Ni8KOzRzuI', 'kNsjE4HO7tE', 'EYL1tYGwYY0', 'yYOysPt5gic', 'oe7Cz-dxSBY', '9mjXFA1TMTI']
# vids_0810 = ['HFp5uH12wkc', '7oXrT1CqLCY', 'KLLqGcgxQEw', '-wlSMSl02Xs', 'wvC3_Rs4mXs', 'mQjCKgEPs8k', 'sM81wJ7GDrI', 'ygRQRgR11Zg']
# vids_0811 = ['uUBVc8Ugz0k', '6CJryveLzvI', 'zMqzjMrxNR0', 'jhAklPzn0XQ', 'Xh_Awznyc7s', 'uMgpr6X5asI', 'Czi_ZirnzRo', 'IICwmc4WX2E']
# vids_0812 = ['bxXXCP0AE5A', 'BzxPDw6ezEc', 'Vrz25x3qnTY', 'mj1Fu3-XQpI', 'Nu_By3eTpoc', 'ZY11rbwCaMM', 'UZJ0nmB3epQ', 'QzS7Z80poKo', 'jHsbUTwIl1A', 'AbhW9YbQ0fM']
# vids_0814 = ['GFd7kLvhc2Q', 'Eeu5uL6r2rg', '2xXPSfQBP-w', 'pn81__TovpY', 'sij_wNj0doI', 'CdZQF4DDAxM', 'ZeVRqW2J3UY', 'xTARWxkTJw0', '8cV5x4jP7EU', 'bwxvH99sLqw']
# vids_0815 = ['cGn_oZPotZA', 'bQKTjz0JKhg', '73lxEIKyX8M', 'k0koOhfXv_s', 'yeT52sDtYEU', 'ZmTxw3UbMO4', 'BotYnPhByWg', 'UriwETsgsqg', 'PyWZYHy17As', 'WcD8bG2VB_s']
# vids_0816 = ['0fxL8v2dMho', 'mUq6l7N6zuk', 'yu-G9kEKdTo', 'SXQHgJHYQgc', 'eDG1c6a6uqc', '4WaXJs9RR3E', 'Y84sqS2Nljs', 'kz5dJ9SCu4M', 'djvLEfwwQPU', 'b2EZggyT5O4']

# video list for creation
# vids_creation_1 = ['mZZJYDfmgeg', 'XN3N5K2axpw', 'WIIjq2GexIw', '2OoebJA2mnE', '-xCtbeecgKQ', '-6tnn1G1dRg', '0SMzqWV6xxs', '_Yb6xLqvsf0', 'nnzPJv5XIws', 'Rcsy2HRuiyA', 'Ag6D8RGQnjw', 'CxdRXDN1fkA']
# vids_creation_2 = ['yJ7VzfG2ONo', 'JNznnqX6SsE', 'dKUomyn1TYQ', 'A_qivvTkijw', 'S0luUzNRtq0', 'eyD2iwXOeFM', 'Cvv1wiqKMHc', 'EnjZHOb6qNE', 'r6JmI35r5E8', 'ta5IB2wy6ic', 'rqBiByEbMHc', '2YGEDsl7PO8']
# vids_creation_3 = ['tb1L7Rsm1U8', 'T1j7Yq5-cIs', 'ihCwjLj31hY', '8DgsLNa3ums', 'N3c81EPZ51Q', 'e3StC_4qemI', 'Df9F8ettY8k', 'ntwi2Unh3JQ', 'ysHg9vOMe_4', 'XFYHIg8U--4', 'm0H56KpKLHA', '1dALzTPQWJg']

# new_vids = ['YmHGiLGINV4', 'u00iLnvVgFc', 'cvZMHEu_Ojk', '1oiCLxngvBo', 'mmGVeV-BvhU']

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
    if audio_file_name.split('.')[-1] == 'mp3':
        sound = AudioSegment.from_file(audio_file_name)
        audio_file_name = audio_file_name.split('.')[0] + '.wav'
        sound.export(audio_file_name, format="wav")

def frame_rate_channel(audio_file_name):
    with wave.open(audio_file_name, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        # print (frame_rate)
        # print (channels)
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
    # for root, dirs, files in os.walk (input_root):
    #     for dir_name in dirs:
    #         print ('-' * 30)
    #         print ('directory :', dir_name)
    #         audio_category_dir = input_root + dir_name
    #         save_category_dir = save_root + dir_name
    #         files = os.listdir(audio_category_dir)
    #         for file in files:
    #             vid = file.split('.')[0]
    #             extension = file.split('.')[1]
    #             if (extension != 'wav'):
    #                 continue
    #             if (vid in new_vids):
    #                 print (vid)

    #                 # preprocess audio file before extracting script
    #                 audio_fp = audio_category_dir + '/' + file
    #                 fr, c = frame_rate_channel (audio_fp)
    #                 if (fr != 16000):
    #                     modify_frame_rate (audio_fp, 16000)
    #                 if (c > 1):
    #                     stereo_to_mono (audio_fp)

    #                 _, _ = frame_rate_channel (audio_fp)

    #                 recognize_from_file (vid, audio_category_dir, save_category_dir)


    new_vids = ['T5MbMuoNQ1k', 'ynmdOz_D1R4']
    # audio_path = '/Users/sangkyung/Desktop/Starlab/videomap/STT/audio/Hobbies and Crafts'

    # for vid in new_vids:
    #     fp = audio_path + '/' + vid + '.mp3'
    #     download_mp3 (audio_path, vid)
    #     mp3_to_wav (fp)

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
                if (vid in new_vids):
                    print (vid)

                    # preprocess audio file before extracting script
                    audio_fp = audio_category_dir + '/' + file
                    fr, c = frame_rate_channel (audio_fp)
                    if (fr != 16000):
                        modify_frame_rate (audio_fp, 16000)
                    if (c > 1):
                        stereo_to_mono (audio_fp)

                    _, _ = frame_rate_channel (audio_fp)

                    recognize_from_file (vid, audio_category_dir, save_category_dir)






