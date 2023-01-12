# import pandas
import pandas as pd
# import matplotlib
import matplotlib.pyplot as plt
# import seaborn
import seaborn as sns

import numpy as np


fig, axes = plt.subplots(1, 2)

axes[0].set_title('Helpfulness')
axes[1].set_title('Importance')

data_list = ['saelyne_data_helpfulness.csv', 'saelyne_data_importance.csv']


for i, filename in enumerate(data_list):
	axes[i].set_ylim([0, 5.5])

	df = pd.read_csv(filename, sep='\t')

	df_values = df.loc[:, df.columns != 'Task']
	df_melt = pd.melt(df_values)

	num_col = len(df_values.columns)
	df_task = df.iloc[:, 0]
	df_task = pd.concat([df_task] * num_col, ignore_index=True)


	df_melt['Task'] = df_task.values

	axes[i].set_xticklabels(df_values.columns, rotation=45)

	ax = sns.boxplot(ax=axes[i], x="variable", y="value", data=df_melt, 
	                 palette="Set2", hue="Task")
	ax.set(ylabel=None, xlabel=None)
	ax.legend(ncol=3)

fig.tight_layout(pad=2.0)

plt.show()