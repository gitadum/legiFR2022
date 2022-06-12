#! ./envs/bin/python3
# -*-coding: utf-8-*-

import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import poli_sci_kit
import json
 
df = pd.read_csv('data.csv', header=0, index_col=['Polling firm', 'Date'],
                 parse_dates=['Date'])
with open('group_colors.json', 'r') as color_file:
    colors = json.load(color_file)

poll = df.groupby(['Date','Polling firm']).mean()
poll = poll.apply(lambda x: round(x / poll.sum(axis=1) * 577, 0))

Date = "2022-06-10"
Pollster = "Ipsos"

SPLIT_NUPES = True

def splitCoalitions(df):
    nupesSeats = df.loc[df['NUPES'] != 0, 'NUPES']
    df.loc[df['NUPES'] != 0, 'PCF'] = nupesSeats.apply(lambda x: round(.1*x))
    df.loc[df['NUPES'] != 0, 'LFI'] = nupesSeats.apply(lambda x: round(.5*x))
    df.loc[df['NUPES'] != 0, 'PS'] = nupesSeats.apply(lambda x: round(.2*x))
    df.loc[df['NUPES'] != 0, 'EELV'] = nupesSeats.apply(lambda x: round(.2*x))
    df.loc[df['NUPES'] != 0, 'NUPES'] = 0.0
    return df

if SPLIT_NUPES:
    splitCoalitions(poll)

selected_poll = poll.loc[(Date, Pollster)]

parl_group = list(df.columns)
groupColor = list(colors.values())
seat_alloc = [int(n) for n in selected_poll.values]

# Check that group names, number of seats & group color lists are of equal length
try:
    assert len(parl_group) == len(groupColor) == len(seat_alloc)
except AssertionError:
    print(len(parl_group), len(groupColor), len(seat_alloc))

# Remove political groups with zero seat for clarity purposes
zeroSeat = []
for i in range(len(seat_alloc)):
    if seat_alloc[i] == 0:
        zeroSeat.append(i)

parl_group = [parl_group[i] for i in range(len(parl_group)) if i not in zeroSeat]
groupColor = [groupColor[i] for i in range(len(groupColor)) if i not in zeroSeat]
seat_alloc = list(filter(lambda x: x != 0, seat_alloc))


if __name__ == "__main__":

    fig, ax = plt.subplots(figsize=(8,6))

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
    fig.savefig("Figure_1.png")
    plt.show()
