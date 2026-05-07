# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 19:48:26 2024

@author: Martin Sauter
"""

import pandas as pd


df=pd.read_csv("../../data_raw/wastewater/amelag_aggregierte_kurve 2022 ff.tsv",
                delimiter="\t",parse_dates=True)
# Eliminate non.relevant
df=df.drop(columns=[ 'n', 'anteil_bev', 'loess_vorhersage',
       'loess_obere_schranke', 'loess_untere_schranke'])

# Eliminate nans

df = df.dropna(subset=["viruslast"]).reset_index(drop=True)

# Get year & weeks
df["datum"] = pd.to_datetime(df["datum"])
df["year"] = df["datum"].dt.isocalendar().year
df["week"] = df["datum"].dt.isocalendar().week
df["month"]=df["datum"].dt.month
#  Elim. date 

df=df.drop(columns=['datum'])


df=df[df["year"]==2022]


df.to_csv("c19_2022_abwasser_monate.csv")

mittelwerte = df.groupby('month')['viruslast'].mean().astype(int)


mittelwerte.to_csv("c19_2022_abwasser_monate_mw.csv")

"""
6     244098
7     328838
8     125646
9     157251
10    257961
11    157957
12    301330
Name: viruslast, dtype: int64
"""
