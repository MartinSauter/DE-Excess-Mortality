
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 28 11:30:36 2024

@author: Martin Sauter
"""
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from cycler import cycler
from matplotlib.ticker import FuncFormatter



def format_func(value, tick_number):
    return f'{value:,.0f}'.replace(',', ' ')  
    # Umständlich Tausendertrennzeichen, ohne Dezimalstellen


plt.figure(figsize=(10,7),dpi=100)
plt.clf()
plt.style.use("classic")
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 13

plt.rcParams['axes.prop_cycle'] = cycler('color',
                                         plt.get_cmap('Paired').colors)


#################################################################

df=pd.read_csv("../../data_raw/deaths/12613-0002_de.csv",delimiter=";",
               skiprows=5,skipfooter=4,index_col=0,engine='python')

j=df.index.to_numpy()[3:].astype(int).reshape(-1,1)

t=df["Insgesamt"].to_numpy()[3:]


# j = np.linspace(2013,2023,11).astype(int).reshape(-1,1)

# t = np.array([893825,868356,925200,910902,932272,954874,
#               939520,985572,1023687,1066341,1028206])



# Lineare Regression
model = LinearRegression()
model.fit(j[0:7], t[0:7])

# Vorhersage
t_pred = model.predict(j)

# Konfidenzniveau und Anzahl der Beobachtungen
confidence_level = 0.68
n = len(j[0:7])
p = 2  # Anzahl der Parameter (Steigung und Achsenabschnitt)

# Freiheitsgrade und kritischer t-Wert
alpha = 1 - confidence_level
t_value = stats.t.ppf(1 - alpha / 2, df=n - p)

# Standardfehler der Schätzung
s = np.sqrt(np.sum((t[0:7] - t_pred[0:7]) ** 2) / (n - p))



j_mean = np.mean(j[0:7])
S_xx = np.sum((j[0:7] - j_mean) ** 2)
margin_error = t_value * s * np.sqrt(1 + 1 / n + ((j - j_mean) ** 2 / S_xx))

lower_bound = t_pred - margin_error.flatten()
upper_bound = t_pred + margin_error.flatten()

lower_sigma = t_pred*0.97
upper_sigma = t_pred*1.0206

########################################
# Visualisierung

plt.grid(True,color="black",linewidth=0.5)
ax=plt.gca()

plt.xlim(2012,2024)
ax.set_xticks(np.linspace(2012,2023,12).astype(int))
ax.set_xticklabels(np.linspace(2012,2023,12).astype(int),
                  rotation=45)

plt.xlabel("Year")
plt.ylabel("Annual Deaths")

ax.yaxis.set_major_formatter(FuncFormatter(format_func))

plt.plot(j,t,linestyle="--",lw=0.5,marker="o",color="salmon",
         label="Observed Deaths in Germany",
         markeredgecolor="salmon")

#plt.plot(j, t_pred, color='red', label="Regressionslinie")

plt.plot(j,t_pred,marker="",linewidth=2,
             label="Linear Model 2013-2019 ",
             ls="-",color="dodgerblue",alpha=1)

plt.plot(j,lower_bound,color="dodgerblue",ls="--",lw=1,
         label="68% PI")
plt.plot(j,upper_bound,color="dodgerblue",ls="--",lw=1)




plt.fill_between(j.flatten(),lower_sigma,upper_sigma,color="gainsboro",
                 alpha=0.3)




handles, labels = plt.gca().get_legend_handles_labels()
dummy = plt.Rectangle((0,0), 1, 1, fc="gainsboro", edgecolor = 'none')
handles.append(dummy)
labels.append("Historical Min/Max")


plt.legend(handles,labels,loc="upper left",
           facecolor="white",edgecolor="white")
plt.tight_layout()

plt.show()


plt.savefig("../figures/Fig S4 de fit 13-19 inkl pi und sigma.png",dpi=600)

plt.savefig("../figures/Fig S4 de fit 13-19 inkl pi und sigma.tif",dpi=600,
            pil_kwargs={"compression": "tiff_lzw"})

