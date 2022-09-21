from turtle import color
import pandas as pd
import matplotlib.pyplot as plt
import os
import json
import numpy as np

def read_json (fp):
    with open (fp, 'r') as s:
        script = json.load(s)
    return script

# style_filepaths = ["./data/final/analyzed_total.json", "./data/final/styles/analyzed_first.json", "./data/final/styles/analyzed_third.json", "./data/final/styles/analyzed_view_both.json", "./data/final/styles/analyzed_screencast.json", "./data/final/styles/analyzed_talking.json", "./data/final/styles/analyzed_dubbing.json", "./data/final/styles/analyzed_narration_both.json", "./data/final/styles/analyzed_static_move.json", "./data/final/styles/analyzed_view_zoom_change.json"]
# styles = ["Total", "1st", "3rd", "View_Both", "Screencast", "Talking", "Dubbing", "Narration_Both", "Static_Move", "View_Zoom_Change"]
style_filepaths = ["./data/final/analyzed_total.json", "./data/final/styles/analyzed_talking.json", "./data/final/styles/analyzed_dubbing.json"]
styles = ["Total","Talking", "Dubbing"]

# Dataframes
df_style_section_count = pd.DataFrame()
df_style_category_count = pd.DataFrame()
df_style_type_count = pd.DataFrame()

df_style_section_time = pd.DataFrame()
df_style_category_time = pd.DataFrame()
df_style_type_time = pd.DataFrame()

style_idx = 0
### Style
# Download data
for fp in style_filepaths:
    style_data = read_json(fp)

    ## Count
    style_count_data = style_data["count"]
    
    # Sections
    for section in style_count_data["sections"]:
        df_style_section_count.loc[styles[style_idx], section] = style_count_data["sections"][section]["portion"]*100   
    
    # Categories
    for category in style_count_data["categories"]:
        df_style_category_count.loc[styles[style_idx], category] = style_count_data["categories"][category]["portion"]*100

    # Types
    for type in style_count_data["types"]:
        df_style_type_count.loc[styles[style_idx], type] = style_count_data["types"][type]["portion"]*100


    ## Time
    style_time_data = style_data["time_portion"]

    # Sections
    for section in style_time_data["sections"]:
        df_style_section_time.loc[styles[style_idx], section] = style_time_data["sections"][section]["time"]*100

    # Categories
    for category in style_time_data["categories"]:
        df_style_category_time.loc[styles[style_idx], category] = style_time_data["categories"][category]["time"]*100

    # Types
    for type in style_time_data["types"]:
        df_style_type_time.loc[styles[style_idx], type] = style_time_data["types"][type]["time"]*100

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
        df_category_section_count.loc[categories[category_idx], section] = category_count_data["sections"][section]["portion"]*100  
    
    # Categories
    for category in category_count_data["categories"]:
        df_category_category_count.loc[categories[category_idx], category] = category_count_data["categories"][category]["portion"]*100

    # Types
    for type in category_count_data["types"]:
        df_category_type_count.loc[categories[category_idx], type] = category_count_data["types"][type]["portion"]*100


    ## Time
    category_time_data = category_data["time_portion"]

    # Sections
    for section in category_time_data["sections"]:
        df_category_section_time.loc[categories[category_idx], section] = category_time_data["sections"][section]["time"]*100

    # Categories
    for category in category_time_data["categories"]:
        df_category_category_time.loc[categories[category_idx], category] = category_time_data["categories"][category]["time"]*100

    # Types
    for type in category_time_data["types"]:
        df_category_type_time.loc[categories[category_idx], type] = category_time_data["types"][type]["time"]*100
        
    category_idx += 1


### Task Type
task_filepaths = ["./data/final/analyzed_total.json", "./data/final/task_type/analyzed_create.json", "./data/final/task_type/analyzed_fix.json", "./data/final/task_type/analyzed_use.json"]
tasks = ["Total", "Create", "Fix", "Use", "Screen"]

# Dataframes
df_task_section_count = pd.DataFrame()
df_task_category_count = pd.DataFrame()
df_task_type_count = pd.DataFrame()

