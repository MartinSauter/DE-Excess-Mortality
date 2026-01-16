# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 13:51:19 2023

@author: Martin Sauter
"""



import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import FuncFormatter


from scipy.stats import linregress

def format_func(value, tick_number):
    return f'{value:,.0f}'.replace(',', ' ')  
    # Umständlich Tausendertrennzeichen, ohne Dezimalstellen




j=np.linspace(2010,2023,14)
t=np.asarray([858768,852328,869582,893825,868356,
               925200,910902,932272,954874,939520,
               985572,1023687,1066341,1028206])


pop=[81802257,81751602,80327900,80523746,80767463,81197537,82175684,
 	82521653	,82792351,83019213,83166711,83155031,83237124,84358845]
     

cmr=t/pop*1000

################################

fit=linregress(j[3:10],cmr[3:10])
f1=j*fit.slope+fit.intercept

psc=(cmr/f1-1)*100

smin=min(psc[3:10])
smax=max(psc[3:10])

tmin=f1*(1+smin)
tmax=f1*(1+smax)



################################
plt.figure(figsize=(10,7),dpi=100)
plt.clf()
plt.style.use("classic")
plt.rcParams['font.family'] = 'Arial'

plt.xlim(2009,2024)


plt.plot(j,cmr,linestyle="--",lw=0.5,marker="o",color="salmon",
         label="CMR in Germany, per 1000 people",
         markeredgecolor="salmon")

plt.grid(True,color="black",linewidth=0.5)

ax = plt.gca()
ax.set_xticks(np.linspace(2010,2023,14).astype(int))
ax.set_xticklabels(np.linspace(2010,2023,14).astype(int),
                   fontsize=13,rotation=45)

#ax.set_yticks(np.linspace(8e5,1.1e6,7))

# Formatter für die y-Achse setzen
#ax.yaxis.set_major_formatter(FuncFormatter(format_func))


plt.xlabel("Year",fontsize="16")
ax.spines[:].set_color('black')




plt.plot(j,f1,marker="",linewidth=2,
              label="Linear Model 2013-2019 ",
              ls="-",color="dodgerblue",alpha=1)

#############################################################

# plt.fill_between(j,tmin,tmax,color="gainsboro",
#                  alpha=0.3)
   
##############################################################
#
# P-score und Pfeile

# psc=(t/f1-1)*100

rel1,rel2=psc[4],psc[5]
r1 = patches.FancyArrowPatch((2014,cmr[4]*1.002), (2014,f1[4]*0.998), 
                              arrowstyle='<-', mutation_scale=20)
ax.add_patch(r1)

r2 = patches.FancyArrowPatch((2015,f1[5]*1.002), (2015,cmr[5]*0.998), 
                              arrowstyle='->', mutation_scale=20)
ax.add_patch(r2)

z1,z2=f"{rel1:.2f}%",f"{rel2:.2f}%"

ax.annotate(z1,(2014.5,cmr[4]*1.02),color="dodgerblue")
ax.annotate(z2,(2014,cmr[5]*1.02),color="dodgerblue")
#-----------------------------------------
psc1,psc2,psc3,psc4=psc[-4],psc[-3],psc[-2],psc[-1]

p4 = patches.FancyArrowPatch((2023,f1[-1]*1.002), (2023,cmr[-1]*0.998), 
                              arrowstyle='<->', mutation_scale=20)
ax.add_patch(p4)

p3 = patches.FancyArrowPatch((2022,f1[-2]*1.002), (2022,cmr[-2]*0.998), 
                              arrowstyle='<->', mutation_scale=20)
ax.add_patch(p3)

p2 = patches.FancyArrowPatch((2021,f1[-3]*1.002), (2021,cmr[-3]*0.998), 
                              arrowstyle='<->', mutation_scale=20)
ax.add_patch(p2)

p1 = patches.FancyArrowPatch((2020,f1[-4]*1.002), (2020,cmr[-4]*0.998), 
                              arrowstyle='<->', mutation_scale=20)
ax.add_patch(p1)

# z0="Rel. Excess" 
z4=f"{psc4:.2f}%"
z3=f"{psc3:.2f}%"
z2=f"{psc2:.2f}%"
z1=f"{psc1:.2f}%"

#ax.annotate(f"Rel. Excess: {p3:.2f}%",(2021,t[-1]*1.01))
ax.annotate(z1,(2019.5,cmr[-4]*1.02),color="dodgerblue")
ax.annotate(z2,(2020.5,cmr[-3]*1.01),color="dodgerblue")
ax.annotate(z3,(2021.5,cmr[-2]*1.005),color="dodgerblue")
ax.annotate(z4,(2022.5,cmr[-1]*1.01),color="dodgerblue")




#################################################################

plt.legend(loc="upper left",facecolor="white",
            edgecolor="white")

plt.tight_layout()




plt.savefig("../figures/Fig S5 de fit cmr 13-19 inkl psc.png")