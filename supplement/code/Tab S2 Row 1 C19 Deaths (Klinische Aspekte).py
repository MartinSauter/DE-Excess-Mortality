# -*- coding: utf-8 -*-
"""
Created on Fri May 20 22:18:38 2022

@author: Martin Sauter
"""



import pandas as pd



##################################
# Read from files


df=pd.read_excel("../../data_raw/covid-deaths/Klinische_Aspekte.xlsx",
               sheet_name="Klinische_Aspekte",
               skiprows=2,index_col=None)

print("Tab S2. Covid 19 Deaths from RKI 'Klinische Aspekte' Excel")
print("-----------------------------------------------------------")
for j in [2020,2021,2022]:
    
    d=df[df["Meldejahr"]==j]["Anzahl Verstorben"]
    print(j,"\t",d.cumsum().values[-1])


