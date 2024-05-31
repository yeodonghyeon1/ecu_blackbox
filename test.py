import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import random
import time
# from can_network import canData
from visualization import Visual
import os 
import threading
import socket
import datetime
import pandas as pd
import re


filename = "2024y_05m_30d_16h_28m_49s"

filename = filename.replace(".mp4", "")
file_pattern = re.compile(r'(\d{4})y_(\d{2})m_(\d{2})d_(\d{2})h_(\d{2})m_(\d{2})s')
match = file_pattern.match(filename)

year, month, day, hour, minute, second = map(int, match.groups())

file_time = datetime.datetime(year, month, day, hour, minute, second)

one_minute = datetime.timedelta(minutes=1)
times_to_check = [
    (file_time - one_minute).strftime("%Yy_%mm_%dd_%Hh_%Mm"),
    file_time.strftime("%Yy_%mm_%dd_%Hh_%Mm"),
    (file_time + one_minute).strftime("%Yy_%mm_%dd_%Hh_%Mm")
]

target_files = []

# 폴더 내 파일들에 대해 반복
for filename in os.listdir("../camera/csv"):
    for time_str in times_to_check:
        if filename.startswith(time_str) and filename.endswith('.csv'):
            target_files.append(filename)
            
dataframe = []
for count, value in enumerate(target_files):
    df = pd.read_csv("../camera/csv/{}".format(value))
    df['time'] = df['time'].astype(int)
    df['time'] = df['time'].astype(float)

    
    dataframe.append(df)

full_dataframe = dataframe[0]

for count, value in enumerate(dataframe):
    if count == 0:
        continue
    full_dataframe = pd.concat([full_dataframe, value])
# print(full_dataframe['time'])
unique_id = full_dataframe["ID"].unique()
# for i in unique_id:
    # print(full_dataframe[full_dataframe['time'] == 1717054131][full_dataframe['ID'] == i])
    


frame_log = pd.read_csv("../camera/time_log/2024y_05m_30d_16h_28m_50s.csv")
frame_log['time'] = frame_log['time'].astype(int)
frame_log['time'] = frame_log['time'].astype(float)

start_time = frame_log.loc[0]['time']
i = 0
frame_for_sec = []
dict = {}
while True:
    #초당 몇 프레임인지 파악
    # print(len(frame_log[frame_log['time'] == int(start_time) + i]))
    frame_for_sec.append(len(frame_log[frame_log['time'] == int(start_time) + i]))

    dict[(start_time) + i] = frame_for_sec[i]
    i += 1
    if(len(frame_log[frame_log['time'] == int(start_time) + i]) == 0):
        break


# 컬럼에 해당하는 데이터만 뽑고싶으면 [[]]
# 어떤 조건에 해당하는 데이터를 뽑고 싶으면 df[df[] == value][df[] == value2], df[(df[] == value) & (df[] == value2)]

frame_ecu_time = {}
i = 0

# print(full_dataframe.loc[0]['time'])
# print(float(list(dict.keys())[i]))
# print(full_dataframe[full_dataframe['time'] == float(list(dict.keys())[i])][full_dataframe["ID"] == float(unique_id[0])])
# print(full_dataframe[(full_dataframe['time'] == float(list(dict.keys())[i])) & (full_dataframe["ID"] == unique_id[0])])
# print(full_dataframe[(full_dataframe['time'] == float(list(dict.keys())[1]))])
# print(full_dataframe[(full_dataframe["ID"] == float(unique_id[0]))])
# print(float(unique_id[0]))
# print(full_dataframe.loc[0]['time'] )
# # print(list(dict.keys())[2])
# print(float(list(dict.keys())[0]))
# print(full_dataframe[full_dataframe['time'] == float(list(dict.keys())[2])])
# for id in unique_id:
#         print(full_dataframe[full_dataframe['time'] == float(list(dict.keys())[i])][full_dataframe["ID"] == float(id)])
# while True:  
#     for j in range(0,20):
#         for id in unique_id:
#             frame_ecu_time[id] =full_dataframe[(full_dataframe['time'] == float(list(dict.keys())[i])) & (full_dataframe["ID"] == id)]
#             frame_ecu_time[id] = full_dataframe[(full_dataframe['time'] == float(list(dict.keys())[i])) & (full_dataframe["ID"] == id)]
#     i += 1
#     if(i > 8):
#         break

# print(frame_ecu_time[unique_id[0]])
# 1715950420
# for _, i in enumerate(dataframe):
#     print(_)

# print(full_dataframe[full_dataframe["ID"]== unique_id[0]][["eng_temp","CONF_TCU"]])
reduction_dataframe ={}
for id in unique_id:
    if id == 1087.0:
        reduction_dataframe[id] = full_dataframe[full_dataframe["ID"]== id][['ID', 'time',"CUR_GR"]]
    elif id == 809.0:
        reduction_dataframe[id] = full_dataframe[full_dataframe["ID"]== id][['ID', 'time',"eng_temp","break_on_off","TPS","PV_AC_CAN","CONF_TCU"]]
    elif id == 544.0:
        reduction_dataframe[id] = full_dataframe[full_dataframe["ID"]== id][['ID', 'time',"break_PRES"]]
    elif id == 790.0:
        reduction_dataframe[id] = full_dataframe[full_dataframe["ID"]== id][['ID', 'time',"VS","RPM"]]
    elif id == 688.0:
        reduction_dataframe[id] = full_dataframe[full_dataframe["ID"]== id][['ID', 'time',"s_angle","s_speed"]]
print(full_dataframe)
# print(reduction_dataframe)
# print(type(unique_id[0]))
# for id in unique_id:
#     print(id)
#     print(reduction_dataframe[id][(reduction_dataframe[id]['time'] == float(list(dict.keys())[3]))& (reduction_dataframe[id]["ID"] == id)])
# print(reduction_dataframe[unique_id[0]][(reduction_dataframe[unique_id[0]]['time'] == float(list(dict.keys())[i])) & (reduction_dataframe[unique_id[0]]["ID"] == unique_id)])