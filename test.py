import os
import pandas as pd

dataframe = pd.read_csv("source/can_data_2024-05-17_001.csv")
print(int(dataframe.loc[0][0]))