df_task_section_time = pd.DataFrame()
df_task_category_time = pd.DataFrame()
df_task_type_time = pd.DataFrame()

task_idx = 0
### Task Type
# Download data
for fp in task_filepaths:
    task_data = read_json(fp)

    ## Count
    task_count_data = task_data["count"]
    
    # Sections
    for section in task_count_data["sections"]:
        df_task_section_count.loc[tasks[task_idx], section] = task_count_data["sections"][section]["portion"]*100   
    
    # Categories
    for category in task_count_data["categories"]:
        df_task_category_count.loc[tasks[task_idx], category] = task_count_data["categories"][category]["portion"]*100

    # Types
    for type in task_count_data["types"]:
        df_task_type_count.loc[tasks[task_idx], type] = task_count_data["types"][type]["portion"]*100


    ## Time
    task_time_data = task_data["time_portion"]

    # Sections
    for section in task_time_data["sections"]:
        df_task_section_time.loc[tasks[task_idx], section] = task_time_data["sections"][section]["time"]*100

    # Categories
    for category in task_time_data["categories"]:
        df_task_category_time.loc[tasks[task_idx], category] = task_time_data["categories"][category]["time"]*100

    # Types
    for type in task_time_data["types"]:
        df_task_type_time.loc[tasks[task_idx], type] = task_time_data["types"][type]["time"]*100

    task_idx += 1


### Audio Portion
audio_filepaths = ["./data/final/analyzed_total.json", "./data/final/audio_portion/analyzed_audio_low.json", "./data/final/audio_portion/analyzed_audio_high.json"]
audios = ["Total", "Low", "High"]

# Dataframes
df_audio_section_count = pd.DataFrame()
df_audio_category_count = pd.DataFrame()
df_audio_type_count = pd.DataFrame()

df_audio_section_time = pd.DataFrame()
df_audio_category_time = pd.DataFrame()
df_audio_type_time = pd.DataFrame()

audio_idx = 0
### Audio Type
# Download data
for fp in audio_filepaths:
    audio_data = read_json(fp)

    ## Count
    audio_count_data = audio_data["count"]
    
    # Sections
    for section in audio_count_data["sections"]:
        df_audio_section_count.loc[audios[audio_idx], section] = audio_count_data["sections"][section]["portion"]*100   
    
    # Categories
    for category in audio_count_data["categories"]:
        df_audio_category_count.loc[audios[audio_idx], category] = audio_count_data["categories"][category]["portion"]*100

    # Types
    for type in audio_count_data["types"]:
        df_audio_type_count.loc[audios[audio_idx], type] = audio_count_data["types"][type]["portion"]*100


    ## Time
    audio_time_data = audio_data["time_portion"]

    # Sections
    for section in audio_time_data["sections"]:
        df_audio_section_time.loc[audios[audio_idx], section] = audio_time_data["sections"][section]["time"]*100

    # Categories
    for category in audio_time_data["categories"]:
        df_audio_category_time.loc[audios[audio_idx], category] = audio_time_data["categories"][category]["time"]*100

    # Types
    for type in audio_time_data["types"]:
        df_audio_type_time.loc[audios[audio_idx], type] = audio_time_data["types"][type]["time"]*100

    audio_idx += 1


# Total
# fig, axes = plt.subplots(nrows=3, ncols=1)

# df_total_section_time = df_style_section_time[:1]
# df_total_section_time = df_total_section_time[['intro', 'procedure', 'outro', 'misc.']]
# df_total_section_time.plot(kind='barh', stacked = True, ax=axes[0], width=0.2)

# df_total_category_time = df_style_category_time[:1]
# df_total_category_time = df_total_category_time[['greeting', 'overview', 'step', 'supplementary', 'explanation', 'description', 'conclusion', 'misc.']]
# df_total_category_time.plot(kind='barh', stacked = True, ax=axes[1], width=0.2) 

