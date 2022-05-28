#! ./envs/bin/python3
# -*-coding: utf-8-*-

from cProfile import label
from re import L
import matplotlib as mpl
import matplotlib.pyplot as plt
from numpy import mean
import poli_sci_kit

parl_group = ["PCF","LFI","PS","EELV","Ens.","LR","DLF","RN","Req.","Div."]
groupColor = ['brown', 'firebrick', 'salmon', 'limegreen', 'gold', 
              'dodgerblue', 'blueviolet', 'navy', 'saddlebrown', 'lightgray']

projec_min = [9,60,18,20,295,32,0,42,0,3]
projec_max = [16,86,34,35,345,52,1,68,3,7]
projec_avg = []
for i in range(len(parl_group)):
    group_avg = round(mean([projec_min[i],projec_max[i]]),0)
    projec_avg.append(group_avg)

seat_alloc = [int(round(i / sum(projec_avg) * 577, 0)) for i in projec_avg]
#print(seat_alloc)

for i in range(len(seat_alloc)):
    if seat_alloc[i] == 0:
        parl_group.pop(i)
        groupColor.pop(i)

seat_alloc.remove(0)
#print(parl_group, len(parl_group))
#print(groupColor, len(groupColor))
#print(seat_alloc, len(seat_alloc))

fig, ax = plt.subplots(figsize=(12,9))

poli_sci_kit.plot.parliament(
    allocations=seat_alloc,
    labels=parl_group,
    colors=[mpl.colors.cnames[c] for c in groupColor],
    style="semicircle",
    num_rows=10,
    marker_size=150,
    speaker=False,
    axis=ax,)
ax.legend(parl_group)

plt.show()
