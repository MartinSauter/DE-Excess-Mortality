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

df=pd.read_csv("../../data_raw/pop/12411-0005_$F.csv",sep=";",
               skiprows=6,skipfooter=5,index_col=0,engine="python",
               encoding="ISO8859")

df.columns=np.linspace(2005,2024,20).astype(int)

df=df.drop(columns=np.linspace(2005,2010,6))
#df=df.apply(pd.to_numeric,errors="coerce")

# manipulate colums for better handling
# column "unter 5" becomes 4 (int)
# df.columns=np.linspace(0,100,101).astype(int)

# ag0_4=df.loc[:,0:14].sum(axis=1).to_numpy()

# ag15=df.loc[:,15:29].sum(axis=1).to_numpy()
# ag30=df.loc[:,30:39].sum(axis=1).to_numpy()
# ag40=df.loc[:,40:59].sum(axis=1).to_numpy()
# ag60=df.loc[:,60:79].sum(axis=1).to_numpy()
# ag80=df.loc[:,80:101].sum(axis=1).to_numpy()


# Neuer df erzeugen und leeren
tmp=df
tmp=tmp.drop(df.index[:],axis=0)



#selektieren; nicht inlusiv; summe heißt axis=0
df0_9=df.iloc[0:10,]
tmp.loc[0]=df0_9.sum(axis=0)



df10_19=df.iloc[10:20,]
tmp.loc[1]=df10_19.sum(axis=0)

df20_29=df.iloc[20:30,]
tmp.loc[2]=df20_29.sum(axis=0)

df30_39=df.iloc[30:40,]
tmp.loc[3]=df30_39.sum(axis=0)


df40_49=df.iloc[40:50,]
tmp.loc[4]=df40_49.sum(axis=0)


df50_59=df.iloc[50:60,]
tmp.loc[5]=df50_59.sum(axis=0)


df60_69=df.iloc[60:70,]
tmp.loc[6]=df60_69.sum(axis=0)

df70_79=df.iloc[70:80,]
tmp.loc[7]=df70_79.sum(axis=0)

df80=df.iloc[80:,]
tmp.loc[8]=df80.sum(axis=0)


index_new=["0-9","10-19","20-29","30-39","40-49","50-59","60-69","70-79","80+"]
tmp.index=index_new


tmp.to_csv("Pop_10y.tsv",sep="\t")

