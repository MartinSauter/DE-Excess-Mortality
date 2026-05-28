# -*- coding: utf-8 -*-
"""
Created on Fri May 20 22:18:38 2022

@author: Martin Sauter
"""



import pandas as pd



##################################
# Read from files


df=pd.read_excel("../../data_raw/covid-deaths/COVID-19_Todesfaelle.xlsx",
               sheet_name="COVID_Todesfälle_Monat",index_col=None)

print("Tab S2. Covid 19 Deaths from RKI 'COVID-19_Todesfälle_Monat' Excel")
print("-----------------------------------------------------------")
for j in [2020,2021,2022]:
    # Filtern auf Jahr
    
    d=df[df["SterbeMonat"].str.contains(str(j))]["Anzahl verstorbene COVID-19 Fälle"]
    print(j,"\t",d.cumsum().values[-1])