# df_total_type_time = df_style_type_time[:1]
# df_total_type_time = df_total_type_time[['opening', 'goal', 'motivation', 'briefing', 'subgoal', 'instruction', 'tool', 'tip', 'warning', 'justification', 'effect', 'status', 'context', 'tool specification', 'closing', 'outcome', 'reflection', 'side note', 'self-promo', 'bridge', 'filler']]
# df_total_type_time.plot(kind='barh', stacked = True, ax=axes[2], width=0.2)

# idx = 0
# for ax in axes:
#     for c in ax.containers:
#         ax.bar_label(c, labels=[f'{x:.1f}%' if x >= 4 else '' for x in c.datavalues ], label_type = "center", fontsize=21)
#     if idx == 0:
#         ax.legend(['Intro', 'Procedure', 'Outro', 'Misc.'], loc='upper left', borderaxespad=0, ncol=8, prop={'size': 15}, bbox_to_anchor=(0, 1.1, 1, 0.2), mode="expand")
#         ax.invert_yaxis()
#         ax.autoscale(enable=True, axis='both', tight=True)
#         ax.set_ylabel ('Section', fontsize=25, labelpad=30)
#         ax.set_xticklabels([0, 20, 40, 60, 80, 100], fontsize=23)
#         ax.set_yticks([])
#     elif idx == 1:
#         ax.legend(['Greeting', 'Overview', 'Method', 'Supplementary', 'Explanation', 'Description', 'Conclusion', 'Misc.'], loc='upper left', borderaxespad=0, ncol=8, prop={'size': 15}, bbox_to_anchor=(0, 1.1, 1, 0.2), mode="expand")
#         ax.invert_yaxis()
#         ax.autoscale(enable=True, axis='both', tight=True)
#         ax.set_ylabel ('Category', fontsize=25, labelpad=30)
#         ax.set_xticklabels([0, 20, 40, 60, 80, 100], fontsize=23)
#         ax.set_yticks([])
#     else:
#         ax.legend(['Opening', 'Goal', 'Motivation', 'Briefing', 'Subgoal', 'Instruction', 'Tool', 'Tip', 'Warning', 'Justification', 'Effect', 'Status', 'Context', 'Tool Spec.', 'Closing', 'Outcome', 'Reflection', 'Side Note', 'Self-promo', 'Bridge', 'Filler'], loc='upper left', borderaxespad=0, ncol=8, prop={'size': 15}, bbox_to_anchor=(0, 1.48, 1, 0.2), mode="expand")
#         ax.invert_yaxis()
#         ax.autoscale(enable=True, axis='both', tight=True)
#         ax.set_ylabel ('Type', fontsize=25, labelpad=30)
#         ax.set_xlabel ('Proportion of Information Type (%)', fontsize=25, labelpad=25)
#         ax.set_xticklabels([0, 20, 40, 60, 80, 100], fontsize=23)
#         ax.set_yticks([])
#     idx += 1

# plt.subplots_adjust(left=0.08,
#                     bottom=0.15, 
#                     right=0.97, 
#                     top=0.93, 
#                     wspace=0.4, 
#                     hspace=1.1)
# plt.show()


## Style visualization
# df_style_section_count.plot(kind = 'bar', stacked = True, title = 'Proportion of Section (Count)')
# #plt.xticks(rotation='horizontal')
# plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
# plt.tight_layout()
# #plt.show()
# plt.savefig('style_section_count.png')

# df_style_category_count.plot(kind = 'bar', stacked = True, title = 'Proportion of Category (Count)')
# #plt.xticks(rotation='horizontal')
# plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
# plt.tight_layout()
# #plt.show() 
# plt.savefig('style_category_count.png')

# df_style_type_count.plot(kind = 'bar', stacked = True, title = 'Proportion of Type (Count)')
# #plt.xticks(rotation='horizontal')
# plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
# plt.tight_layout()
# #plt.show() 
# plt.savefig('style_type_count.png')



## HEEEEEREEE

## Example code
# fig, axes = plt.subplots(nrows=3, ncols=1)

