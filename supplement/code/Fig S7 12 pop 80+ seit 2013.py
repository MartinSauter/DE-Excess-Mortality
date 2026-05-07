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

df=pd.read_csv("../../data_proc/pop/Pop_20y.tsv",sep="\t",
               index_col=0)




# %%
df=df.drop(columns=["2011","2012","2024"])
# pop=[4325719, 4366360,4544298 ,4729203,4941910,5150685,5389106,5681135,
# 5936434,6111655,6112952]



# %%
jahre=np.linspace(2013,2023,11).astype(int)
x=0;y=0
k=0


pop80=df.loc["80+",:].values

# pop=[4325719, 4366360,4544298 ,4729203,4941910,5150685,5389106,5681135,
# 5936434,6111655,6112952]



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

ax.plot(jahre,pop80,lw=0.5,marker="o",color="salmon",
        markersize=10,
        markeredgecolor="salmon",ls="--",label="Estimates by NSO Destatis")
#ax.set_ylabel("Number of Inhabitants of Age >80")

c=plt.get_cmap('Paired').colors
# # #############################################################
# ax.axvspan(2011,2012, color=c[4], alpha=0.3)
# ax.axvspan(2015,2016, color=c[2],alpha=0.3)
# ax.axvspan(2022,2023, color=c[2],alpha=0.3)

# ######################################

m=(pop80[-1]-pop80[0])/10
b=pop80[0]
pop80_corr=b+m*(jahre-2013)

# export for further usage

np.savetxt("../../data_proc/pop/pop80.csv",pop80,fmt="%d",delimiter=";")
np.savetxt("../../data_proc/pop/pop80_corr.csv",pop80_corr,fmt="%d",delimiter=";")

ax.plot(jahre,pop80_corr,color=c[1],lw=2,ls=(0, (20, 15)),
        label="Corrected by Interpolation"
        , alpha=0.5)
plt.grid(True)
plt.legend(loc="upper left")
plt.tight_layout()

plt.savefig("../figures/Fig S7 Bev 80 + Zeitverlauf.png")