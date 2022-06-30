import os
import glob


path = './data_v2'
with open('HowTo100M_v2_merged.txt', 'w') as wf:
    for filename in glob.glob(os.path.join(path, '*.txt')):
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            for line in f.readlines():
                wf.write(line)
wf.close()
