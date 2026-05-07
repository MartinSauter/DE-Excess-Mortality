# -*- coding: utf-8 -*-
"""
Created on Fri May 20 22:18:38 2022

@author: Martin Sauter
"""



import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import linregress
from matplotlib import ticker
from matplotlib.ticker import FuncFormatter

from cycler import cycler



def format_func(value, tick_number):
    return f'{value:,.0f}'.replace(',', ' ')  
    # Umständlich Tausendertrennzeichen, ohne Dezimalstellen

#####################################################


#plt.figure(figsize=(10,7),dpi=100)
fig,ax=plt.subplots(3,2,figsize=(12,8),dpi=100)

#ax[3,1].remove()


plt.style.use("classic")
plt.rcParams["lines.linewidth"]=2
plt.rcParams['font.family'] = 'Arial'
plt.rcParams["font.size"]=13
plt.rcParams['axes.prop_cycle'] = cycler('color',
                                         plt.get_cmap('Paired').colors)


########################################################################


df=pd.read_csv("../../data_proc/pop/Pop_20y_back_2005.tsv",sep="\t",
               index_col=0)




df=df.drop(columns=["2005","2006","2007","2024"])
jahre=np.linspace(2008,2023,16).astype(int)
x=0;y=0
k=0
lbls=df.index.values.astype(str)
#lbls=["0-14","15-29","30-39","40-59","60-79","80+"]

# with open("ausgabe.txt","w") as file:
#         print()

#for lbl in (ag0_15,ag15_29,ag30_39,ag40_59,ag60_79,ag80_):
for lbl in df.index:
    ag=df.loc[lbl,:].values
    
    x=k%2
    y=k//2
    ax[y,x].xaxis.set_major_formatter(ticker.StrMethodFormatter("{x:g}"))
    
    ax[y,x].yaxis.set_major_formatter(FuncFormatter(format_func))
    ax[y,x].set_xlim(2011,2024)#Alt war ab 2008
    ax[y,x].set_xticks(jahre) 
    
    if y==2: ax[y,x].set_xticklabels(jahre,rotation=90)
    else: ax[y,x].set_xticklabels([])
    
    if x==0: ax[y,x].set_ylabel("Population in age bands")
    ax[y,x].grid(True)
    ax[y,x].plot(jahre,ag,label=lbl,marker="x",linestyle="--",color="dodgerblue")
    
    # Fit
    
    lf=linregress(jahre[5:12]-2013,ag[5:12].astype(int))
    
    # Fit
    z=(jahre-2013)*lf.slope+lf.intercept  
  
            
    locs=["upper left","upper right",
          "upper left","upper right",
          "upper left","upper left"]
    
#     label=""
#     if k==0:label="Trend 2013-2019"
    
#
    if (x==0 and y==0):
        ax[y,x].plot(jahre[2:],z[2:],linestyle="-",color="red",label="Fit 2013-2019") #,label=label) 
    else:
        ax[y,x].plot(jahre[2:],z[2:],linestyle="-",color="red")
        #     ## sigma hi/lo
  
    ax[y,x].legend(loc=locs[k],fontsize=14,edgecolor="none")
    
    

    k+=1
    
# ######################################

plt.tight_layout()

plt.savefig("../figures/Fig S6 Bev Age Bands neu.png")