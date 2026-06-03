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
plt.rcParams["font.size"]=13
plt.rcParams['axes.prop_cycle'] = cycler('color',
                                         plt.get_cmap('Paired').colors)


########################################################################



df=pd.read_csv("../../data_raw/pop/12411-0005_$F.csv",sep=";",
               skiprows=6,skipfooter=4,index_col=0,engine="python",
               encoding="ISO8859")

#  delete Data before 2009
df=df.iloc[:,4:]


# 31.12.2008 = 2009 in column headers
jahre=np.linspace(2009,2024,16).astype(int)
df.columns=jahre

pop=df.loc["Insgesamt"].values

"""
array([82002356, 81802257, 81751602, 80327900, 80523746, 80767463,
       81197537, 82175684, 82521653, 82792351, 83019213, 83166711,
       83155031, 83237124, 84358845, 84669326])
"""



ax.set_xticks(jahre)
ax.set_xticklabels(jahre,rotation=45)


# Formatter für die y-Achse setzen
ax.yaxis.set_major_formatter(FuncFormatter(format_func))


ax.set_xlabel("Year")
ax.set_ylabel("Total Population")
ax.spines[:].set_color('black')
ax.plot(jahre,pop,lw=0.5,marker="o",color="salmon",
         label="Observed Deaths in Germany",markersize=10,
         markeredgecolor="salmon",ls="--")
#ax.set_ylabel("Population Number")

c=plt.get_cmap('Paired').colors
# #############################################################
ax.axvspan(2011,2012, color=c[4], alpha=0.3)
ax.axvspan(2015,2016, color=c[2],alpha=0.3)
ax.axvspan(2022,2023, color=c[2],alpha=0.3)

# ######################################
plt.grid(True)
plt.tight_layout()

plt.savefig("../figures/Fig S6 Bev Zeitverlauf.png",dpi=600)
plt.savefig("../figures/Fig S6 Bev Zeitverlauf.tif",dpi=600,
            pil_kwargs={"compression": "tiff_lzw"})