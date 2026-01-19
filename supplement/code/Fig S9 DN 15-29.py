# -*- coding: utf-8 -*-
"""
Created on Fri May 20 22:18:38 2022

@author: Martin Sauter
"""



import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import linregress
from cycler import cycler
from matplotlib import ticker


plt.style.use("classic")
plt.rcParams["lines.linewidth"]=2
plt.rcParams['font.family'] = 'Arial'
plt.rcParams["font.size"]=13
plt.rcParams['axes.prop_cycle'] = cycler('color',plt.get_cmap('Paired').colors)

##################################
# Read from files

d15=np.loadtxt("d_ag15.csv",dtype=int) # years descending; so swap
d15=np.flip(d15)


years=np.linspace(2013,2023,11).astype(int)

########################################
#  Fit 13-19

d15_params_1=linregress(years[0:7]-2013,d15[0:7])
d15_fit_1=d15_params_1.slope*(years-2013)+d15_params_1.intercept

########################################
#  Fit 16-19

d15_params_2=linregress(years[3:7]-2016,d15[3:7])
d15_fit_2=d15_params_2.slope*(years-2016)+d15_params_2.intercept

# #######################################

fig,ax=plt.subplots(1,1,figsize=(12,8))


ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:g}"))

ax.set_xlim(2012.5,2023.5)
ax.set_xticks(years) 

ax.set_ylabel("Annual Deaths in Age Group 15-29")
##################################
    
ax.grid(True)


ax.plot(years,d15,linestyle="--",color="dodgerblue",
        label="CDN")
ax.plot(years,d15_fit_1,color="red",alpha=0.6,
        label="Fit CDN 2013-19")



ax.set_xticklabels(years,rotation=90)


ax.plot(years[2:],d15_fit_2[2:],
        label="Fit CDN 2016-19")


ax.legend(loc="lower left", edgecolor="white")

plt.savefig("../figures/Fig S9 DN 15 29.png")