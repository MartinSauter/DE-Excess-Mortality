# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 10:23:32 2022

@author: Martin Sauter
"""
import matplotlib as mpl
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import linregress
from cycler import cycler
from matplotlib.ticker import FuncFormatter



def format_func(value, tick_number):
    return f'{value:,.0f}'.replace(',', ' ')  
    # Umständlich Tausendertrennzeichen, ohne Dezimalstellen




#   Ab 22.10: Excel csv mit ";"


tmp=pd.read_csv("DEUTNPstfmout_wochen.csv",sep=",",
                encoding="ISO8859-1",index_col=0)

################################################


woche_marker_13bis19=[]     
################################################
#
#   Min-Max Vorjahre 
d_hi=[]
d_lo=[]

sigma_min=[]
sigma_max=[]

#################################################
 
for woche in range(1,53,1):
       
    todesfälle=[]
    for j in range(2013,2020,1):
        print(j,woche)
        cond=((tmp["Year"]==j) & (tmp["Week"]==woche))
        todesfälle.append(tmp["Total"][cond].to_list()[0])
    
    
    ###################
    #   2020 von 13-19
    jahre_vorher=np.linspace(2013,2019,7)
    
    # Fit / LR
    k1=linregress(jahre_vorher-2013,todesfälle)
    
    # Modell für Alte Jahre
    fit_vorher=k1.slope*(jahre_vorher-2013)+k1.intercept
    
    # Rel. Abweichung
    
    sigma=np.array(todesfälle)/fit_vorher-1
    sigma_min,sigma_max=np.min(sigma),np.max(sigma)
    #2021:
    f1=k1.slope*9+k1.intercept
    
    woche_marker_13bis19.append(f1)
    d_lo.append(f1*(1+sigma_min))
    d_hi.append(f1*(1+sigma_max))
    
   
#############################################################
################################################################

plt.figure(figsize=(10,7),dpi=100)
plt.clf()
plt.style.use("classic")
plt.rcParams["lines.linewidth"]=2
plt.rcParams['font.family'] = 'Arial'
plt.rcParams["font.size"]=14
plt.rcParams['axes.prop_cycle'] = cycler('color',
                                         plt.get_cmap('Paired').colors)



# plt.suptitle("Mortality in Germany 2020 / Data: mortality.org & destatis.de , Vis. M. Sauter ",
#              fontsize=18)

plt.subplot(211)
plt.grid(True)

#   Y-Achse
#
#-----------------------------------------
plt.ylim(15000,29000)
plt.gca().set_yticks(np.linspace(15000,29000,8))
plt.gca().set_yticklabels(np.linspace(15000,25000,8).astype(int))

plt.ylabel("Weekly Deaths Reported") 


plt.gca().yaxis.set_major_formatter(FuncFormatter(format_func))

plt.xlim(1,52)

xticks=np.array([1,4,8,12,16,20,24,28,32,36,40,44,48,52]).astype(int)


plt.gca().set_xticks(xticks)
plt.gca().set_xticklabels([])

#-------------------------------------

plt.plot(np.linspace(1,52,52),woche_marker_13bis19,
         linestyle="dashed",lw=1.5,color="dodgerblue",
         label="Trend Projection 2013-2019")
#color="dodgerblue",
# Jahr hier eintragen

d_2022=tmp[tmp["Year"]==2022]["Total"].to_numpy()

plt.plot(np.linspace(1,52,52),d_2022,color="red",
         label="Reported Deaths 2022")

##################################


#Schattierung
plt.gca().fill_between(np.linspace(1,52,52),d_hi,d_lo,color="gainsboro",
                       alpha=0.6)

plt.plot(np.linspace(1,52,52),d_lo,color="lightgrey",linestyle="--")
plt.plot(np.linspace(1,52,52),d_hi,color="lightgrey",linestyle="--")

######################################
handles, labels = plt.gca().get_legend_handles_labels()
dummy = plt.Rectangle((0,0), 1, 1, fc="gainsboro", edgecolor = 'none')
handles.append(dummy)
labels.append("Sigma Min/Max")


plt.legend(handles,labels,loc="upper center",
           facecolor="white",edgecolor="white")

###########################################

c19tote=pd.read_csv('./C19 Todesfälle 2022 Wochen gesamt.txt',
                     delimiter="\s+")
# c19tote=pd.read_csv('../../RKI/Todesfälle/C19 Todesfälle 2022 Wochen gesamt.txt',
#                     delimiter="\s+")

c19tote=c19tote[c19tote["Sterbejahr"]==2022]
plt.plot(c19tote["Sterbewoche"],c19tote["Todesfälle"], 
         label="COVID19-Deaths weekly reported by RKI")

# plt.legend(loc="upper left",prop={'size': 15})

#abwasser=pd.read_csv("../../RKI/amelag/c19_2022_abwasser.csv")
abwasser=pd.read_csv("./c19_2022_abwasser.csv")

# #################################

plt.subplot(212)

plt.grid(True)

plt.xlabel("Calendar Week")
plt.xlim(1,52)


plt.gca().set_xticks(xticks)
plt.gca().set_xticklabels(xticks)

plt.ylim(0,9000)
plt.gca().yaxis.set_major_formatter(FuncFormatter(format_func))

# plt.plot(c19tote["Sterbewoche"],c19tote["Todesfälle"], 
#          label="COVID19-Deaths weekly reported by RKI",
#          color="black")

xd=d_2022-woche_marker_13bis19
plt.plot(np.linspace(1,52,52),xd,label="Calc. Excess Deaths")

plt.plot(c19tote["Sterbewoche"],c19tote["Todesfälle"]*2, 
         label="COVID19-Deaths weekly reported by RKI (scaled x2)",
         color="black")


plt.plot(abwasser["Woche"],abwasser["viruslast"]/100,
         label="COVID19 Wastewater Load by Amelag/RKI (÷200)",
         color=mpl.colormaps["Paired"].colors[-4],ls="-")
plt.legend(loc="upper center",facecolor="white",edgecolor="white")

plt.tight_layout()

plt.savefig("../figures/Fig 2c de üs 2022 baseline 13-19 .png")