# df_style_section_time = df_style_section_time[['intro', 'procedure', 'outro', 'misc.']]
# df_style_section_time = df_style_section_time[1:]
# df_style_section_time.plot(kind='barh', stacked = True, ax=axes[0])
# #handles, labels = plt.gca().get_legend_handles_labels()
# #plt.gca().legend(handles[::-1], labels[::-1], loc='upper left', borderaxespad=0, ncol=4)
# # plt.gca().legend(loc='upper left', borderaxespad=0, ncol=4)
# # plt.gca().invert_yaxis()
# # plt.autoscale(enable=True, axis='x', tight=True)
# #plt.savefig('style_section_time.png')

fig, axes = plt.subplots(nrows=3, ncols=1)

df_style_section_time = df_style_section_time[['intro', 'procedure', 'outro', 'misc.']]
df_style_section_time = df_style_section_time[1:]
df_style_section_time.plot(kind='barh', stacked = True, ax=axes[0], width=0.6)

df_style_category_time = df_style_category_time[['greeting', 'overview', 'step', 'supplementary', 'explanation', 'description', 'conclusion', 'misc.']]
df_style_category_time = df_style_category_time[1:]
df_style_category_time.plot(kind='barh', stacked = True, ax=axes[1], width=0.6) 

df_style_type_time = df_style_type_time[['opening', 'goal', 'motivation', 'briefing', 'subgoal', 'instruction', 'tool', 'tip', 'warning', 'justification', 'effect', 'status', 'context', 'tool specification', 'closing', 'outcome', 'reflection', 'side note', 'self-promo', 'bridge', 'filler']]
df_style_type_time = df_style_type_time[1:]
df_style_type_time.plot(kind='barh', stacked = True, ax=axes[2], width=0.6)

idx = 0
for ax in axes:
    for c in ax.containers:
        ax.bar_label(c, labels=[f'{x:.1f}%' if x >= 4 else '' for x in c.datavalues ], label_type = "center", fontsize=18)
    if idx == 0:
        ax.legend(['Intro', 'Procedure', 'Outro', 'Misc.'], loc='upper left', borderaxespad=0, ncol=8, prop={'size': 15}, bbox_to_anchor=(0, 1.1, 1, 0.2), mode="expand")
        ax.invert_yaxis()
        ax.autoscale(enable=True, axis='both', tight=True)
        ax.set_xticklabels([0, 20, 40, 60, 80, 100], fontsize=23)
        ax.set_yticklabels(["Real-time", "Dubbing"], fontsize=19)
    elif idx == 1:
        ax.legend(['Greeting', 'Overview', 'Method', 'Supplementary', 'Explanation', 'Description', 'Conclusion', 'Misc.'], loc='upper left', borderaxespad=0, ncol=8, prop={'size': 15}, bbox_to_anchor=(0, 1.1, 1, 0.2), mode="expand")
        ax.invert_yaxis()
        ax.autoscale(enable=True, axis='both', tight=True)
        ax.set_ylabel ('Narration Style', fontsize=25, labelpad=25)
        ax.set_xticklabels([0, 20, 40, 60, 80, 100], fontsize=23)
        ax.set_yticklabels(["Real-time", "Dubbing"], fontsize=19)
    else:
        ax.legend(['Opening', 'Goal', 'Motivation', 'Briefing', 'Subgoal', 'Instruction', 'Tool', 'Tip', 'Warning', 'Justification', 'Effect', 'Status', 'Context', 'Tool Spec.', 'Closing', 'Outcome', 'Reflection', 'Side Note', 'Self-promo', 'Bridge', 'Filler'], loc='upper left', borderaxespad=0, ncol=8, prop={'size': 15}, bbox_to_anchor=(0, 1.48, 1, 0.2), mode="expand")
        ax.invert_yaxis()
        ax.autoscale(enable=True, axis='both', tight=True)
        ax.set_xlabel ('Proportion of Information Type (%)', fontsize=25, labelpad=25)
        ax.set_xticklabels([0, 20, 40, 60, 80, 100], fontsize=23)
        ax.set_yticklabels(["Real-time", "Dubbing"], fontsize=19)
    idx += 1

