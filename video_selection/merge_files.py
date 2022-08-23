import os
import glob


path = './data_all'
with open('HowTo100M_all_merged.txt', 'w') as wf:
    for filename in glob.glob(os.path.join(path, '*.txt')):
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            for line in f.readlines():
                wf.write(line)
wf.close()
