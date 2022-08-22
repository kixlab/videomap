with open('HowTo100M_all_filtered.txt', 'w') as wf:
    with open('HowTo100M_all_merged.txt', 'r') as f:
        for line in f.readlines():
            info = line.split(",")
            if len(info) != 4:
                continue
            vid = info[0].strip()
            category = info[1].strip()
            duration = info[2].strip()
            date = info[3].strip()
            if duration == "error" or date == "error":
                continue
            if len(category) <= 1:
                continue
            time = duration.split(":")
            if len(time) == 1:
                continue
            if int(time[0]) < 5:
                continue
            wf.write(vid+", "+category+", "+duration+", "+date)
            wf.write('\n')


wf.close()
