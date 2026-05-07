


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

#  Elim. date 

df=df.drop(columns=['datum'])


df[df["year"]==2022].to_csv("./c19_2022_abwasser.csv")

df[df["year"]==2023].reset_index().to_csv("./c19_2023_abwasser.csv")

