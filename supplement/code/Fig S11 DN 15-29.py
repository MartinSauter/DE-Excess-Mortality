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


df=pd.read_csv("../../data_raw/deaths/12613-0003_de.csv",sep=";",
               skiprows=6,skipfooter=4,index_col=0,engine="python")

# Keep only total number (delete m + f)

df=df.iloc[25:37]

# delete "Unknown" and "Total"
df=df.drop(columns={"Alter unbekannt","Insgesamt"})


# manipulate colums for better handling
# column "unter 5" becomes 4 (int)
df.columns=np.linspace(0,100,101).astype(int)

#d0=df.loc[:,0:14].sum(axis=1).to_numpy()
d15=df.loc[:,15:29].sum(axis=1).to_numpy()






years=np.linspace(2013,2023,11).astype(int)

########################################
#  Fit 13-19

d15_params_1=linregress(years[0:7]-2013,d15[0:7])
d15_fit_1=d15_params_1.slope*(years-2013)+d15_params_1.intercept

psc_1=d15/d15_fit_1-1

########################################
#  Fit 16-19

d15_params_2=linregress(years[3:7]-2016,d15[3:7])
d15_fit_2=d15_params_2.slope*(years-2016)+d15_params_2.intercept

psc_2=d15/d15_fit_2-1

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

#plt.savefig("../figures/Fig S9 DN 15 29.png")
plt.savefig("../figures/Fig S11 DN 15-29.png",dpi=600)
plt.savefig("../figures/Fig S11 DN 15-29.tif",dpi=600,
            pil_kwargs={"compression": "tiff_lzw"})

#Output For Tab S7
print("Tab S7, P-Score AG 15-29")
print("\t\t"+
      f"{'2020':>10}"
      f"{'2021':>10}"
      f"{'2022':>10}"
      f"{'2023':>10}"
      f"{'Min.':>10}"
      f"{'Max.':>10}"
      )



print("Trend 16-19"+
      f"{psc_2[-4]:>10.2%}"
      f"{psc_2[-3]:>10.2%}"
      f"{psc_2[-2]:>10.2%}"
      f"{psc_2[-1]:>10.2%}"
      f"{min(psc_2[3:7]):>10.2%}"
      f"{max(psc_2[3:7]):>10.2%}"
      )

print("Trend 13-19"+
      f"{psc_1[-4]:>10.2%}"
      f"{psc_1[-3]:>10.2%}"
      f"{psc_1[-2]:>10.2%}"
      f"{psc_1[-1]:>10.2%}"
      f"{min(psc_1[0:7]):>10.2%}"
      f"{max(psc_1[0:7]):>10.2%}"
      )

