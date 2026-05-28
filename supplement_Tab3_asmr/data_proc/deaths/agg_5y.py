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

ag0_4=df.loc[:,0:4].sum(axis=1).to_numpy(dtype=int)
ag5_9=df.loc[:,5:9].sum(axis=1).to_numpy(dtype=int)

ag10_14=df.loc[:,10:14].sum(axis=1).to_numpy(dtype=int)
ag15_19=df.loc[:,15:19].sum(axis=1).to_numpy(dtype=int)

ag20_24=df.loc[:,20:24].sum(axis=1).to_numpy(dtype=int)
ag25_29=df.loc[:,25:29].sum(axis=1).to_numpy(dtype=int)


ag30_34=df.loc[:,30:34].sum(axis=1).to_numpy(dtype=int)
ag35_39=df.loc[:,35:39].sum(axis=1).to_numpy(dtype=int)

ag40_44=df.loc[:,40:44].sum(axis=1).to_numpy(dtype=int)
ag45_49=df.loc[:,45:49].sum(axis=1).to_numpy(dtype=int)

ag50_54=df.loc[:,50:55].sum(axis=1).to_numpy(dtype=int)
ag55_59=df.loc[:,55:59].sum(axis=1).to_numpy(dtype=int)

ag60_64=df.loc[:,60:64].sum(axis=1).to_numpy(dtype=int)
ag65_69=df.loc[:,65:69].sum(axis=1).to_numpy(dtype=int)

ag70_74=df.loc[:,70:74].sum(axis=1).to_numpy(dtype=int)
ag75_79=df.loc[:,75:79].sum(axis=1).to_numpy(dtype=int)

ag80_84=df.loc[:,80:84].sum(axis=1).to_numpy(dtype=int)
ag85=df.loc[:,85:].sum(axis=1).to_numpy(dtype=int)


tmp=pd.DataFrame([ag0_4,ag5_9,
                  ag10_14,ag15_19,
                  ag20_24,ag25_29,
                  ag30_34,ag35_39,
                  ag40_44,ag45_49,
                  ag50_54,ag55_59,
                  ag60_64,ag65_69,
                  ag70_74,ag75_79,
                  ag80_84,ag85])

    

tmp.columns=np.linspace(2013,2023,11).astype(int)
index_new=["0-4","5-9",
           "10-14","15-19",
           "20-24","25-29",
           "30-34","35-39",
           "40-44","45-49",
           "50-54","55-59",
           "60-64","65-69",
           "70-74","75-79",
           "80-84","85+"]
           

tmp.index=index_new


tmp.to_csv("./Deaths_5y.tsv",sep="\t")
