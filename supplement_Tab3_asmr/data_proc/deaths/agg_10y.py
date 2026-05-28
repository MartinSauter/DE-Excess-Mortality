# -*- coding: utf-8 -*-
"""
Created on Fri May 20 22:18:38 2022

@author: Martin Sauter
"""



import pandas as pd

import numpy as np





#####################################################



df=pd.read_csv("../../../data_raw/deaths/12613-0003_de.csv",sep=";",
               skiprows=6,skipfooter=4,index_col=0,
               engine="python")

# Keep only total number (delete m + f)

df=df.iloc[25:37]

# delete "Unknown" and "Total"
df=df.drop(columns={"Alter unbekannt","Insgesamt"})


# manipulate colums for better handling
# column "unter 5" becomes 4 (int)
df.columns=np.linspace(0,100,101).astype(int)

ag0_9=df.loc[:,0:9].sum(axis=1).to_numpy(dtype=int)
ag10_19=df.loc[:,10:19].sum(axis=1).to_numpy(dtype=int)
ag20_29=df.loc[:,20:29].sum(axis=1).to_numpy(dtype=int)
ag30_39=df.loc[:,30:39].sum(axis=1).to_numpy(dtype=int)
ag40_49=df.loc[:,40:49].sum(axis=1).to_numpy(dtype=int)
ag50_59=df.loc[:,50:59].sum(axis=1).to_numpy(dtype=int)
ag60_69=df.loc[:,60:69].sum(axis=1).to_numpy(dtype=int)
ag70_79=df.loc[:,70:79].sum(axis=1).to_numpy(dtype=int)
ag80=df.loc[:,80:].sum(axis=1).to_numpy(dtype=int)

tmp=pd.DataFrame([ag0_9,ag10_19,ag20_29,ag30_39,ag40_49,
                  ag50_59,ag60_69,ag70_79,ag80])

    

tmp.columns=np.linspace(2013,2023,11).astype(int)
index_new=["0-9","10-19","20-29",
           "30-39","40-49","50-59",
           "60-69","70-79","80+"]
tmp.index=index_new


tmp.to_csv("./Deaths_10y.tsv",sep="\t")
