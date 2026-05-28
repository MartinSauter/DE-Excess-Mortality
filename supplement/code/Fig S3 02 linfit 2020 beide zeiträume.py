# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 10:23:32 2022

@author: Martin Sauter
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



plt.style.use("classic")

#   Ab 22.10: Excel csv mit ";"


tmp=pd.read_csv("../../data_proc/deaths/DEUTNPstmfout_weeks.csv",sep=",",
                encoding="ISO8859-1",index_col=None)


woche_marker_13bis19=[]     
woche_marker_15bis19=[]   

hi_b=[]
lo_b=[]

 

for woche in range(1,53,1):
    
    
    
    jahr=[]
    for j in range(2013,2020,1):
        #print(j,woche)
        cond=((tmp["Year"]==j) & (tmp["Week"]==woche))
        jahr.append(tmp["Total"][cond].to_list()[0])
    
    
    ###################
    #   2020 von 13-19
    k1=linregress(np.linspace(2013,2019,7)-2013,jahr)
    f1=k1.slope*7+k1.intercept
    
    woche_marker_13bis19.append(f1)
    
    ####################
    #   2020 von 15-19
    
    k2=linregress(np.linspace(2015,2019,5)-2015,jahr[2:])
    f2=k2.slope*5+k2.intercept
    
    woche_marker_15bis19.append(f2)
    
    jahr_list=[]
    
    for jahr in range(2020,2023,1):
         
         cond=((tmp["Year"]==jahr) & (tmp["Week"]==woche))
         jahr_list.append(tmp["Total"][cond].to_list()[0])
         
    
    
   
#############################################################


plt.figure(figsize=(10,7),dpi=100)
plt.clf()
plt.style.use("classic")
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['axes.prop_cycle'] = cycler('color',
                                         plt.get_cmap('Paired').colors)




plt.subplot(111)
plt.grid(True)

#-----------------------------------------
plt.ylim(15000,25000)
plt.gca().set_yticks(np.linspace(15000,25000,6))
plt.gca().set_yticklabels(np.intp(np.linspace(15000,25000,6)),fontsize=18)

plt.ylabel("Weekly Deaths Reported",fontsize=18)



plt.gca().yaxis.set_major_formatter(FuncFormatter(format_func))

plt.xlabel("Calendar Week",fontsize=18)
plt.xlim(1,52)


xticks=np.array([1,4,8,12,16,20,24,28,32,36,40,44,48,52]).astype(int)


plt.gca().set_xticks(xticks)
plt.gca().set_xticklabels(xticks,fontsize=18)

#-------------------------------------



plt.plot(np.linspace(1,52,52),woche_marker_15bis19,
         linestyle="dashed",lw=2,
         label="Trend Projection 2015-2019")

plt.plot(np.linspace(1,52,52),woche_marker_13bis19,
         linestyle="dashed",lw=2,
         label="Trend Projection 2013-2019")


d_2020=tmp[tmp["Year"]==2020]["Total"].to_numpy()

plt.plot(np.linspace(1,53,53),d_2020,color="red",
         label="Reported Deaths 2020")

##################################




handles, labels = plt.gca().get_legend_handles_labels()
dummy = plt.Rectangle((0,0), 1, 1, fc="gainsboro", 
                      edgecolor = 'none')
handles.append(dummy)


plt.legend(handles,labels,loc="upper left",
           facecolor="white",edgecolor="white")


plt.fill_between(np.linspace(1,11,11), woche_marker_13bis19[0:11], 
                 woche_marker_15bis19[0:11], 
                 color="gainsboro",alpha=0.3)


plt.tight_layout()


plt.savefig("../figures/Fig S3 de üs 2020 2 baselines.tif",dpi=600,
            pil_kwargs={"compression": "tiff_lzw"})


delta_flu=sum(woche_marker_13bis19[0:10])-sum(woche_marker_15bis19[0:10])
print("Difference CW 0-10:",int(delta_flu))

delta_heat=sum(woche_marker_13bis19[24:36])-sum(woche_marker_15bis19[24:36])
print("Difference CW 24-36",int(delta_heat))


