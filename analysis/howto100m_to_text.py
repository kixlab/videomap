import csv

f = open('./../HowTo100M/HowTo100M_v1.csv', 'r')
rdr = csv.reader(f)
video_info = []
count = 0
for line in rdr:
    vid = line[0]
    category = line[1]
    video_info.append([vid, category])

with open('HowTo100M_v1.txt', 'w') as f:
    for line in video_info:
        f.write(line[0])
        f.write(', ')
        f.write(line[1])
        f.write('\n')
