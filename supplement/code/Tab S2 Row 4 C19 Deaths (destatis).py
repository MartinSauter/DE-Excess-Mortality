# -*- coding: utf-8 -*-
"""
Created on Fri May 20 22:18:38 2022

@author: Martin Sauter
"""



import pandas as pd



##################################
# Read from files
df=pd.read_excel("../../data_raw/covid-deaths/23211-0001_en.xlsx",
                 sheet_name="23211-0001",skiprows=4)

# df=pd.read_csv("../../data_raw/covid-deaths/23211-0001_$F.csv",
#                sep=";",skiprows=6,skipfooter=3,encoding="ISO8859-1",
#                engine="python")

#tmp=df[df.iloc[:,0]=="TDU-18" | df.iloc[:,0]=="TDU-19" ]


tmp=df[df.iloc[:,0].isin(["TDU-18","TDU-19"])]

       
print("Tab S2. Row 4, Covid 19 Deaths from Destatis csv")
print("-----------------------------------------------------------")

d2020=tmp.iloc[0,6]+tmp.iloc[0,8]+tmp.iloc[1,6]+tmp.iloc[1,8]
print("2020:\t",d2020)

d2021=tmp.iloc[0,10]+tmp.iloc[0,12]+tmp.iloc[1,10]+tmp.iloc[1,12]
print("2021:\t",d2021)

d2022=tmp.iloc[0,14]+tmp.iloc[0,16]+tmp.iloc[1,14]+tmp.iloc[1,16]
print("2022:\t",d2022)

d2023=tmp.iloc[0,18]+tmp.iloc[0,20]+tmp.iloc[1,18]+tmp.iloc[1,20]
print("2023:\t",d2023)



