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
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

from cycler import cycler



def format_func(value, tick_number):
    return f'{value:,.0f}'.replace(',', ' ')  
    # Umständlich Tausendertrennzeichen, ohne Dezimalstellen

#####################################################




plt.style.use("classic")
plt.rcParams["lines.linewidth"]=2
plt.rcParams['font.family'] = 'Arial'
plt.rcParams["font.size"]=13
plt.rcParams['axes.prop_cycle'] = cycler('color',
                                         plt.get_cmap('Paired').colors)


########################################################################


df=pd.read_csv("../../data_raw/deaths/12613-0003_de.csv",sep=";",
               skiprows=6,skipfooter=4,index_col=0,engine="python")

# Keep only total number (delete m + f)

df=df.iloc[25:37]

# delete "Unknown" and "Total"
df=df.drop(columns={"Alter unbekannt","Insgesamt"})


# manipulate colums for better handling
# column "unter 5" becomes 4 (int)
df.columns=np.linspace(0,100,101).astype(int)

ag0=df.loc[:,0:14].sum(axis=1).to_numpy()
ag15=df.loc[:,15:29].sum(axis=1).to_numpy()
ag30=df.loc[:,30:39].sum(axis=1).to_numpy()
ag40=df.loc[:,40:59].sum(axis=1).to_numpy()
ag60=df.loc[:,60:79].sum(axis=1).to_numpy()
ag80=df.loc[:,80:101].sum(axis=1).to_numpy()




jahre=np.linspace(2013,2023,11).astype(int)

#############################################################

fig,ax=plt.subplots(3,2,figsize=(12,8))
x=0;y=0
k=0
lbls=["0-14","15-29","30-39","40-59","60-79","80+"]

with open("ausgabe.txt","w") as file:
       print()

for ag in (ag0,ag15,ag30,ag40,ag60,ag80):
    
    x=k%2
    y=k//2
    
    if x==0:ax[y,x].set_ylabel("Annual Deaths in Age Group")
    
    ax[y,x].grid(True)
    ax[y,x].plot(jahre,ag,marker="x",linestyle="--",color="dodgerblue")
    
  
    lf=linregress(jahre[0:7]-2013,ag[0:7].astype(int))
    print(f"AG: {lbls[k]}, R²={(lf.stderr)} \n")
    print("----------------------------")
    
    # Fit
    trend=(jahre-2013)*lf.slope+lf.intercept  
    
    sigma_min=min(ag[0:7]/trend[0:7])-1
    sigma_max=max(ag[0:7]/trend[0:7])-1
    
    d_lo=trend*(1+sigma_min)
    d_hi=trend*(1+sigma_max)
            
    locs=["upper left","upper right",
          "upper left","upper right",
          "upper left","upper left"]
  
        
    
    ax[y,x].plot(jahre,trend,linestyle="-",color="red",label="") 
    
    ## min/max areas
    
    ax[y,x].plot(jahre,d_lo,color="lightgrey",linestyle="--")
    ax[y,x].plot(jahre,d_hi,color="lightgrey",linestyle="--")
    
    ax[y,x].fill_between(jahre,d_hi,d_lo,color="gainsboro",
                           alpha=0.6)
    
    #handles, labels = ax[y,x].get_legend_handles_labels()
    
    blue_line = Line2D([0], [0], color="dodgerblue", linewidth=2,ls="--")
    red_line = Line2D([0], [0], color="red", linewidth=2)
    rect = Rectangle((0,0), 1, 1, fc="gainsboro", edgecolor = 'none')
    
    if x==0 and y==0:
        
        handles, labels = ax[y,x].get_legend_handles_labels()
        
        labels.append(lbls[k])
        handles.append(blue_line)
        
        labels.append("Trend 2013-19")
        handles.append(red_line)
    
        labels.append("2013-19 Min/Max")
        handles.append(rect)
    
    else: 
        handles, labels = ax[y,x].get_legend_handles_labels()
        
        labels.append(lbls[k])
        handles.append(blue_line)
 
    
    ax[y,x].legend(handles, labels,loc=locs[k],fontsize=12,edgecolor="none")
    
    ax[y,x].set_xlim(2012.5,2023.5)
    
    ax[y,x].set_xticks(np.linspace(2013,2023,11).astype(int))
    
    
    if (y==2):
        ax[y,x].set_xticklabels(np.linspace(2013,2023,11).astype(int),rotation="vertical")
       
    else: ax[y,x].set_xticklabels([])
    
   
    
    ax[y,x].yaxis.set_major_formatter(FuncFormatter(format_func))
    
    if k==0:
        with open("Tab.2 Data CDC Trend 13-19 20y age groups.txt", "a") as file:  
            print("\t"*4+"2020"+"\t"*6+"2021"+"\t"*6+"2022"+"\t"*6+"2023",
                  file=file)
            print("\t"*4+"abs."+"\t"*3+"rel."+
                  "\t"*2+"abs."+"\t"*3+"rel."+
                  "\t"*2+"abs."+"\t"*3+"rel."+
                  "\t"*2+"abs."+"\t"*3+"rel.",
                  file=file)
    with open("Tab.2 Data CDC Trend 13-19 20y age groups.txt", "a") as file:
   

        print(f"{lbls[k]:<6}\t",end="",file=file)
        for jahr in [-4,-3,-2,-1]:
            
            diff_abs=int(ag[jahr]-trend[jahr])
            psc=int(100*(ag[jahr]/trend[jahr]-1))
        
      
            print(f"\t{int(ag[jahr])-int(trend[jahr]):>8}\t",end="",file=file)
            print(f"\t{int(10000*(ag[jahr]/trend[jahr]-1))/100:>6}%\t",end="",file=file)
            
            
    
   
        print(f"\t{sigma_min:.2%}\t\t{sigma_max:.2%}",
                  end="",file=file)
        
        print("",file=file)
    k+=1
    
######################################

plt.tight_layout()

plt.savefig("../figures/Fig 3 ÜS AG 13-19 3x20 gruppen.png",dpi=1000)
