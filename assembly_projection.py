#! ./envs/bin/python3
# -*-coding: utf-8-*-

import matplotlib as mpl
import matplotlib.pyplot as plt
from numpy import mean
import poli_sci_kit

parl_group = ["PCF","LFI","PS","EELV","Ens.","LR","DLF","RN","Req.","Others"]
groupColor = ['red', 'firebrick', 'salmon', 'limegreen', 'orange', 
              'royalblue', 'blueviolet', 'navy', 'saddlebrown', 'lightgray']

projec_min = [9,60,18,20,295,32,0,42,0,3]
projec_max = [16,86,34,35,345,52,1,68,3,7]
projec_avg = []

try:
    assert len(parl_group) == len(groupColor) == len(projec_min) == len(projec_max)
except AssertionError:
    print(len(parl_group), len(groupColor), len(projec_min), len(projec_max))

for i in range(len(parl_group)):
    group_avg = round(mean([projec_min[i],projec_max[i]]),0)
    projec_avg.append(group_avg)

seat_alloc = [int(round(i / sum(projec_avg) * 577, 0)) for i in projec_avg]
#print(seat_alloc)

zeroSeat = []
for i in range(len(seat_alloc)):
    if seat_alloc[i] == 0:
        zeroSeat.append(i)

parl_group = [parl_group[i] for i in range(len(parl_group)) if i not in zeroSeat]
groupColor = [groupColor[i] for i in range(len(groupColor)) if i not in zeroSeat]
seat_alloc = list(filter(lambda x: x != 0, seat_alloc))

#print(parl_group, len(parl_group))
#print(groupColor, len(groupColor))
#print(seat_alloc, len(seat_alloc))

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
ax.text(0,-1,'source: Harris Interactive, May 23rd, 2022', fontsize=12)
ax.set_title("Polls - France: 2022 Legislative elections - seat projections")

fig.tight_layout()

plt.show()
