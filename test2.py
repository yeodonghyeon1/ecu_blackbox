import os
import pandas as pd

frame_log = pd.read_csv("../camera/time_log/2024y_05m_30d_16h_28m_50s.csv")

start_time = frame_log.loc[0]['time']
i = 0
frame_for_sec = []
dict = {}
while True:
    frame_for_sec.append(len(frame_log[frame_log['time'] == int(start_time) + i]))
    dict[(start_time) + i] = frame_for_sec[i]
    i += 1
    
    if(len(frame_log[frame_log['time'] == int(start_time) + i]) == 0):
        break

print(dict)
# print(list(dict.keys())[0])