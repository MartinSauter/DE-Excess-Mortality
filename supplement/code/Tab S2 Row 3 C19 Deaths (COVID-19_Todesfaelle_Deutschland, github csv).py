# -*- coding: utf-8 -*-
"""
Created on Fri May 20 22:18:38 2022

@author: Martin Sauter
"""



import pandas as pd



##################################
# Read from files


df=pd.read_csv("../../data_raw/covid-deaths/COVID-19-Todesfaelle_Deutschland.csv",
               index_col=None,parse_dates=["Berichtsdatum"])

# print("Tab S2. Covid 19 Deaths from RKI 'COVID-19_Todesfälle_Deutschland' csv, github")
# print("-----------------------------------------------------------")
for j in [2020,2021,2022]:
    # Filtern auf Jahr
    d=df[df["Berichtsdatum"].dt.year==j]["Todesfaelle_neu"]
    print(j,"\t",d.cumsum().values[-1])

"""
index "Todesfaelle_gesamt"
"""