import pandas as pd
import os

ROOT_DIR = "./data/csv"
OUTPUT_DIR = "./data/json"

type_hierarchy = {
    "greeting": ["opening", "closing"],
    "overview": ["goal", "motivation", "briefing"],
    "step": ["subgoal", "instruction", "tool"],
    "supplementary": ["warning", "tip"],
    "explanation": ["justification", "effect"],
    "description": ["status", "context"],
    "conclusion": ["outcome", "reflection"],
    "misc.": ["side note", "self-promo", "bridge", "filler"]
}

for filename in os.listdir(ROOT_DIR):
    vid = filename.split('.')[0]

    with open(os.path.join(ROOT_DIR, filename), 'r') as csv_file:
        if not "csv" in filename:
            continue

        print ('-' * 30)
        print (vid)
        data = pd.read_csv(csv_file)

        # drop unnecessary columns
        data.drop('P1', inplace=True, axis=1)
        data.drop('P2', inplace=True, axis=1)
        data.drop('Match', inplace=True, axis=1)

        data = data.rename(columns={'Final':'Low_type'})
        high_label = pd.DataFrame(columns=['High_type'])

        for ind, row in data.iterrows():
            low_label = row['Low_type']
            for key in type_hierarchy.keys():
                if (low_label in type_hierarchy[key]):
                    high_label.loc[ind] = [key]
        data = pd.concat([data, high_label], axis = 1)

        json_fp = OUTPUT_DIR + '/' + vid + '.json'
        data_json = data.to_json(json_fp, orient="records")
        print ("json file saved")


