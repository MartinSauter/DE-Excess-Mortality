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



#################################################################
# Kuhbander
kr_h=[0,981557,989707,998545]
kr_f=[0,974875,976341,978263]
kr_n=[0,988288,1003270,1018827]

kr_h[0]=kr_h[1]-1/2*(kr_h[3]-kr_h[1])
kr_f[0]=kr_f[1]-1/2*(kr_f[3]-kr_f[1])
kr_n[0]=kr_n[1]-1/2*(kr_n[3]-kr_n[1])


######################################################
# De Nicola
dn=[900000,920000,940000,960000,979255]


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
    f"{'Timespan':<10}"
    f"{'Exp.2020':>12}"
    f"{'Exp.2023':>12}"
    f"{'Slope  ':>8}"
    f"{'Intercept':>8}"
    f"{'Hist. Min':>12}"
    f"{'Hist. Max':>12}"
)

for sj in np.arange(0,7):
    #print(j[sj:10])
    k1=linregress(jf[sj:10],de[sj:10])
    f1=k1.slope*jf+k1.intercept
    
    psc=de[sj:10]/f1[sj:10]-1
    hist_max, hist_min=max(psc),min(psc)
    
    plt.plot(j[sj:],f1[sj:],marker="",linewidth=2,
             label="Timespan: "+str(int(j[sj]))+"-2019",
             alpha=0.3,
             linestyle=(0,(20,5)))
    print(f"{j[sj]:4}"+"-2019\t"
          f"{f1[-5]:10.0f}"
          f"{f1[-2]:10.0f}"
          f"{k1.slope:>11.0f}\t"
          f"{k1.intercept:>8.0f}\t"
          f"{hist_min:>6.2%}\t"
          f"{hist_max:>6.2%}\t")

plt.legend(loc="upper left",facecolor="white",
           edgecolor="white")

plt.tight_layout()

plt.savefig("../figures/Fig S1 de multi lr.tif",dpi=600,
           pil_kwargs={"compression": "tiff_lzw"})
plt.savefig("../figures/Fig S1 de multi lr.png",dpi=600)


###########################################################
# Actuary models


dashes=(5,2)
n=10;m=13
plt.plot(j[n:m],kr_n[1:],color="lightgrey",linewidth=2,linestyle="--",
         label='Exp. Deaths Kuhbandner, Trend="None"',
         marker="D",markersize=4,markeredgecolor="lightgrey",
         dashes=dashes)

plt.plot(j[n:m],kr_h[1:],color="grey",linewidth=2,linestyle="--",
         label='Exp. Deaths Kuhbandner, Trend="Half"',
         marker="D",markersize=4,markeredgecolor="grey",
         dashes=dashes)

plt.plot(j[n:m],kr_f[1:],color="black",linewidth=2,linestyle="--",
          label='Exp. Deaths Kuhbandner, Trend="Full"',
          marker="D",markersize=4,
          dashes=dashes)

n=-6;m=-4

plt.plot(j[n:m],kr_n[0:2],color="lightgrey",linewidth=1,linestyle="dotted")

plt.plot(j[n:m],kr_h[0:2],color="grey",linewidth=1,linestyle="dotted")

plt.plot(j[n:m],kr_f[0:2],color="black",linewidth=1,linestyle="dotted")



plt.plot(j[6:11],dn,color="indigo",linewidth=1.5,ls="--",
         label="Exp. Deaths De Nicola",marker="D",markersize=5,
         markerfacecolor="none",markeredgecolor="indigo",dashes=dashes)



plt.legend(loc="upper left",facecolor="white",
           edgecolor="white")



plt.savefig("../figures/Fig S3 de multi lr add act models.png",dpi=600)
           
plt.savefig("../figures/Fig S3 de multi lr add act models.tif",dpi=600,
           pil_kwargs={"compression": "tiff_lzw"})

"""
Result:
Tab. S1
---------------------------------------------------------
Timespan      Exp.2020    Exp.2023 Slope  Intercept   Hist. Min   Hist. Max
2010-2019	    962767    996696      11310	  849669	-2.97%	 2.09%	
2011-2019	    965547   1001751      12068	  844866	-2.77%	 2.21%	
2012-2019	    963902    998625      11575	  848156	-2.92%	 2.12%	
2013-2019	    963163    997148      11328	  849880	-3.00%	 2.06%	
2014-2019	    968475   1008436      13320	  835272	-2.27%	 2.59%	
2015-2019	    954337    976121       7261	  881725	-1.56%	 1.60%	
2016-2019	    961506    994043      10846	  853050	-1.17%	 1.60%	
    
    
"""

