#! ./envs/bin/python3
# -*-coding: utf-8-*-

from datetime import date
import matplotlib.pyplot as plt
import seaborn as sns
from assembly_seatProjection import *

def enable_coalitions(df):
    df.loc[df['NUPES'] == 0, 'NUPES'] = df['PCF']+df['LFI']+df['PS']+df['EELV']
    df.drop(columns=['PCF', 'LFI', 'PS', 'EELV'], inplace=True)
    for group in ['PCF', 'LFI', 'PS', 'EELV']:
        del colors[group]
    return df

COALITIONS_ENABLED = True

if COALITIONS_ENABLED:
    poll = enable_coalitions(poll)

tab = poll.stack().reset_index().rename(columns={'level_2': 'party', 0: 'numSeats'})
tab['Date'] = pd.to_datetime(tab['Date']).apply(lambda date: date.toordinal())

sns.set_theme()
plot = sns.lmplot(data=tab, x='Date', y='numSeats', hue="party", palette=colors,
                  height=9, aspect=1.5, legend=False)
# iterate through the axes of the figure-level plot
for ax in plot.axes.flat:
    labels = ax.get_xticks() # get x labels
    new_labels = [date.fromordinal(int(label)) for label in labels] # convert ordinal back to datetime
    ax.set_xticks(labels)
    ax.set_xticklabels(new_labels, rotation=90) # set new labels
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig('Figure_1.png')
plt.show()
quit()