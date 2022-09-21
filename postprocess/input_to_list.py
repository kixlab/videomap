### for convenience of handling input

N = 240
vid = []
dates = []
for i in range (N):
    if i<120:
        vid.append(input())
    else:
        dates.append (input())

date_dict={}
for i in range (120):
    date_dict[vid[i]] = dates[i]

print (date_dict)