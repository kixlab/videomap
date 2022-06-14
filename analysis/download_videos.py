
from pytube import YouTube

SAVE_PATH = "./../data_video"

# link of the video to be downloaded
video_ids = ["xWOoBJUqlbI"]

for vid in video_ids:
    try:
        yt = YouTube("youtu.be/"+vid)
    except:
        print("Connection Error")

    # filters out all the files with "mp4" extension
    mp4files = yt.streams.filter(file_extension='mp4')

    # get the video with the extension and
    # resolution passed in the get() function
    d_video = mp4files[0]
    try:
        # downloading the video
        d_video.download(SAVE_PATH)
    except:
        print("Some Error!")
print('Task Completed!')
