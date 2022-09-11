import pandas as pd
import matplotlib.pyplot as plt
import os
import json

def read_json (fp):
    with open (fp, 'r') as s:
        script = json.load(s)
    return script

style_filepaths = ["./data/final/analyzed_total.json", "./data/final/styles/analyzed_first.json", "./data/final/styles/analyzed_third.json", "./data/final/styles/analyzed_view_both.json", "./data/final/styles/analyzed_screencast.json", "./data/final/styles/analyzed_talking.json", "./data/final/styles/analyzed_dubbing.json", "./data/final/styles/analyzed_narration_both.json", "./data/final/styles/analyzed_static_move.json", "./data/final/styles/analyzed_view_zoom_change.json"]
styles = ["Total", "1st", "3rd", "View_Both", "Screencast", "Talking", "Dubbing", "Narration_Both", "Static_Move", "View_Zoom_Change"]

# Dataframes
df_style_section_count = pd.DataFrame()
df_style_category_count = pd.DataFrame()
df_style_type_count = pd.DataFrame()

df_style_section_time = pd.DataFrame()
df_style_category_time = pd.DataFrame()
df_style_type_time = pd.DataFrame()


# Accumulate data

style_idx = 0
### Style
# Download data
for fp in style_filepaths:
    style_data = read_json(fp)

    ## Count
    style_count_data = style_data["count"]
    
    # Sections
    for section in style_count_data["sections"]:
        df_style_section_count.loc[styles[style_idx], section] = style_count_data["sections"][section]["portion"]   
    
    # Categories
    for category in style_count_data["categories"]:
        df_style_category_count.loc[styles[style_idx], category] = style_count_data["categories"][category]["portion"]

    # Types
    for type in style_count_data["types"]:
        df_style_type_count.loc[styles[style_idx], type] = style_count_data["types"][type]["portion"]


    ## Time
    style_time_data = style_data["time_portion"]

    # Sections
    for section in style_time_data["sections"]:
        df_style_section_time.loc[styles[style_idx], section] = style_time_data["sections"][section]["time"]

    # Categories
    for category in style_time_data["categories"]:
        df_style_category_time.loc[styles[style_idx], category] = style_time_data["categories"][category]["time"]

    # Types
    for type in style_time_data["types"]:
        df_style_type_time.loc[styles[style_idx], type] = style_time_data["types"][type]["time"]

    style_idx += 1

### Video category (genre)
category_filepaths = ["./data/final/analyzed_total.json", "./data/final/categories/analyzed_Arts and Entertainment.json", "./data/final/categories/analyzed_Cars & Other Vehicles.json", "./data/final/categories/analyzed_Computers and Electronics.json", "./data/final/categories/analyzed_Education and Communications.json", "./data/final/categories/analyzed_Food and Entertaining.json", "./data/final/categories/analyzed_Health.json", "./data/final/categories/analyzed_Hobbies and Crafts.json", "./data/final/categories/analyzed_Holidays and Traditions.json", "./data/final/categories/analyzed_Home and Garden.json", "./data/final/categories/analyzed_Personal Care and Style.json", "./data/final/categories/analyzed_Pets and Animals.json", "./data/final/categories/analyzed_Sports and Fitness.json"]
categories = ["Total", "Arts and Entertainment", "Cars & Other Vehicles", "Computers and Electronics", "Education and Communications", "Food and Entertaining", "Health", "Hobbies and Crafts", "Holidays and Traditions", "Home and Garden", "Personal Care and Style", "Pets and Animals", "Sports and Fitness"]

# Dataframes
df_category_section_count = pd.DataFrame()
df_category_category_count = pd.DataFrame()
df_category_type_count = pd.DataFrame()

df_category_section_time = pd.DataFrame()
df_category_category_time = pd.DataFrame()
df_category_type_time = pd.DataFrame()

category_idx = 0
# Download data
for fp in category_filepaths:
    category_data = read_json(fp)

    ## Count
    category_count_data = category_data["count"]
    
    # Sections
    for section in category_count_data["sections"]:
        df_category_section_count.loc[categories[category_idx], section] = category_count_data["sections"][section]["portion"]   
    
    # Categories
    for category in category_count_data["categories"]:
        df_category_category_count.loc[categories[category_idx], category] = category_count_data["categories"][category]["portion"]

    # Types
    for type in category_count_data["types"]:
        df_category_type_count.loc[categories[category_idx], type] = category_count_data["types"][type]["portion"]


    ## Time
    category_time_data = category_data["time_portion"]

    # Sections
    for section in category_time_data["sections"]:
        df_category_section_time.loc[categories[category_idx], section] = category_time_data["sections"][section]["time"]

    # Categories
    for category in category_time_data["categories"]:
        df_category_category_time.loc[categories[category_idx], category] = category_time_data["categories"][category]["time"]

    # Types
    for type in category_time_data["types"]:
        df_category_type_time.loc[categories[category_idx], type] = category_time_data["types"][type]["time"]
        
    category_idx += 1


## Style visualization
df_style_section_count.plot(kind = 'bar', stacked = True, title = 'Proportion of Section (Count)')
#plt.xticks(rotation='horizontal')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.tight_layout()
plt.show()

df_style_category_count.plot(kind = 'bar', stacked = True, title = 'Proportion of Category (Count)')
#plt.xticks(rotation='horizontal')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.tight_layout()
plt.show() 

df_style_type_count.plot(kind = 'bar', stacked = True, title = 'Proportion of Type (Count)')
#plt.xticks(rotation='horizontal')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.tight_layout()
plt.show() 

df_style_section_time.plot(kind = 'bar', stacked = True, title = 'Proportion of Section (Time)')
#plt.xticks(rotation='horizontal')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.tight_layout()
plt.show()

df_style_category_time.plot(kind = 'bar', stacked = True, title = 'Proportion of Category (Time)')
#plt.xticks(rotation='horizontal')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.tight_layout()
plt.show() 

df_style_type_time.plot(kind = 'bar', stacked = True, title = 'Proportion of Type (Time)')
#plt.xticks(rotation='horizontal')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.tight_layout()
plt.show() 


## Category visualization
df_category_section_count.plot(kind = 'bar', stacked = True, title = 'Proportion of Section (Count)')
#plt.xticks(rotation='horizontal')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.tight_layout()
plt.show()

df_category_category_count.plot(kind = 'bar', stacked = True, title = 'Proportion of Category (Count)')
#plt.xticks(rotation='horizontal')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.tight_layout()
plt.show() 

df_category_type_count.plot(kind = 'bar', stacked = True, title = 'Proportion of Type (Count)')
#plt.xticks(rotation='horizontal')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.tight_layout()
plt.show() 

df_category_section_time.plot(kind = 'bar', stacked = True, title = 'Proportion of Section (Time)')
#plt.xticks(rotation='horizontal')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.tight_layout()
plt.show()

df_category_category_time.plot(kind = 'bar', stacked = True, title = 'Proportion of Category (Time)')
#plt.xticks(rotation='horizontal')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.tight_layout()
plt.show() 

df_category_type_time.plot(kind = 'bar', stacked = True, title = 'Proportion of Type (Time)')
#plt.xticks(rotation='horizontal')
plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
plt.tight_layout()
plt.show() 