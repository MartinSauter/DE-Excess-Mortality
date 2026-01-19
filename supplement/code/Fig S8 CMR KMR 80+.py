# -*- coding: utf-8 -*-
"""
Created on Fri May 20 22:18:38 2022

@author: Martin Sauter
"""



import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

from cycler import cycler
from matplotlib import ticker

from scipy.stats import linregress


plt.style.use("classic")
plt.rcParams["lines.linewidth"]=2
plt.rcParams['font.family'] = 'Arial'
plt.rcParams["font.size"]=13
plt.rcParams['axes.prop_cycle'] = cycler('color',plt.get_cmap('Paired').colors)

##################################
# Read from files

d_80=np.loadtxt("d_ag80.csv",dtype=int) # years descending; so swap
d_80=np.flip(d_80)

pop_80=np.loadtxt("pop80.csv",dtype=int) # years ascending
pop_80_corr=np.loadtxt("pop80_corr.csv",dtype=int)

# df=pd.read_excel("Überprüfung CMR mit KMR.xlsx",
#                  sheet_name="ag 80+")

years=np.linspace(2013,2023,11).astype(int)

#####################################

# Calculations

cmr=d_80/pop_80
kmr=d_80/pop_80_corr

cmr_params=linregress(years[0:7]-2013,cmr[0:7])
cmr_fit=cmr_params.slope*(years-2013)+cmr_params.intercept

psc_cmr=cmr/cmr_fit-1

kmr_params=linregress(years[0:7]-2013,kmr[0:7])
kmr_fit=kmr_params.slope*(years-2013)+kmr_params.intercept

psc_kmr=kmr/kmr_fit-1

#####################################

fig,ax=plt.subplots(2,1,figsize=(16,10))

for k in [0,1]:
    ax[k].xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:g}"))

    ax[k].set_xlim(2012.5,2023.5)
    ax[k].set_xticks(years) 
    
    ax[k].set_ylim(0.093*1000,0.113*1000)
   



##################################
    
ax[0].grid(True)
ax[0].set_xticklabels([])
ax[0].set_ylabel("Deaths per 1000 in Age Group 80+")

ax[0].plot(years,cmr*1000,linestyle="--",color="dodgerblue",
        label="CMR")
ax[0].plot(years,cmr_fit*1000,color="red",
        label="Fit CMR 2013-19")


sig_low=min(psc_cmr[0:6])
sig_hi=max(psc_cmr[0:6])

d_hi=cmr_fit*1000*(1+sig_hi)
d_lo=cmr_fit*1000*(1+sig_low)
ax[0].plot(years,d_hi,color="lightgrey",linestyle="--")
ax[0].plot(years,d_lo,color="lightgrey",linestyle="--")


ax[0].fill_between(years,d_hi,d_lo,color="gainsboro",
                       alpha=0.6)

ax[0].legend(loc="lower left", edgecolor="white")
##################################
ax[1].grid(True)

ax[1].set_xticklabels(years,rotation=90)
ax[1].set_xlabel("Year")
ax[1].set_ylabel("Deaths per 1000 in Age Group 80+")


ax[1].plot(years,kmr*1000,linestyle="--",color="dodgerblue",
        label="CorrMR")
ax[1].plot(years,kmr_fit*1000,color="red",
        label="Fit CorrMR 2013-19")

sig_low=min(psc_kmr[0:7])
sig_hi=max(psc_kmr[0:7])

d_hi=kmr_fit*1000*(1+sig_hi)
d_lo=kmr_fit*1000*(1+sig_low)
ax[1].plot(years,d_hi,color="lightgrey",linestyle="--")
ax[1].plot(years,d_lo,color="lightgrey",linestyle="--")


ax[1].fill_between(years,d_hi,d_lo,color="gainsboro",
                       alpha=0.6)

ax[1].legend(loc="lower left", edgecolor="white")


plt.savefig("../figures/Fig S8 CMR KMR 80+.png")