import os
import json

def read_json (fp):
    with open (fp, 'r') as s:
        script = json.load (s)
    return script


