from analysis.create_dataset import ROOT_DIR
from sklearn.metrics import cohen_kappa_score
import csv
import os


def transform_step(code):
    if "instruction" in code:
        return "instruction"
    elif "tool" in code:
        return "tool"
    elif "subgoal" in code:
        return "subgoal"
    return code


ROOT_DIR = "./data/csv"
taxonomy = {"goal": 0, "motivation": 1, "briefing": 2, "reflection": 3, "subgoal": 4, "instruction": 5, "tool": 6, "description": 7, "effect": 8,
            "justification": 9, "background info": 10, "tip": 11, "greeting": 12, "outro": 13, "side note": 14, "transition": 15, "filler": 16, "outcome": 17, "": 18}
total_score = 0
file_count = 0
for filename in os.listdir(ROOT_DIR):
    first_coder = []
    second_coder = []
    with open(os.path.join(ROOT_DIR, filename), 'r') as csv_file:
        if not "csv" in filename:
            continue
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
                continue
            elif row[2] == "":
                continue
            else:
                first_code = transform_step(row[3].strip().lower())
                second_code = transform_step(row[4].strip().lower())
                # if first_code == "" or second_code == "":
                # print(f"no code exists for line {line_count}")
                if (not first_code in taxonomy) or (not second_code in taxonomy):
                    print(f"not existing code {first_code} or {second_code}")
                first_coder.append(taxonomy[first_code])
                second_coder.append(taxonomy[second_code])
                line_count += 1
        # print(first_coder)
        # print(second_coder)
        # if 18 in first_coder or 18 in second_coder:
        #     print(f"{filename[:-4]} has empty codes")
        score = cohen_kappa_score(first_coder, second_coder)
        total_score += score
        file_count += 1
        print(f"{filename[:-4]}: {score}")
print(f"average: {total_score/file_count}")
