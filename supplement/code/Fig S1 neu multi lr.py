# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 13:51:19 2023

@author: Martin Sauter
"""



import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from scipy.stats import linregress
from matplotlib import ticker
from matplotlib.ticker import FuncFormatter
import matplotlib.patches as patches
from cycler import cycler


def format_func(value, tick_number):
    return f'{value:,.0f}'.replace(',', ' ')  
    # Umständlich Tausendertrennzeichen, ohne Dezimalstellen




#################################################################
j=np.linspace(2010,2023,14)
jf=j-2019
de=np.asarray([858768,852328,869582,893825,868356,
               925200,910902,932272,954874,939520,
               985572,1023687,1066341,1028206])



######################################################

plt.figure(figsize=(10,7),dpi=100)
plt.clf()
plt.style.use("classic")
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 13
plt.rcParams['axes.prop_cycle'] = cycler('color',
                                          plt.get_cmap('Paired').colors)

# plt.title("Deaths in Germany; Source: destatis, Vis. M. Sauter",
#           fontsize=18)

plt.xlim(2009,2024)
# plt.yticks(np.arange(825000,1002500,25000))

plt.plot(j,de,marker="o",color="salmon",
         label="Observed Deaths in Germany",
         markeredgecolor="salmon",lw=0.5,ls=":")

plt.grid(True,color="black",linewidth=0.5)

ax = plt.gca()
ax.set_xticks(np.linspace(2010,2023,14).astype(int))
ax.set_xticklabels(np.linspace(2010,2023,14).astype(int),
                   fontsize=13,rotation=45)


# Formatter für die y-Achse setzen
ax.yaxis.set_major_formatter(FuncFormatter(format_func))



plt.xlabel("Year",fontsize="13")
ax.spines[:].set_color('black')
plt.ylabel("Annual Deaths",fontsize="13")


for sj in np.arange(0,7):
    print(j[sj:10])
    k1=linregress(jf[sj:10],de[sj:10])
    f1=k1.slope*jf+k1.intercept
    print(f1)
    plt.plot(j[sj:],f1[sj:],marker="",linewidth=2,
             label="Timespan: "+str(int(j[sj]))+"-2019",
             alpha=1,
             linestyle=(0,(20,5)))
   

plt.legend(loc="upper left",facecolor="white",
           edgecolor="white")

plt.tight_layout()

plt.savefig("../figures/Fig S1 de multi lr.png")