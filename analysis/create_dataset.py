import pandas as pd
import os


def check_label(label, label_set):
    if label in label_set:
        return True
    return False


label_set = ["goal", "motivation", "briefing", "reflection", "subgoal", "instruction", "tool", "outcome", "description", "effect",
             "justification", "background info", "tip", "greeting", "outro", "side note", "transition", "filler",
             "early instruction", "late instruction",
             "subgoal (optional)", "instruction (optional)", "instruction (multiple)", "early instruction (optional)", "early instruction (multiple)", "late instruction (optional)", "late instruction (multiple)", "tool (optional), tool (multiple)"]
ROOT_DIR = "./data/xls"
column_names = ['Video ID', 'Category', 'Script', 'Final']
df_default = pd.DataFrame(columns=column_names)
for filename in os.listdir(ROOT_DIR):
    xls = pd.ExcelFile(os.path.join(ROOT_DIR, filename))
    sheet_to_df_map = {}
    for sheet_name in xls.sheet_names:
        sheet_to_df_map[sheet_name] = xls.parse(sheet_name)
    for vid, df in sheet_to_df_map.items():
        if df.empty:
            continue
        # IMPORTANT: Sentence and the final label should be stored under 'Script' and 'Final', respectively.
        df = pd.DataFrame(df, columns=['Script', 'Final'])
        # remove rows with undecided final label ('Final' = NaN)
        df = df.dropna(subset=['Final'])
        # df = df[df.Final != ""]
        if not df.empty:
            # check if all the labels are correct
            for label in df['Final']:
                if not (label.strip() in label_set):
                    print(
                        f"{filename} - {vid} has an incorrect label: {label.strip()} ")
            # merge into one dataframe
            df_meta = pd.DataFrame(index=range(df.shape[0]), columns=[
                                   'Video ID', 'Category'])
            df_meta['Video ID'] = vid
            df_meta['Category'] = filename[:-5]
            df.reset_index(drop=True, inplace=True)
            df_meta.reset_index(drop=True, inplace=True)
            df_final = pd.concat([df_meta, df], axis=1)
            # print(df_final)
            frames = [df_default, df_final]
            df_default = pd.concat(frames, ignore_index=True)
df_default.to_csv("label_data.csv", encoding='utf-8', index=False)
