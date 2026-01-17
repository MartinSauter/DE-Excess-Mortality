# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 18:40:38 2025

@author: Martin Sauter
"""

import matplotlib.pyplot as plt
import numpy as np
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
ag=np.array([22,34.5,49.5,69.5,90])

exzm_rel=np.array([7.8e-5,6.42342E-06,0.000197838,1.80E-03,2.45E-02])

# bis 8.6.

#####################################################
ax.plot(ag,exzm_rel, color="salmon",marker="o",markerfacecolor="salmon",
        markeredgecolor="salmon",markersize=10,
        lw=1,ls="--",alpha=0.5,label="Relative Risk of Excess Mortality")



lr=linregress(ag[2:],np.log10(exzm_rel[2:]))
              
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
