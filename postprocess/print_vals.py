# just to help necessary values in nested json
import os
import json

def read_json (fp):
    with open (fp, 'r') as s:
        script = json.load (s)
    return script


ROOT_DIR = './data/final/'

fns = ['analyzed_total.json', 'analyzed_fix.json', 'analyzed_use.json']

if __name__ == "__main__":
    for root, dirs, files in os.walk (ROOT_DIR):
        for dir_name in dirs:
            cat_dir = os.path.join (ROOT_DIR, dir_name) 
            files = os.listdir(cat_dir)
            for file in files:
                if file in fns:
                    print ('*' * 30)
                    print (file)
                    fp = os.path.join (cat_dir, file)
                    af = read_json (fp)

                    tp = af['time_portion']
                    for level in tp:
                        print ('-' * 30)
                        print (level)

                        for item in tp[level]:
                            if item == "status" or item == 'context':
                                print (item, tp[level][item]['time'])


