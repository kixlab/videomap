import csv
from googleapiclient.discovery import build

# api_key = "AIzaSyAu43HmXnR-5mbxn-SAxU8SFGpzF8kUALY"
api_key = "AIzaSyAazzKsiPmzxymKDWznYK8lhpdaRyb0Fo4"
youtube = build('youtube', 'v3', developerKey=api_key)

video_ids = ['95hUxNBeD3E', 'eW_ztUkNKZQ']


def get_duration_and_date(vid):
    pl_request = youtube.videos().list(
        part='contentDetails, snippet',
        id=vid
    )
    published = ""
    duration = ""
    pl_response = pl_request.execute()
    for item in pl_response['items']:
        # print(item.keys())
        if 'snippet' in item:
            # publishedAt: '2010-10-31T03:29:25Z'
            published = item['snippet']['publishedAt']
        if 'contentDetails' in item:
            # duration: PT#M#S / PT#H#M#S / P#DT#H#M#S
            duration = item['contentDetails']['duration']
    return duration, published


def parse_duration(duration):
    if "D" in duration or "H" in duration:
        return -1
    midx = duration.find('M')
    sidx = duration.find('S')
    if midx == -1 or sidx == -1:
        return -1
    minute = duration[2:midx]
    seconds = duration[midx+1:sidx]
    if minute == "":
        minute = 0
    if seconds == "":
        seconds = 0
    return int(minute)*60+int(seconds)


def get_videos_from_howto100m():
    f = open('./../HowTo100M/HowTo100M_v1.csv', 'r')
    rdr = csv.reader(f)
    video_info = []
    count = 0
    for line in rdr:
        if count < 9822:
            count += 1
            continue
        vid = line[0]
        category = line[1]
        duration, published = get_duration_and_date(vid)
        if duration == "" or published == "":
            continue
        duration = parse_duration(duration)
        if duration == -1:
            continue
        published = published[:4]
        if published > "2017" and duration >= 300:
            print(vid, category, duration, published)
            video_info.append([vid, category, duration, published])
        count += 1
    return video_info


def get_videos_from_list():
    video_ids = ["UHA1Q5JK3_A"]
    for vid in video_ids:
        duration, published = get_duration_and_date(vid)
        if duration == "" or published == "":
            continue
        duration = parse_duration(duration)
        if duration == -1:
            continue
        published = published[:4]


def save_to_text(video_info):
    with open('video_info.txt', 'w') as f:
        for line in video_info:
            f.write(line)
            f.write('\n')


def main():
    video_info = get_videos_from_howto100m()
    save_to_text(video_info)
    # get_videos_from_list()


if __name__ == "__main__":
    main()
