# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 18:40:38 2025

@author: Martin Sauter
"""

import matplotlib.pyplot as plt
import numpy as np
from cycler import cycler
import pandas as pd

from scipy.stats import linregress

from math import log  # ln !


fig,ax=plt.subplots(1,1,figsize=(12,8),dpi=100)

plt.style.use("classic")
plt.rcParams["lines.linewidth"]=2
plt.rcParams['font.family'] = 'Arial'
plt.rcParams["font.size"]=13
plt.rcParams['axes.prop_cycle'] = cycler('color',
                                         plt.get_cmap('Paired').colors)


# Median of age groups
ag=np.array([5,15,25,35,45,55,65,75,85])



c19=pd.read_excel("../../data_raw/covid-deaths/Klinische_Aspekte.xlsx",
                  sheet_name="Todesfälle_Alter_Geschlecht",skiprows=5,
                  usecols="A:K",index_col=0)

c19=c19[c19.index =="gesamt"].values.astype(int)[0]
c19[-2]=c19[-1]+c19[-2]
c19=np.delete(c19,-1)

# Agg. 80-90 and 90 +  (last and 2nd last)

"""
Result:
72,54,203,599,1678,6388,16713,35371,76988,36155
"""



pop=pd.read_csv("../../data_proc/pop/Pop_10y.tsv",delimiter="\t",index_col=0)
pop2022=pop["2022"].values


"""
7863474,  7570441,  9415256, 10888798,  9996703, 13071909,
       10961974,  7356914,  6111655
"""

#####################################################
ax.plot(ag,c19/pop2022, color="salmon",marker="o",markerfacecolor="salmon",
        markeredgecolor="salmon",markersize=10,
        lw=1,ls="--",alpha=0.5,label="Covid Deaths normalised to population")



lr=linregress(ag[1:9],np.log10(c19[1:9]/pop2022[1:9]))
print(lr)
              
f=np.exp(log(10)*(lr.intercept+lr.slope*ag[1:9]))
         
ax.plot(ag[1:9],f,ls="-",lw=2,color="dodgerblue",
        label="Exponential Fit", alpha=0.5)


ax.set_yscale("log")
ax.set_xlabel("Median of age brackets")

ax.set_ylabel("Deaths normalised to members of Age Group")
ax.grid(True)
ax.legend(loc="upper left",edgecolor="white")


plt.savefig("../figures/Fig 5a C19 norm deaths.tif",
            dpi=600,pil_kwargs={"compression": "tiff_lzw"})
plt.savefig("../figures/Fig 5a C19 norm deaths.png",
            dpi=1000)