plt.subplots_adjust(left=0.12,
                    bottom=0.15, 
                    right=0.97, 
                    top=0.93, 
                    wspace=0.4, 
                    hspace=1.1)
plt.show()

## HEEEEEREEE


## Category visualization
# df_category_section_count.plot(kind = 'bar', stacked = True, title = 'Proportion of Section (Count)')
# #plt.xticks(rotation='horizontal')
# plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
# plt.tight_layout()
# #plt.show()
# plt.savefig('category_section_count.png')

# df_category_category_count.plot(kind = 'bar', stacked = True, title = 'Proportion of Category (Count)')
# #plt.xticks(rotation='horizontal')
# plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
# plt.tight_layout()
# #plt.show() 
# plt.savefig('category_category_count.png')

# df_category_type_count.plot(kind = 'bar', stacked = True, title = 'Proportion of Type (Count)')
# #plt.xticks(rotation='horizontal')
# plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
# plt.tight_layout()
# #plt.show() 
# plt.savefig('category_type_count.png')

# df_category_section_time.plot(kind = 'bar', stacked = True, title = 'Proportion of Section (Time)')
# #plt.xticks(rotation='horizontal')
# plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
# plt.tight_layout()
# #plt.show()
# plt.savefig('category_section_time.png')

# df_category_category_time.plot(kind = 'bar', stacked = True, title = 'Proportion of Category (Time)')
# #plt.xticks(rotation='horizontal')
# plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
# plt.tight_layout()
# #plt.show() 
# plt.savefig('category_category_time.png')

# df_category_type_time.plot(kind = 'bar', stacked = True, title = 'Proportion of Type (Time)')
# #plt.xticks(rotation='horizontal')
# plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
# plt.tight_layout()
# #plt.show() 
# plt.savefig('category_type_time.png')




## Task Type Visualization
# df_task_section_count.plot(kind = 'bar', stacked = True, title = 'Proportion of Section (Count)')
# #plt.xticks(rotation='horizontal')
# plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
# plt.tight_layout()
# #plt.show()
# plt.savefig('task_section_count.png')

# df_task_category_count.plot(kind = 'bar', stacked = True, title = 'Proportion of Category (Count)')
# #plt.xticks(rotation='horizontal')
# plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
# plt.tight_layout()
# #plt.show() 
# plt.savefig('task_category_count.png')

# df_task_type_count.plot(kind = 'bar', stacked = True, title = 'Proportion of Type (Count)')
# #plt.xticks(rotation='horizontal')
# plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
# plt.tight_layout()
# #plt.show() 
# plt.savefig('task_type_count.png')


# HERRRRRRRRRREEE

fig, axes = plt.subplots(nrows=3, ncols=1)

df_task_section_time = df_task_section_time[['intro', 'procedure', 'outro', 'misc.']]
df_task_section_time = df_task_section_time[1:]
df_task_section_time.plot(kind='barh', stacked = True, ax=axes[0], width=0.8)

df_task_category_time = df_task_category_time[['greeting', 'overview', 'step', 'supplementary', 'explanation', 'description', 'conclusion', 'misc.']]
df_task_category_time = df_task_category_time[1:]
df_task_category_time.plot(kind='barh', stacked = True, ax=axes[1], width=0.8) 

df_task_type_time = df_task_type_time[['opening', 'goal', 'motivation', 'briefing', 'subgoal', 'instruction', 'tool', 'tip', 'warning', 'justification', 'effect', 'status', 'context', 'tool specification', 'closing', 'outcome', 'reflection', 'side note', 'self-promo', 'bridge', 'filler']]
df_task_type_time = df_task_type_time[1:]
df_task_type_time.plot(kind='barh', stacked = True, ax=axes[2], width=0.8)

