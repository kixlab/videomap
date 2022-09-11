import pandas as pd
import matplotlib.pyplot as plt
import os
import json

def read_json (fp):
    with open (fp, 'r') as s:
        script = json.load(s)
    return script

filepaths = ["./data/final/analyzed_total.json", "./data/final/analyzed_first.json", "./data/final/analyzed_third.json", "./data/final/analyzed_view_both.json", "./data/final/analyzed_screencast.json", "./data/final/analyzed_talking.json", "./data/final/analyzed_dubbing.json", "./data/final/analyzed_narration_both.json", "./data/final/analyzed_static_move.json", "./data/final/analyzed_view_zoom_change.json"]
styles = ["Total", "1st", "3rd", "View_Both", "Screencast", "Talking", "Dubbing", "Narration_Both", "Static_Move", "View_Zoom_Change"]

# Dataframes
df_section_count = pd.DataFrame()
df_category_count = pd.DataFrame()
df_type_count = pd.DataFrame()

df_section_time = pd.DataFrame()
df_category_time = pd.DataFrame()
df_type_time = pd.DataFrame()


# Accumulate data

idx = 0
# Download data
for fp in filepaths:
    data = read_json(fp)

    ## Count
    count_data = data["count"]
    
    # Sections
    for section in count_data["sections"]:
        df_section_count.loc[styles[idx], section] = count_data["sections"][section]["portion"]   
    
    # Categories
    for category in count_data["categories"]:
        df_category_count.loc[styles[idx], category] = count_data["categories"][category]["portion"]

    # Types
    for type in count_data["types"]:
        df_type_count.loc[styles[idx], type] = count_data["types"][type]["portion"]


    ## Time
    time_data = data["time_portion"]

    # Sections
    for section in time_data["sections"]:
        df_section_time.loc[styles[idx], section] = time_data["sections"][section]["time"]

    # Categories
    for category in time_data["categories"]:
        df_category_time.loc[styles[idx], category] = time_data["categories"][category]["time"]

    # Types
    for type in time_data["types"]:
        df_type_time.loc[styles[idx], type] = time_data["types"][type]["time"]


    idx += 1

df_section_count.plot(kind = 'bar', stacked = True, title = 'Proportion of Section (Count)')
plt.xticks(rotation='horizontal')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.tight_layout()
plt.show()

df_category_count.plot(kind = 'bar', stacked = True, title = 'Proportion of Category (Count)')
#plt.xticks(rotation='horizontal')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.tight_layout()
plt.show() 

df_type_count.plot(kind = 'bar', stacked = True, title = 'Proportion of Type (Count)')
#plt.xticks(rotation='horizontal')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.tight_layout()
plt.show() 

df_section_time.plot(kind = 'bar', stacked = True, title = 'Proportion of Section (Time)')
#plt.xticks(rotation='horizontal')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.tight_layout()
plt.show()

df_category_time.plot(kind = 'bar', stacked = True, title = 'Proportion of Category (Time)')
#plt.xticks(rotation='horizontal')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.tight_layout()
plt.show() 

df_type_time.plot(kind = 'bar', stacked = True, title = 'Proportion of Type (Time)')
#plt.xticks(rotation='horizontal')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.tight_layout()
plt.show() 