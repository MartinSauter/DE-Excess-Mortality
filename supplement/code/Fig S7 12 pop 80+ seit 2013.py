# -*- coding: utf-8 -*-
"""
Created on Fri May 20 22:18:38 2022

@author: Martin Sauter
"""



import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import linregress
from matplotlib.ticker import FuncFormatter

from cycler import cycler
import os


def format_func(value, tick_number):
    return f'{value:,.0f}'.replace(',', ' ')  
    # Umständlich Tausendertrennzeichen, ohne Dezimalstellen

#####################################################

#plt.clf()
#plt.figure(figsize=(10,7),dpi=100)
fig,ax=plt.subplots(1,1,figsize=(12,6),dpi=100)

plt.style.use("classic")
plt.rcParams["lines.linewidth"]=2
plt.rcParams['font.family'] = 'Arial'
plt.rcParams["font.size"]=14
plt.rcParams['axes.prop_cycle'] = cycler('color',
                                         plt.get_cmap('Paired').colors)


########################################################################

pop=[4325719, 4366360,4544298 ,4729203,4941910,5150685,5389106,5681135,
5936434,6111655,6112952]

# pop=[84669326,84358845,83237124,	83155031	,83166711,83019213,82792351,	82521653	,
#      82175684,81197537,80767463,	80523746	,80327900,81751602,81802257,82002356	]


jahre=np.linspace(2013,2023,11).astype(int)


ax.set_xlim(2012,2024)
ax.set_xticks(np.linspace(2012,2024,13).astype(int))
ax.set_xticklabels(np.linspace(2013,2024,13).astype(int),
                   fontsize=13,rotation=45)

#ax.set_yticks(np.linspace(8e5,1.1e6,7))

# Formatter für die y-Achse setzen
ax.yaxis.set_major_formatter(FuncFormatter(format_func))


ax.set_xlabel("Year",fontsize="16")
ax.spines[:].set_color('black')

ax.set_ylabel("Population 80+")

ax.plot(jahre,pop,lw=0.5,marker="o",color="salmon",
        markersize=10,
        markeredgecolor="salmon",ls="--",label="Estimates by NSO Destatis")
#ax.set_ylabel("Number of Inhabitants of Age >80")

c=plt.get_cmap('Paired').colors
# # #############################################################
# ax.axvspan(2011,2012, color=c[4], alpha=0.3)
# ax.axvspan(2015,2016, color=c[2],alpha=0.3)
# ax.axvspan(2022,2023, color=c[2],alpha=0.3)

# ######################################

m=(pop[-1]-pop[0])/10
b=pop[0]
pop_corr=b+m*(jahre-2013)

ax.plot(jahre,pop_corr,color=c[1],lw=2,ls=(0, (20, 15)),
        label="Corrected by Interpolation"
        , alpha=0.5)
plt.grid(True)
plt.legend(loc="upper left")
plt.tight_layout()

plt.savefig("../figures/Fig S7 Bev 80 + Zeitverlauf.png")