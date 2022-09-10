from email.mime import audio
import os
import json


# ----------------------------------------------------#
# --------------- Helper functions -------------------#
# ----------------------------------------------------#
def read_json (fp):
    with open (fp, 'r') as s:
        script = json.load (s)
    return script

def write_json (fp, script):
    with open(fp, "w") as json_file:
        json.dump(script, json_file)


# analyze total videos
def analyze_total (data):
    return

ROOT_DIR = './data/analysis/'

vids = ['XFYHIg8U--4', 'm0H56KpKLHA', '1dALzTPQWJg', 'ygRQRgR11Zg', 'jGsEBwiKnCI', 'kNsjE4HO7tE', 'mj1Fu3-XQpI', 'CdZQF4DDAxM', 'UriwETsgsqg', 'b2EZggyT5O4']

if __name__ == "__main__":

    scripts = []
    for root, dirs, files in os.walk (ROOT_DIR):
        for dir_name in dirs:

            print ('*' * 30)
            print ('directory :', dir_name)

            cat_dir = os.path.join (ROOT_DIR, dir_name)
            files = os.listdir(cat_dir)
            for file in files:
                vid = file.split('.')[0]
                if vid in vids:
                    fp = os.path.join (cat_dir, file)
                    script_data = read_json (fp)
                    scripts.append (script_data)

    analyze_total (scripts)

                    


