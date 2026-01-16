# -*- coding: utf-8 -*-
"""
Created on Fri May 20 22:18:38 2022

@author: Martin Sauter
"""



import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import linregress
from matplotlib.ticker import FuncFormatter

from cycler import cycler
import os


def format_func(value, tick_number):
    return f'{value:,.0f}'.replace(',', ' ')  
    # Umständlich Tausendertrennzeichen, ohne Dezimalstellen

#####################################################

#plt.clf()
#plt.figure(figsize=(10,7),dpi=100)
fig,ax=plt.subplots(3,2,figsize=(12,8),dpi=100)
#ax[3,1].remove()

plt.style.use("classic")
plt.rcParams["lines.linewidth"]=2
plt.rcParams['font.family'] = 'Arial'
plt.rcParams["font.size"]=14
plt.rcParams['axes.prop_cycle'] = cycler('color',
                                         plt.get_cmap('Paired').colors)


########################################################################

df=pd.read_excel("./sonderauswertung-sterbefaelle bis 2023 inkl. Daten vor 2015 update.xlsx",
                   sheet_name="D_2016-2023_Monate_AG_Ins",skiprows=8)

df=df.drop(columns=["Nr.",'Januar', 'Februar', 'März', 'April', 'Mai', 'Juni',
       'Juli', 'August', 'September', 'Oktober', 'November', 'Dezember',])


df=df.rename(columns={'unter … Jahren':"AG","Unnamed: 1":"Jahr","Unnamed: 15":"Tote" })
#df.to_csv("./sterbefaelle.csv")
ag0=df[df["AG"]=="0-15"].to_numpy()[:,2]
ag15=df[df["AG"]=="15-30"].to_numpy()[:,2]
ag30=df[df["AG"]=="30-35"].to_numpy()[:,2]+df[df["AG"]=="35-40"].to_numpy()[:,2]
#geht jetzt von 40 bis 59
ag40=df[df["AG"]=="40-45"].to_numpy()[:,2]+df[df["AG"]=="45-50"].to_numpy()[:,2]
ag50=df[df["AG"]=="50-55"].to_numpy()[:,2]+df[df["AG"]=="55-60"].to_numpy()[:,2]
ag40=ag40+ag50
del ag50    #weg damit
ag60=df[df["AG"]=="60-65"].to_numpy()[:,2]+df[df["AG"]=="65-70"].to_numpy()[:,2]
ag70=df[df["AG"]=="70-75"].to_numpy()[:,2]+df[df["AG"]=="75-80"].to_numpy()[:,2]
ag60=ag60+ag70
del ag70
ag80=df[df["AG"]=="80-85"].to_numpy()[:,2]+df[df["AG"]=="85-90"].to_numpy()[:,2]
ag90=df[df["AG"]=="90-95"].to_numpy()[:,2]+df[df["AG"]=="95 u. mehr"].to_numpy()[:,2]

ag80=ag80+ag90
del ag90

jahre=np.array([2023,2022,2021,2020,2019,2018,2017,2016,2015,2014,2013]).astype(int)

#############################################################

try:
    os.remove("ausgabe 13-19.txt")
except FileNotFoundError:
    print("nicht da")

# fig.suptitle("German Excess Mortality in 2020-2023, Comparison with 2013-2019 for Age Groups, data: destatis, Vis. Martin Sauter",
#              fontsize=18)

x=0;y=0
k=0
lbls=["0-14","15-29","30-39","40-59","60-79","80+"]

with open("ausgabe.txt","w") as file:
       print()

for ag in (ag0,ag15,ag30,ag40,ag60,ag80):
    
    x=k%2
    y=k//2
    
    
    ax[y,x].grid(True)
    ax[y,x].plot(jahre,ag,label=lbls[k],marker="x",linestyle="--",color="dodgerblue")
    
  
    lf=linregress(jahre[4:11]-2013,ag[4:11].astype(int))
    print(f"AG: {lbls[k]}, R²={(lf.stderr)} \n")
    print("----------------------------")
    
    # Fit
    z=(jahre-2013)*lf.slope+lf.intercept  
    
    sigma_min=min(ag[4:11]/z[4:11])-1
    sigma_max=max(ag[4:11]/z[4:11])-1
    
    d_lo=z*(1+sigma_min)
    d_hi=z*(1+sigma_max)
            
    locs=["upper left","upper right",
          "upper left","upper right",
          "upper left","upper left"]
         
    label=""
    if k==0:label="Trend 2013-2019"
    
    ax[y,x].plot(jahre,z,linestyle="-",color="red",label=label) 
    
    ## sigma hi/lo
    
    ax[y,x].plot(jahre,d_lo,color="lightgrey",linestyle="--")
    ax[y,x].plot(jahre,d_hi,color="lightgrey",linestyle="--")
    
    ax[y,x].fill_between(jahre,d_hi,d_lo,color="gainsboro",
                           alpha=0.6)

    ax[y,x].set_xlim(2012.5,2023.5)
    
    ax[y,x].set_xticks(np.linspace(2013,2023,11))
    #ax[y,x].set_xticks(["2015","2016","2017","2018","2019","2020","2021","2022"])
    
    
    if (y==2):
        ax[y,x].set_xticklabels(["2013","2014","2015","2016","2017","2018","2019","2020","2021","2022","2023"],rotation="vertical")
    else: ax[y,x].set_xticklabels([])
    
    
    ax[y,x].legend(loc=locs[k],fontsize=14,edgecolor="none")
    
    
    ax[y,x].yaxis.set_major_formatter(FuncFormatter(format_func))
    
    
        
    with open("ausgabe 13-19 2x 20 jahre gruppen.txt", "a") as file:
   

        print(f"Gruppe:\t{lbls[k]}\t\t",end="",file=file)
        for jahr in [3,2,1,0]:
            
            diff_abs=int(ag[jahr]-z[jahr])
            psc=int(100*(ag[jahr]/z[jahr]-1))
        
      
            print(f"Absolut:\t{int(ag[jahr]-z[jahr])}\t",end="",file=file)
            print(f"Relativ:\t{int(10000*(ag[jahr]/z[jahr]-1))/100}%\t",end="",file=file)
            
            
    
        #txt="Absolut: "+str(diff_abs)+"\nRelativ: "+str(psc)
   
        print(f"sigma_min:\t{sigma_min:.2%}\tsigma_max:\t{sigma_max:.2%}",
                  end="",file=file)
        
        print("",file=file)
    k+=1
    
######################################

plt.tight_layout()

plt.savefig("../figures/Fig 3 ÜS AG 13-19 3x20 gruppen.png")