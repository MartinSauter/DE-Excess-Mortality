# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 13:51:19 2023

@author: Martin Sauter
"""



import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from scipy.stats import linregress

from matplotlib.ticker import FuncFormatter
from cycler import cycler


def format_func(value, tick_number):
    return f'{value:,.0f}'.replace(',', ' ')  
    # Umständlich Tausendertrennzeichen, ohne Dezimalstellen



df=pd.read_csv("../../data_raw/deaths/12613-0002_de.csv",delimiter=";",
               skiprows=5,skipfooter=4,index_col=0,engine='python')

j=df.index.to_numpy()
jf=j-2010
de=df["Insgesamt"].to_numpy()




######################################################

plt.figure(figsize=(10,7),dpi=100)
plt.clf()
plt.style.use("classic")
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 13
plt.rcParams['legend.fontsize'] = 11
plt.rcParams['axes.prop_cycle'] = cycler('color',
                                          plt.get_cmap('Paired').colors)

# plt.title("Deaths in Germany; Source: destatis, Vis. M. Sauter",
#           fontsize=18)

plt.xlim(2009,2025)
# plt.yticks(np.arange(825000,1002500,25000))

plt.plot(j,de,marker="o",color="salmon",
         label="Observed Deaths in Germany",
         markeredgecolor="salmon",lw=0.5,ls=":")

plt.grid(True,color="black",linewidth=0.5)

ax = plt.gca()
ax.set_xticks(np.linspace(2010,2024,15).astype(int))
ax.set_xticklabels(np.linspace(2010,2024,15).astype(int),
                   fontsize=13,rotation=45)


# Formatter für die y-Achse setzen
ax.yaxis.set_major_formatter(FuncFormatter(format_func))



plt.xlabel("Year",fontsize="13")
ax.spines[:].set_color('black')
plt.ylabel("Annual Deaths",fontsize="13")

print("Tab. S1")
print("---------------------------------------------------------")
print(
    f"{'Timespan':<16}"
    f"{'LR Exp.2023':>16}"
    f"{'PR Exp.2023':>16}"
    f"{'Diff. PR-LR':>16}"
   
)

for sj in np.arange(0,7):
    #print(j[sj:10])
    # lr
    k1=linregress(jf[sj:10],de[sj:10])
    f1=k1.slope*jf+k1.intercept
    
   
    
    plt.plot(j[sj:],f1[sj:],marker="",linewidth=2,
             label="LR Timespan: "+str(int(j[sj]))+"-2019",
             alpha=0.6,
             linestyle=(0,(20,5)))
    print(f"{f'{j[sj]}-2019':16}{f1[-2]:16.0f}",end="")
         
    #poisson
    k2=linregress(jf[sj:10],np.log10(de[sj:10]))
                  
    f2=np.power(10,k2.slope*jf+k2.intercept)
    plt.plot(j[sj:],f2[sj:],marker=".",linewidth=1,
             label="PR Timespan: "+str(int(j[sj]))+"-2019",
             alpha=0.6,markersize=5,
             linestyle="")
    
    print(f"{f2[-2]:16.0f}",end="")
    
    abs_diff=f2[-2]-f1[-2] 
    rel_diff=abs_diff/f1[-2]
    
    print(f"{rel_diff:16.2%}")
         
plt.legend(loc="upper left",facecolor="white",
           edgecolor="white")

plt.tight_layout()




###########################################################
# Actuary models




plt.savefig("../figures/Fig S1 de multi lr poisson.png",dpi=1000)
plt.savefig("../figures/Fig S1 de multi lr poisson.svg")
plt.savefig("../figures/Fig S1 de multi lr poisson.tif",dpi=600,
            pil_kwargs={"compression": "tiff_lzw"})

"""
Result:
Tab. S2
---------------------------------------------------------
Timespan             LR Exp.2023     PR Exp.2023     Diff. PR-LR
2010-2019                 996696         1001263           0.46%
2011-2019                1001751         1006705           0.49%
2012-2019                 998625         1002617           0.40%
2013-2019                 997148         1000622           0.35%
2014-2019                1008436         1013306           0.48%
2015-2019                 976121          977034           0.09%
2016-2019                 994043          996220           0.22%
    
    
"""

