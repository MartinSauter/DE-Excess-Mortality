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
from scipy.signal import savgol_filter



def format_func(value, tick_number):
    return f'{value:,.0f}'.replace(',', ' ')  
    # Umständlich Tausendertrennzeichen, ohne Dezimalstellen



plt.style.use("classic")

#   Ab 22.10: Excel csv mit ";"


tmp=pd.read_csv("../../data_proc/deaths/DEUTNPstmfout_weeks.csv",sep=",",
                encoding="ISO8859-1",index_col=None)

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
        #print(j,woche)
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
    #2023:
    f1=k1.slope*10+k1.intercept
    
    woche_marker_13bis19.append(f1)
    d_lo.append(f1*(1+sigma_min))
    d_hi.append(f1*(1+sigma_max))
    
   
#############################################################
################################################################

plt.figure(figsize=(10,7),dpi=100)
plt.clf()
plt.style.use("classic")
plt.rcParams['font.family'] = 'Arial'
plt.rcParams["font.size"]=14
plt.rcParams["lines.linewidth"]=2
plt.rcParams['axes.prop_cycle'] = cycler('color',
                                         plt.get_cmap('Paired').colors)



plt.subplot(211)
plt.grid(True)

#   Y-Achse
#
#-----------------------------------------
plt.ylim(15000,25000)
plt.gca().set_yticks(np.linspace(15000,25000,6))
plt.gca().set_yticklabels(np.linspace(15000,25000,6).astype(int))

plt.ylabel("Weekly Deaths Reported",fontsize=18)


plt.gca().yaxis.set_major_formatter(FuncFormatter(format_func))

plt.xlim(1,52)

xticks=np.array([1,4,8,12,16,20,24,28,32,36,40,44,48,52]).astype(int)


plt.gca().set_xticks(xticks)
plt.gca().set_xticklabels([])

#-------------------------------------

plt.plot(np.linspace(1,52,52),woche_marker_13bis19,
         linestyle="dashed",lw=1.5,color="dodgerblue",
         label="Trend Projection 2013-2019")


d_2023=tmp[tmp["Year"]==2023]["Total"].to_numpy()

plt.plot(np.linspace(1,52,52),d_2023,color="red",
         label="Reported Deaths 2023")

##################################


#Schattierung
plt.gca().fill_between(np.linspace(1,52,52),d_hi,d_lo,color="gainsboro",
                       alpha=0.6)

plt.plot(np.linspace(1,52,52),d_lo,color="lightgrey",linestyle="--")
plt.plot(np.linspace(1,52,52),d_hi,color="lightgrey",linestyle="--")



handles, labels = plt.gca().get_legend_handles_labels()
dummy = plt.Rectangle((0,0), 1, 1, fc="gainsboro", edgecolor = 'none')
handles.append(dummy)
labels.append("Historical Min/Max")


plt.legend(handles,labels,loc="upper center",
           facecolor="white",edgecolor="white")

# #################################

c19tote=pd.read_csv('../../data_proc/covid-deaths/c19_2023_tote_wochen.csv',
                    delimiter=",")


abwasser=pd.read_csv("../../data_proc/wastewater/c19_2023_abwasser.csv")

######################################
handles, labels = plt.gca().get_legend_handles_labels()
dummy = plt.Rectangle((0,0), 1, 1, fc="gainsboro", edgecolor = 'none')
handles.append(dummy)
labels.append("Historical Min/Max")


plt.legend(handles,labels,loc="upper center",
           facecolor="white",edgecolor="white")

# #################################

plt.subplot(212)


plt.grid(True)

plt.xlabel("Calendar Week")
plt.xlim(1,52)


plt.gca().set_xticks(xticks)
plt.gca().set_xticklabels(xticks)

plt.ylim(0,4000)
plt.gca().yaxis.set_major_formatter(FuncFormatter(format_func))

xd=d_2023-woche_marker_13bis19
xd_smooth = savgol_filter(
    xd,
    window_length=7,  # Fenstergröße (ungerade!)
    polyorder=3        # Polynomgrad
)

plt.plot(np.linspace(1,52,52),xd_smooth,label="Calc. Excess Deaths (smoothed)")
plt.plot(c19tote["Woche"],4*c19tote["Todesfaelle_neu"], 
         label="COVID19-Deaths (scaled x4)",
         color="black")

plt.plot(abwasser["week"],abwasser["viruslast"]/200,
         label="COVID19 Wastewater Load (÷200)",
         color=mpl.colormaps["Paired"].colors[-4])

plt.legend(loc="upper center",facecolor="white",edgecolor="white",
           bbox_to_anchor=(0.55,1))

##################################

plt.tight_layout()


plt.savefig("../figures/Fig 2d de üs 2023 baseline 13-19.tif",
            dpi=600,pil_kwargs={"compression": "tiff_lzw"})



plt.savefig("../figures/Fig 2d de üs 2023 baseline 13-19.png",
            dpi=1000)


##################################
# Merging for postproc. of correlation

corr_df=pd.merge(c19tote[["Woche","Todesfaelle_neu"]],
                 abwasser[["week","viruslast"]],
                 left_on="Woche",right_on="week")
corr_df=corr_df.drop(columns=["week"])

corr_df["xd"]=np.int64(xd)
corr_df["xd_smooth"]=np.int64(xd_smooth)

corr_df.to_csv("../../data_proc/corr/corr_2023.tsv",sep="\t")



