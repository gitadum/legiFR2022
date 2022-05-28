#! ./envs/bin/python3
# -*-coding: utf-8-*-

import matplotlib.pyplot as plt
import seaborn as sns
from assembly_projection import *

def enable_coalitions(df):
    df.loc[df['NUPES'] == 0, 'NUPES'] = df['PCF']+df['LFI']+df['PS']+df['EELV']
    df.drop(columns=['PCF', 'LFI', 'PS', 'EELV'], inplace=True)
    for group in ['PCF', 'LFI', 'PS', 'EELV']:
        del colors[group]
    return df

COALITIONS_ENABLED = True

df_cp = poll.reset_index()
df_cp.drop(columns=['Polling firm'], inplace=True)
df_cp.set_index('Date', inplace=True)
if COALITIONS_ENABLED:
    df_cp = enable_coalitions(df_cp)
print(df_cp)
print(colors.values())
sns.lineplot(data=df_cp, palette=colors.values(), ax=ax)
ax.legend(loc='upper left')
plt.show()
quit()