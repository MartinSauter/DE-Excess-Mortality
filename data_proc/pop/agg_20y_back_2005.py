# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 20:57:43 2026

@author: Martin Sauter

Aggregating pop. numbers from destatis orig.
12411-0005 (1 yr bands)

to "mixed" 20-year bands (for normalised Excess D.)

Relevant for Fig. 5 (lower)

"""
import pandas as pd
import numpy as np

df=pd.read_csv("../../data_raw/pop/12411-0005_$F.csv",sep=";",
               skiprows=6,skipfooter=5,index_col=0,engine="python",
               encoding="ISO8859")

df.columns=np.linspace(2005,2024,20).astype(int)

#df=df.drop(columns=np.linspace(2005,2010,6))

tmp=df
tmp=tmp.drop(df.index[:],axis=0)



#selektieren; nicht inlusiv; summe heißt axis=0
df0_14=df.iloc[0:15,]
tmp.loc[0]=df0_14.sum(axis=0)


df15_29=df.iloc[15:30,]
tmp.loc[1]=df15_29.sum(axis=0)

df30_39=df.iloc[30:40,]
tmp.loc[2]=df30_39.sum(axis=0)

df40_59=df.iloc[40:60,]
tmp.loc[3]=df40_59.sum(axis=0)

df60_79=df.iloc[60:80,]
tmp.loc[4]=df60_79.sum(axis=0)


df80=df.iloc[80:,]
tmp.loc[8]=df80.sum(axis=0)


index_new=["0-14","15-29","30-39","40-59","60-79","80+"]
tmp.index=index_new


tmp.to_csv("Pop_20y_back_2005.tsv",sep="\t")

