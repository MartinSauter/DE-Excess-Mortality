# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 18:40:38 2025

@author: Martin Sauter
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from cycler import cycler

from scipy.stats import linregress

from math import log  # ln !


fig,ax=plt.subplots(1,1,figsize=(12,8),dpi=100)

plt.style.use("classic")
plt.rcParams["lines.linewidth"]=2
plt.rcParams['font.family'] = 'Arial'
plt.rcParams["font.size"]=14
plt.rcParams['axes.prop_cycle'] = cycler('color',
                                         plt.get_cmap('Paired').colors)


# Beispiel-Daten
ag=np.array([7,22,34.5,49.5,69.5,90])

#exzm_rel=np.array([7.8e-5,6.42342E-06,0.000197838,1.80E-03,2.45E-02])
exzm=pd.read_csv("./Tab.2 Data CDC Trend 13-19 20y age groups.txt",
                     delimiter="\s+",skiprows=2,engine="python",
                     header=None,
                     index_col=0,           # erste Spalte = Zeilenindex)
                     usecols=[0,1,3,5,7])   # Only absolute values
exzm.columns=[2020,2021,2022,2023]
"""
Checking Values
        2020   2021   2022   2023
0                                
0-14    -431   -428   -407   -480
15-29   -142     25    281    181
30-39    -19     36    194   -141
40-59    169   3764   1718  -1029
60-79  -1716  10220  15278   9379
80+    24554  35584  63464  23155

"""
pop=pd.read_csv("../../data_proc/pop/Pop_20y.tsv",delimiter="\t",
                index_col=0,usecols=[0,10,11,12,13])
pop.columns=[2020,2021,2022,2023]

pop.index=["0-14","15-29","30-39","40-59","60-79","80+"]
pop.index.name="AG"

"""
          2020      2021      2022      2023
AG                                           
0-14   11391259  11477800  11606935  11928977
15-29  13622145  13340204  13242236  13478239
30-39  10784930  10871964  10888798  11090345
40-59  23629924  23375290  23068612  22999053
60-79  18057318  18153339  18318888  18749279
80+     5681135   5936434   6111655   6112952
"""


exzm_rel=exzm/pop
exzm_rel["Total"]=exzm_rel.sum(axis=1)
ex=exzm_rel["Total"].values

#####################################################
ax.plot(ag[1:],ex[1:], color="salmon",marker="o",markerfacecolor="salmon",
        markeredgecolor="salmon",markersize=10,
        lw=1,ls="--",alpha=0.5,label="Relative Risk of Excess Mortality")



lr=linregress(ag[3:],np.log10(ex[3:]))
              
f=np.exp(log(10)*(lr.intercept+lr.slope*ag))
         
ax.plot(ag[1:],f[1:],ls="-",lw=2,color="dodgerblue",
        label="Exponential Fit", alpha=0.5)


ax.set_yscale("log")
ax.set_xlabel("Median of age brackets")

ax.set_ylabel("Relative Risk for Excess Deaths in Age Group")
ax.grid(True)
ax.legend(loc="upper left",edgecolor="white")

print(f"{lr.slope}")
plt.savefig("../figures/Fig 5b exzm rel risk.png")
