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
plt.rcParams["font.size"]=13
plt.rcParams['axes.prop_cycle'] = cycler('color',
                                         plt.get_cmap('Paired').colors)


# Beispiel-Daten
ag=np.array([5,15,25,35,45,55,65,75,90])

# Hardcoded from RKI-File

c19=np.array([72,54,203,599,1678,6388,16713,35371,76988+36155])

# Hardcoded (bis 8.6.)
pop2022=np.array([7723290,7625031,9595549,10798034,10169023,13324539,10961974,
         7507364,5779583])
#####################################################
ax.plot(ag,c19/pop2022, color="salmon",marker="o",markerfacecolor="salmon",
        markeredgecolor="salmon",markersize=10,
        lw=1,ls="--",alpha=0.5,label="Covid Deaths normalised to population")



lr=linregress(ag[1:8],np.log10(c19[1:8]/pop2022[1:8]))
              
f=np.exp(log(10)*(lr.intercept+lr.slope*ag[1:8]))
         
ax.plot(ag[1:8],f,ls="-",lw=2,color="dodgerblue",
        label="Exponential Fit", alpha=0.5)


ax.set_yscale("log")
ax.set_xlabel("Median of age brackets")

ax.set_ylabel("Deaths normalised to members of Age Group")
ax.grid(True)
ax.legend(loc="upper left",edgecolor="white")


plt.savefig("../figures/Fig 5a C19 norm deaths.png")