idx = 0
for ax in axes:
    for c in ax.containers:
        ax.bar_label(c, labels=[f'{x:.1f}%' if x >= 4 else '' for x in c.datavalues ], label_type = "center", fontsize=18)
    if idx == 0:
        ax.legend(['Intro', 'Procedure', 'Outro', 'Misc.'], loc='upper left', borderaxespad=0, ncol=8, prop={'size': 15}, bbox_to_anchor=(0, 1.1, 1, 0.2), mode="expand")
        ax.invert_yaxis()
        ax.autoscale(enable=True, axis='both', tight=True)
        ax.set_xticklabels([0, 20, 40, 60, 80, 100], fontsize=23)
        ax.set_yticklabels(["Creating", "Fixing", "Using"], fontsize=19)
    elif idx == 1:
        ax.legend(['Greeting', 'Overview', 'Method', 'Supplementary', 'Explanation', 'Description', 'Conclusion', 'Misc.'], loc='upper left', borderaxespad=0, ncol=8, prop={'size': 15}, bbox_to_anchor=(0, 1.1, 1, 0.2), mode="expand")
        ax.invert_yaxis()
        ax.autoscale(enable=True, axis='both', tight=True)
        ax.set_ylabel ('Task Type', fontsize=25, labelpad=25)
        ax.set_xticklabels([0, 20, 40, 60, 80, 100], fontsize=23)
        ax.set_yticklabels(["Creating", "Fixing", "Using"], fontsize=19)
    else:
        ax.legend(['Opening', 'Goal', 'Motivation', 'Briefing', 'Subgoal', 'Instruction', 'Tool', 'Tip', 'Warning', 'Justification', 'Effect', 'Status', 'Context', 'Tool Spec.', 'Closing', 'Outcome', 'Reflection', 'Side Note', 'Self-promo', 'Bridge', 'Filler'], loc='upper left', borderaxespad=0, ncol=8, prop={'size': 15}, bbox_to_anchor=(0, 1.48, 1, 0.2), mode="expand")
        ax.invert_yaxis()
        ax.autoscale(enable=True, axis='both', tight=True)
        ax.set_xlabel ('Proportion of Information Type (%)', fontsize=25, labelpad=25)
        ax.set_xticklabels([0, 20, 40, 60, 80, 100], fontsize=23)
        ax.set_yticklabels(["Creating", "Fixing", "Using"], fontsize=19)
    idx += 1

plt.subplots_adjust(left=0.12,
                    bottom=0.15, 
                    right=0.97, 
                    top=0.93, 
                    wspace=0.4, 
                    hspace=1.1)
plt.show()

# HERRRRRRRRRREEE


## Audio Type Visualization
# df_audio_section_count.plot(kind = 'bar', stacked = True, title = 'Proportion of Section (Count)')
# #plt.xticks(rotation='horizontal')
# plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
# plt.tight_layout()
# #plt.show()
# plt.savefig('audio_section_count.png')

# df_audio_category_count.plot(kind = 'bar', stacked = True, title = 'Proportion of Category (Count)')
# #plt.xticks(rotation='horizontal')
# plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
# plt.tight_layout()
# #plt.show() 
# plt.savefig('audio_category_count.png')

# df_audio_type_count.plot(kind = 'bar', stacked = True, title = 'Proportion of Type (Count)')
# #plt.xticks(rotation='horizontal')
# plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
# plt.tight_layout()
# #plt.show() 
# plt.savefig('audio_type_count.png')

# df_audio_section_time.plot(kind = 'bar', stacked = True, title = 'Proportion of Section (Time)')
# #plt.xticks(rotation='horizontal')
# plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
# plt.tight_layout()
# #plt.show()
# plt.savefig('audio_section_time.png')

# df_audio_category_time.plot(kind = 'bar', stacked = True, title = 'Proportion of Category (Time)')
# #plt.xticks(rotation='horizontal')
# plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
# plt.tight_layout()
# #plt.show() 
# plt.savefig('audio_category_time.png')

# df_audio_type_time.plot(kind = 'bar', stacked = True, title = 'Proportion of Type (Time)')
# #plt.xticks(rotation='horizontal')
# plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)
# plt.tight_layout()
# ##plt.show() 
# plt.savefig('audio_type_time.png')