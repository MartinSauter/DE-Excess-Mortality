# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 19:48:26 2024

@author: Martin Sauter
"""

import pandas as pd

c19=pd.read_csv("../../data_raw/covid-deaths/COVID-19-Todesfaelle_Deutschland.csv",
                parse_dates=["Berichtsdatum"])

c19["Jahr"]=c19["Berichtsdatum"].dt.isocalendar().year
c19["Monat"]=c19["Berichtsdatum"].dt.month
c19["Woche"]=c19["Berichtsdatum"].dt.isocalendar().week



c19_2023=c19[c19["Jahr"]==2023]


c19_2023=c19_2023[["Todesfaelle_neu","Woche"]]

#c19_2023.set_index('Berichtsdatum', inplace=True)



c19_2023_w=c19_2023.groupby("Woche").sum()
c19_2023_w.to_csv("c19_2023_tote_wochen.csv")



