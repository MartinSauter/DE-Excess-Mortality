# -*- coding: utf-8 -*-
"""
Created on Fri Dec 16 13:46:20 2022
Retrievung monthly deaths for groups 15-29 in 2022
These data are only available from "Sonderauswertung"

2 sources, the first 2021-2024
the older ones from "SBxxxxx"

@author: Martin
"""




import pandas as pd




def format_func(value, tick_number):
    return f'{value:,.0f}'.replace(',', ' ')  
    # Umständlich Tausendertrennzeichen, ohne Dezimalstellen



##############################################################

df1=pd.read_excel("../../data_raw/deaths/statistischer-bericht-sterbefaelle-tage-wochen-monate-aktuell-5126109.xlsx",
                 sheet_name="12613-04",skiprows=3,skipfooter=3)
df1=df1.rename(columns={df1.columns[0]:"Jahr",df1.columns[1]:"AG"})

df1["Jahr"]=df1["Jahr"].astype(int)


df1=df1[df1["Jahr"]<2024]
df1=df1[df1.iloc[:,1]=="15-29"]

df1=df1.drop(columns=["Insgesamt"]).reset_index(drop=True)
###############################################################

"""
  Jahr     AG  Januar  Februar März  ... August September Oktober November Dezember
0  2023  15-29     323      310  327  ...    336       321     313      333      350
1  2022  15-29     343      292  355  ...    348       371     346      331      391
2  2021  15-29     290      278  296  ...    313       344     358      321      341
"""
 
###############################################################
df2=pd.read_excel("../../data_raw/deaths/5126108209005_SB.xlsx",
                 sheet_name="12613-05",skiprows=3,skipfooter=3)
df2=df2.rename(columns={df2.columns[0]:"Jahr",df2.columns[1]:"AG"})

df2["Jahr"]=df2["Jahr"].astype(int)


df2=df2[df2["Jahr"]>2012]
df2=df2[df2.iloc[:,1]=="15-29"]

df2=df2.drop(columns=["Insgesamt"]).reset_index(drop=True)

"""
   Jahr     AG  Januar  Februar  ...  September  Oktober  November  Dezember
0  2020  15-29     329      330  ...        305      320       309       311
1  2019  15-29     333      327  ...        303      319       327       318
2  2018  15-29     386      329  ...        329      336       323       324
3  2017  15-29     397      346  ...        351      320       325       353
4  2016  15-29     359      339  ...        380      384       370       348
5  2015  15-29     353      361  ...        353      395       373       347
6  2014  15-29     348      312  ...        361      338       355       367
7  2013  15-29     361      380  ...        368      399       312       337

"""

df3=pd.concat([df1,df2]).reset_index(drop=True)

df3.to_csv("./Deaths monthly 15-29.csv")
##############################################################

