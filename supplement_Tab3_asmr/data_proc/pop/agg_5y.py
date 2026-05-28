# -*- coding: utf-8 -*-
"""
Created on Tue Apr 14 20:57:43 2026

@author: Martin Sauter

Aggregating pop. numbers from destatis orig.
12411-0005 (1 yr bands)

to precise 10-year bands (for normalised C19-Deaths)
equal to RKI-Excel "Klinische Aspekte"

"""
import pandas as pd
import numpy as np

df=pd.read_csv("../../../data_raw/pop/12411-0005_$F.csv",sep=";",
               skiprows=6,skipfooter=5,index_col=0,engine="python",
               encoding="ISO8859")

df.columns=np.linspace(2005,2024,20).astype(int)

df=df.drop(columns=np.linspace(2005,2012,8))



# Neuer df erzeugen und leeren
tmp=df
tmp=tmp.drop(df.index[:],axis=0)



#selektieren; nicht inklusiv; summe heißt axis=0
df0_4=df.iloc[0:5,]
tmp.loc[0]=df0_4.sum(axis=0)

df5_9=df.iloc[5:10,]
tmp.loc[1]=df5_9.sum(axis=0)

#########################################
df10_14=df.iloc[10:15,]
tmp.loc[2]=df10_14.sum(axis=0)

df15_19=df.iloc[15:19,]
tmp.loc[3]=df15_19.sum(axis=0)
#########################################
df20_24=df.iloc[20:25,]
tmp.loc[4]=df20_24.sum(axis=0)

df25_29=df.iloc[25:30,]
tmp.loc[5]=df25_29.sum(axis=0)
#########################################
df30_34=df.iloc[30:35,]
tmp.loc[6]=df30_34.sum(axis=0)

df35_39=df.iloc[35:40,]
tmp.loc[7]=df35_39.sum(axis=0)
#########################################
df40_44=df.iloc[40:45,]
tmp.loc[8]=df30_34.sum(axis=0)

df45_49=df.iloc[45:50,]
tmp.loc[9]=df35_39.sum(axis=0)
#########################################
df50_54=df.iloc[50:55,]
tmp.loc[10]=df50_54.sum(axis=0)

df55_59=df.iloc[55:60,]
tmp.loc[11]=df55_59.sum(axis=0)
#########################################
df60_64=df.iloc[60:65,]
tmp.loc[12]=df60_64.sum(axis=0)

df65_69=df.iloc[65:70,]
tmp.loc[13]=df65_69.sum(axis=0)
#########################################
df70_74=df.iloc[70:75,]
tmp.loc[14]=df70_74.sum(axis=0)

df75_79=df.iloc[75:80,]
tmp.loc[15]=df75_79.sum(axis=0)
#########################################
df80_84=df.iloc[80:85,]
tmp.loc[16]=df80_84.sum(axis=0)

df85=df.iloc[85:,]
tmp.loc[17]=df85.sum(axis=0)
#########################################

index_new=["0-4","5-9","10-14","15-19","20-24","25-29",
           "30-34","35-39","40-44","45-49","50-54","55-59",
           "60-64","65-69","70-74","75-79","80-84","85+"]
tmp.index=index_new


tmp.to_csv("./Pop_5y.tsv",sep="\t")


