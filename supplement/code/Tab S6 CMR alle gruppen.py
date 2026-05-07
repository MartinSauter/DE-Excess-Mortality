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
# Deaths


df=pd.read_csv("../../data_raw/deaths/12613-0003_de.csv",sep=";",
               skiprows=6,skipfooter=4,index_col=0,engine="python")

# Keep only total number (delete m + f)

df=df.iloc[25:37]

# delete "Unknown" and "Total"
df=df.drop(columns={"Alter unbekannt","Insgesamt"})


# manipulate colums for better handling
# column "unter 5" becomes 4 (int)
df.columns=np.linspace(0,100,101).astype(int)

d0=df.loc[:,0:14].sum(axis=1).to_numpy()
d15=df.loc[:,15:29].sum(axis=1).to_numpy()
d30=df.loc[:,30:39].sum(axis=1).to_numpy()
d40=df.loc[:,40:59].sum(axis=1).to_numpy()
d60=df.loc[:,60:79].sum(axis=1).to_numpy()
d80=df.loc[:,80:101].sum(axis=1).to_numpy()




jahre=np.linspace(2013,2023,11).astype(int)
############################################
#
# Pop 
p=pd.read_csv("../../data_proc/pop/Pop_20y.tsv",sep="\t",index_col=0)
p=p.drop(columns=["2011","2012","2024"])
p0=p.loc["0-14",:].values
p15=p.loc["15-29",:].values
p30=p.loc["30-39",:].values
p40=p.loc["40-59",:].values
p60=p.loc["60-79",:].values
p80=p.loc["80+",:].values


#####################################
# Calc. Moratilty Rates

c30=d30/p30
c40=d40/p40
c60=d60/p60
c80=d80/p80

print("Tab S6, P-Score CMR")
print("\t"+f"{'2020':>10}"
      f"{'2021':>10}"
      f"{'2022':>10}"
      f"{'2023':>10}"
      f"{'Min.':>10}"
      f"{'Max.':>10}"
      )

for (lbl,c) in [("60-79",c60),("40-59",c40),("30-39",c30)]:
    fit=linregress(jahre[0:7],c[0:7])
    c_fit=jahre*fit.slope+fit.intercept
    psc=c/c_fit-1
    print(lbl+f"{psc[-4]:>10.2%}"
          f"{psc[-3]:>10.2%}"
          f"{psc[-2]:>10.2%}"
          f"{psc[-1]:>10.2%}"
          f"{min(psc[0:7]):>10.2%}"
          f"{max(psc[0:7]):>10.2%}"
          )
