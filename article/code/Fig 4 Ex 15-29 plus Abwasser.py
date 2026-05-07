# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 13:46:20 2022
Linearer Trend für Sterbezahlen
von 2020 bis 22


@author: Martin
"""




import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import linregress
from cycler import cycler
from matplotlib.ticker import FuncFormatter



def format_func(value, tick_number):
    return f'{value:,.0f}'.replace(',', ' ')  
    # Umständlich Tausendertrennzeichen, ohne Dezimalstellen



##############################################################

df=pd.read_csv("../../data_proc/deaths/Deaths monthly 15-29.csv",index_col=0)
df=df.drop(columns="AG")


##############################################################


plt.figure(figsize=(10,7),dpi=100)
plt.clf()
plt.style.use("classic")
plt.rcParams["lines.linewidth"]=2
plt.rcParams['font.family'] = 'Arial'
plt.rcParams["font.size"]=13
plt.rcParams['axes.prop_cycle'] = cycler('color',
                                         plt.get_cmap('Paired').colors)


##############################################################


plt.subplot(211)
bl_13_19=[];bl_16_19=[]
monate=np.linspace(1,12,12).astype(int)
lbl_monate=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
y_13_19=np.linspace(2019,2013,7)
y_16_19=np.linspace(2019,2016,4)

d_lo=[];d_hi=[]

for m in monate:
    # Werte 13-19 + LR
    t_13_19=df[df.keys()[m]].to_numpy()[4:11]
    lr1=linregress(y_13_19,t_13_19)
    
    # xtrapolation
    
    xtrapol1=lr1.intercept+lr1.slope*2022
    bl_13_19.append(xtrapol1)
    
    # Min/Max
    fit_13_19=lr1.intercept+lr1.slope*y_13_19
    psc=t_13_19/fit_13_19-1
    min_sigma=min(psc);max_sigma=max(psc)
    
    d_lo.append(xtrapol1*(1+min_sigma))
    d_hi.append(xtrapol1*(1+max_sigma))
    
  

plt.xlim(1,12)
plt.xticks(monate,labels=[])
plt.ylim(240,460)
plt.grid(True)

plt.plot(monate,bl_13_19,label="Trend Projection from 2013-2019")
plt.ylabel("Deaths per month in Age Group 15-29")
#plt.plot(monate,bl_16_19,label="16-19")
t_2022=df[df["Jahr"]==2022].to_numpy()[0][1:13]

plt.plot(monate,t_2022,label="Reported Deaths 2022, Age Group 15-29",
         color="red")


plt.gca().fill_between(monate,d_hi,d_lo,color="gainsboro",
                       alpha=0.6)

plt.plot(monate,d_lo,color="lightgrey",linestyle="--")
plt.plot(monate,d_hi,color="lightgrey",linestyle="--")



plt.legend(loc="upper left")


######################################
handles, labels = plt.gca().get_legend_handles_labels()
dummy = plt.Rectangle((0,0), 1, 1, fc="gainsboro", edgecolor = 'none')
handles.append(dummy)
labels.append("Historical Min/Max")


plt.legend(handles,labels,loc="upper left",
           facecolor="white",edgecolor="white",fontsize=10)


######################################

plt.subplot(212)
plt.grid("True")

plt.xticks(monate,labels=lbl_monate,rotation=45)

plt.ylim(0,100)

##################
exzm=t_2022-bl_13_19

plt.plot(monate,exzm,label="Excess Deaths calculated")

abwasser=pd.read_csv("../../data_proc/wastewater/c19_2022_abwasser_monate_mw.csv")
#abwasser=pd.read_csv("../../RKI/amelag/mittelwerte_vl_2022.csv")

plt.plot(abwasser["month"],abwasser["viruslast"]/4000,label="Wastewater Load (scaled by 4000)")

plt.legend(loc="upper left",edgecolor="none",fontsize=10)

plt.savefig("../figures/Fig 4 Exm 15-29 in 2022 plus Abwasser.png")