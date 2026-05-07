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



df=pd.read_csv("../../data_raw/deaths/12613-0002_de.csv",delimiter=";",
               skiprows=5,skipfooter=4,index_col=0,engine='python')

j=df.index.to_numpy()
jf=j-2010
de=df["Insgesamt"].to_numpy()



#################################################################
# j=np.linspace(2010,2023,14)
# jf=j-2019
# de=np.asarray([858768,852328,869582,893825,868356,
#                925200,910902,932272,954874,939520,
#                985572,1023687,1066341,1028206])



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

print("Tab. S1")
print("---------------------------------------------------------")
print(
    f"{'Timespan':<10}"
    f"{'Exp.2023':>12}"
    f"{'Slope  ':>8}"
    f"{'Intercept':>8}"
    f"{'Hist. Min':>12}"
    f"{'Hist. Max':>12}"
)
#print("Timespan\tExp. 2023\t Slope \t Intercept \t Hist. Min/Max")

for sj in np.arange(0,7):
    #print(j[sj:10])
    k1=linregress(jf[sj:10],de[sj:10])
    f1=k1.slope*jf+k1.intercept
    
    psc=de[sj:10]/f1[sj:10]-1
    hist_max, hist_min=max(psc),min(psc)
    
    plt.plot(j[sj:],f1[sj:],marker="",linewidth=2,
             label="Timespan: "+str(int(j[sj]))+"-2019",
             alpha=1,
             linestyle=(0,(20,5)))
    print(f"{j[sj]:4}"+"-2019\t"
          f"{k1.slope*4+k1.intercept:.0f}\t"
          f"{k1.slope:>11.0f}\t"
          f"{k1.intercept:>8.0f}\t"
          f"{hist_min:>6.2%}\t"
          f"{hist_max:>6.2%}\t")

plt.legend(loc="upper left",facecolor="white",
           edgecolor="white")

plt.tight_layout()

#plt.savefig("../figures/Fig S1 de multi lr.png")


"""
Result:
    
    Tab. S1
    ---------------------------------------------------------
    Timespan	Exp. 2023	 Slope 	 Intercept 	 Hist. Min/Max
    2010-2019	894908	11310		849669	-2.97%	2.09%	
    2011-2019	893138	12068		844866	-2.77%	2.21%	
    2012-2019	894455	11575		848156	-2.92%	2.12%	
    2013-2019	895193	11328		849880	-3.00%	2.06%	
    2014-2019	888553	13320		835272	-2.27%	2.59%	
    2015-2019	910770	7261		881725	-1.56%	1.60%	
    2016-2019	896432	10846		853050	-1.17%	1.60%	
    
"""