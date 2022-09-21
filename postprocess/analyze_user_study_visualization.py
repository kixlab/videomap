import matplotlib.pyplot as plt
import pandas as pd

# Data
summary_helpfulness = [4.333333333, 4.555555556, 5, 4.666666667, 4.666666667, 4.666666667, 4.555555556, 4.444444444]
summary_helpfulness_std = [x/2 for x in [1.414213562, 0.8819171037, 0, 0.7071067812, 0.5, 0.5, 1.013793755, 1.333333333]]
follow_helpfulness = [3.888888889, 4.222222222, 5, 4.444444444, 4.777777778, 4.333333333, 4, 4.111111111]
follow_helpfulness_std = [x/2 for x in [1.763834207, 1.301708279, 0, 0.8819171037, 0.4409585518, 0.8660254038, 1.732050808, 1.763834207]]

summary_importance = [1.222222222, 4.111111111, 4.888888889, 3.333333333, 3.333333333, 3.333333333, 2.777777778, 1]
summary_importance_std = [x/2 for x in [0.4409585518, 1.054092553, 0.3333333333, 0.8660254038, 1, 1.118033989, 1.201850425, 0]]
follow_importance = [1.666666667, 3.777777778, 5, 4.111111111, 4.111111111, 3.888888889, 2.777777778, 1]
follow_importance_std = [x/2 for x in [1.414213562, 1.394433378, 0, 0.9279607271, 1.364225462, 0.78173596, 1.56347192, 0]]

# Data Frame
categories = ['Greeting', 'Overview', 'Method', 'Supplementary', 'Explanation', 'Description', 'Conclusion', 'Misc.']

df_helpfulness = pd.DataFrame(columns=categories)
df_importance = pd.DataFrame(columns=categories)

df_helpfulness.loc[0] = summary_helpfulness
df_helpfulness.loc[1] = follow_helpfulness
df_helpfulness = df_helpfulness.T

df_importance.loc[0] = summary_importance
df_importance.loc[1] = follow_importance
df_importance = df_importance.T

# Plot
fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(10,10))

df_helpfulness.plot(kind="bar", ax=axes[0], yerr=[summary_helpfulness_std, follow_helpfulness_std], capsize=5, zorder=3)
df_importance.plot(kind="bar", ax=axes[1], yerr=[summary_importance_std, follow_importance_std], capsize=5, zorder=3)

idx = 0
for ax in axes:
    ax.legend(['Summary', 'Following'], loc='upper right', ncol=2, bbox_to_anchor=(0, 1.018, 1.018, 0), prop={'size': 17}, frameon=False)
    #ax.set_xlabel('Category', fontsize=30, labelpad=0)
    #ax.set_ylabel('Score', fontsize=30, labelpad=20)
    ax.set_xticklabels(categories, fontsize=20, rotation=45, ha="right")
    ax.set_yticklabels([0, 1, 2, 3, 4, 5], fontsize=20)
    ax.grid(axis='y', zorder=0)
    if idx == 0:
        ax.set_title("Helpfulness", fontsize=22, pad=25)
    else:
        ax.set_title("Importance", fontsize=22, pad=25)
    idx += 1

plt.subplots_adjust(left=0.2,
                    bottom=0.1, 
                    right=0.935, 
                    top=0.93, 
                    wspace=0.2, 
                    hspace=0.4)
plt.tight_layout()
plt.show()

