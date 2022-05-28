#! ./envs/bin/python3
# -*-coding: utf-8-*-

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from numpy import mean
import poli_sci_kit
import json
 
df = pd.read_csv('data.csv', header=0, index_col=['Polling firm', 'Date'],
                 parse_dates=['Date'])
with open('group_colors.json', 'r') as color_file:
    colors = json.load(color_file)

poll = df.groupby(['Polling firm','Date']).mean()
poll = poll.apply(lambda x: round(x / poll.sum(axis=1) * 577, 0))

Pollster = "Harris Interactive"
Date = "2022-05-23"

selected_poll = poll.loc[(Pollster, Date)]
parl_group = list(df.columns)
groupColor = list(colors.values())
seat_alloc = [int(n) for n in selected_poll.values]

try:
    assert len(parl_group) == len(groupColor) == len(seat_alloc)
except AssertionError:
    print(len(parl_group), len(groupColor), len(seat_alloc))

zeroSeat = []
for i in range(len(seat_alloc)):
    if seat_alloc[i] == 0:
        zeroSeat.append(i)

parl_group = [parl_group[i] for i in range(len(parl_group)) if i not in zeroSeat]
groupColor = [groupColor[i] for i in range(len(groupColor)) if i not in zeroSeat]
seat_alloc = list(filter(lambda x: x != 0, seat_alloc))

fig, ax = plt.subplots(figsize=(8,6))

if __name__ == "__main__":

    poli_sci_kit.plot.parliament(
        allocations=seat_alloc,
        labels=parl_group,
        colors=[mpl.colors.cnames[c] for c in groupColor],
        style="semicircle",
        num_rows=10,
        marker_size=120,
        speaker=False,
        axis=ax)

    ax.legend(["{g} : {s}".format(g=group, s=seat)
            for group, seat in zip(parl_group, seat_alloc)])
    ax.text(0,-1,'source: {p}, {d}'.format(p=Pollster, d=Date), fontsize=12)
    ax.set_title("Polls - France: 2022 Legislative elections - seat projections")

    fig.tight_layout()

    plt.show()
