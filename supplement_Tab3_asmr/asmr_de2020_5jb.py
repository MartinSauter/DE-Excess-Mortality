# -*- coding: utf-8 -*-
"""
Created on Tue May 12 21:13:56 2026

@author: Martin Sauter
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Dec 29 11:02:12 2025

@author: Martin Sauter
"""
import pandas as pd
import numpy as np

#from std_pops.std_pops import *
from matplotlib import pyplot as plt
from matplotlib import ticker

from scipy.stats import linregress

##############################################################
# Def. std-pops

# 0-9,10-19,......80-89+90+
esp_2013_10_jb=np.array([10.5,11,12,13.5,14,13.5,11.5,9,4+1])/100

#####################################

who_2015_10jb=np.array([17.5439,17.0640,16.1443,14.7548,12.6256,9.9165,
6.6777,3.7287,1.3495+0.1899+0.050])/100

##################################
# de_2020_5jb_85=np.array([
#         4.763,4.481,4.452,4.737,5.541,6.102,6.608,6.360,5.903,
#         6.341,8.068,8.101,6.791,5.843,4.418,4.661,3.961,
#         1.880+0.791+0.178+0.020]) / 100


de_2020_10jb=np.array([
        9.244,9.189,11.643,12.968,
        12.243,16.169,12.633,9.079,
        5.841+0.969+0.020]) / 100

##############################################################

def fit_n_print(df,marker):
    y=df.loc[marker].values
    
    x=np.array(list(asmr.keys()), dtype=int)
   
    lr=linregress(x[0:7],y[0:7])
    lf=lr.slope*x+lr.intercept
    psc=y/lf-1
    
    print("Relative Excess for Standard Population DE2020")
    print("---------------------------------------------")
    for k in [-4,-3,-2,-1]:
        print(f"{int(x[k])}\t{psc[k]:.2%}")
    print("\n")
    print("Historical Min/Max:")
    print(f"{min(psc[0:7]):.2%}\t\t{max(psc[0:7]):.2%}")


        
        
    
    
    

##############################################################
p=pd.read_csv("./data_proc/pop/Pop_5y.tsv",sep="\t",index_col=0)

p=p.drop(columns=["2024"])


d=pd.read_csv("./data_proc/deaths/Deaths_5y.tsv",sep="\t",index_col=0)

cmr=d/p

std_pop=p["2020"].values/p["2020"].sum()



asmr=cmr.mul(std_pop,axis=0)
asmr.loc["ASMR_DE_2020"]=asmr.sum()

fit_n_print(asmr,"ASMR_DE_2020")

# plt.plot(asmr.keys().values.astype(int),asmr.loc["ASMR_DE2020"],
#          marker="o",color="dodgerblue",ls="")

# plt.gca().xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:g}"))
# plt.xticks(rotation=90)
# plt.grid(True)


    
           

             
