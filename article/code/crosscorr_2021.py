# -*- coding: utf-8 -*-
"""
Created on Tue May 19 11:02:54 2026

@author: Martin Sauter
"""



import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

from scipy.signal import detrend






# Datei laden
df = pd.read_csv("../../data_proc/corr/corr_2021.tsv", sep="\t")



# Daten extrahieren
x = df["xd_smooth"].values[0:26]
y = df["Tote"].values[0:26]

x=detrend(x)
y=detrend(y)

max_lag = 10

lags = np.arange(-max_lag, max_lag + 1)

corrs = []

for lag in lags:

    if lag < 0:
        r = np.corrcoef(x[:lag], y[-lag:])[0,1]

    elif lag > 0:
        r = np.corrcoef(x[lag:], y[:-lag])[0,1]

    else:
        r = np.corrcoef(x, y)[0,1]

    corrs.append(r)

# Plot
plt.figure(figsize=(10,5))

plt.plot(lags, corrs, marker="o")

plt.axhline(0, linestyle="--")

plt.xlabel("Lag (Wochen)")
plt.ylabel("Pearson Cross-Correlation")

plt.show()

best_lag = lags[np.argmax(corrs)]

print("Best Lag:", best_lag)
print("Max Corr:", max(corrs))

"""
Best Lag: 0
Max Corr: 0.9629320259326142
"""