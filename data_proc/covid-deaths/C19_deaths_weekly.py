# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 10:23:32 2022

@author: Martin Sauter
"""

import pandas as pd
# Separating Data from RKI-Excel
# into annual data
# for pandemic years


tmp=pd.read_excel("../../data_raw/covid-deaths/COVID-19_Todesfaelle.xlsx",
                  sheet_name="COVID_Todesfälle")

# Replace small number "<4" by 2
tmp=tmp.replace("<4",2)
tmp.columns=["Jahr","Woche","Tote"]

tmp["Tote"]=pd.to_numeric(tmp["Tote"])

tmp[tmp["Jahr"]==2020].to_csv("./C19 Todesfälle 2020 Wochen.txt")
tmp[tmp["Jahr"]==2021].to_csv("./C19 Todesfälle 2021 Wochen.txt")
tmp[tmp["Jahr"]==2022].to_csv("./C19 Todesfälle 2022 Wochen.txt")
