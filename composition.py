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
from pi.can import can_net

def can_data_csv_read(filename):
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
    unique_id = full_dataframe["ID"].unique()
    return full_dataframe, unique_id

def time_log_csv(frame_log):
    frame_log['time'] = frame_log['time'].astype(int)
    frame_log['time'] = frame_log['time'].astype(float)
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

    return dict
def data_reduction(ecu_dataframe, unique_id):
    reduction_dataframe ={}
    for id in unique_id:
        if id == 1087.0:
            reduction_dataframe[id] = ecu_dataframe[ecu_dataframe["ID"]== id][['ID', 'time',"CUR_GR"]]
        elif id == 809.0:
            reduction_dataframe[id] = ecu_dataframe[ecu_dataframe["ID"]== id][['ID', 'time',"eng_temp","break_on_off","TPS","PV_AC_CAN","CONF_TCU"]]
        elif id == 544.0:
            reduction_dataframe[id] = ecu_dataframe[ecu_dataframe["ID"]== id][['ID', 'time',"break_PRES"]]
        elif id == 790.0:
            reduction_dataframe[id] = ecu_dataframe[ecu_dataframe["ID"]== id][['ID', 'time',"VS","RPM"]]
        elif id == 688.0:
            reduction_dataframe[id] = ecu_dataframe[ecu_dataframe["ID"]== id][['ID', 'time',"s_angle","s_speed"]]
    return reduction_dataframe

def data_synchronization(dataframe, camera_dict, unique_id, i):
        ecu_data = {}
        for id in unique_id:
            ecu_data[id] = dataframe[id][(dataframe[id]['time'] == float(list(camera_dict.keys())[i])) & (dataframe[id]["ID"] == id)]
        camera_frame_sum = camera_dict[list(camera_dict.keys())[i]]
        frame_time_jump = int(len(ecu_data[unique_id[0]][list(ecu_data[unique_id[0]].keys())[0]]) / camera_frame_sum)
        if frame_time_jump == 0:
            frame_time_jump = 1
        return ecu_data, camera_frame_sum, frame_time_jump

def send_file(sock, filepath):#rase 1 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    with open(filepath, 'rb') as f:
        file_data = f.read()
    # 파일 데이터 전송
    sock.sendall(file_data + b'--EOF--')
    # 파일 전송 종료 신호 전송
    
    # sock.sendall(b'--EOF--')# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ


#send_video_version_2 

def send_video_version2(folder_path, video_status):#rase main ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    print(video_status)
    plus = 0.2
    if video_status == "ORG":
        file_list = ""
        server_request = 0
        client_socket.sendall("LCA".encode())
        file_list = client_socket.recv(4096)  # 서버 응답 대기
        for filename in os.listdir(folder_path):
            if filename.endswith(".mp4"):
                if file_list.decode().find("LCA") != -1:
                    if file_list.decode().find(filename) != -1:
                        continue      
                    if file_list.decode() == "LCA NOT_FILE":
                        filepath = os.path.join(folder_path, filename)
                        print("ORG", filename, "--EOF--")
                        client_socket.sendall(b"ORG" + filename.encode() + b'--EOF--')  # 파일 이름 전송
                        send_file(client_socket, filepath)
                        # print(f'{filename} 파일이 전송되었습니다.')
                    else:
                        filepath = os.path.join(folder_path, filename)
                        print("ORG", filename, "--EOF--")
                        client_socket.sendall(b"ORG" + filename.encode() + b'--EOF--')  # 파일 이름 전송
                        send_file(client_socket, filepath)
                        # print(f'{filename} 파일이 전송되었습니다.')
    elif video_status == "CVV":
        file_list = ""
        server_request = 0
        client_socket.sendall("LCA".encode())
        file_list = client_socket.recv(4096)  # 서버 응답 대기
        for filename in os.listdir(folder_path):
            if filename.endswith(".mp4"):
                if file_list.decode().find("LCA") != -1:
                    if file_list.decode().find(filename) != -1:
                        continue
                    if file_list.decode() == "LCA NOT_FILE":
                        filepath = os.path.join(folder_path, filename)
                        print("CVV", filename, "--EOF--")
                        client_socket.sendall(b"CVV" + filename.encode() + b'--EOF--')  # 파일 이름 전송
                        send_file(client_socket, filepath)
                        print(f'{filename} 파일이 전송되었습니다.')
                    else:
                        filepath = os.path.join(folder_path, filename)
                        print("CVV", filename, "--EOF--")
                        client_socket.sendall(b"CVV" + filename.encode() + b'--EOF--')  # 파일 이름 전송
                        send_file(client_socket, filepath)
                        print(f'{filename} 파일이 전송되었습니다.')


#send_video_version_1
# def send_video(folder_path, video_status):#rase main ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
#     if video_status == "ORG":
#         for filename in os.listdir(folder_path):
#             if filename.endswith(".mp4"):
#                 client_socket.sendall("LCA".encode())
#                 file_list = client_socket.recv(4096)  # 서버 응답 대기
#                 # print(file_list)
#                 if file_list.decode().find("LCA") != -1:
#                     if file_list.decode().find(filename) != -1:
#                         continue
                    
#                     if file_list.decode() == "LCA NOT_FILE":
#                         filepath = os.path.join(folder_path, filename)
#                         client_socket.sendall(b"ORG" + filename.encode() + b'--EOF--')  # 파일 이름 전송
#                         send_file(client_socket, filepath)
#                         # print(f'{filename} 파일이 전송되었습니다.')
#                     else:
#                         filepath = os.path.join(folder_path, filename)
#                         client_socket.sendall(b"ORG" + filename.encode() + b'--EOF--')  # 파일 이름 전송
#                         send_file(client_socket, filepath)
#                         # print(f'{filename} 파일이 전송되었습니다.')
#     else: 
#         for filename in os.listdir(folder_path):
#             if filename.endswith(".mp4"):
#                 client_socket.sendall("LCB".encode())
#                 file_list = client_socket.recv(4096)  # 서버 응답 대기
#                 print(file_list)
#                 if file_list.decode().find("LCB") != -1:
#                     if file_list.decode().find(filename) != -1:
#                         continue
#                     if file_list.decode() == "LCB NOT_FILE":
#                         filepath = os.path.join(folder_path, filename)
#                         client_socket.sendall(b"CVV" + filename.encode() + b'--EOF--')  # 파일 이름 전송
#                         send_file(client_socket, filepath)
#                         print(f'{filename} 파일이 전송되었습니다.')
#                     else:
#                         filepath = os.path.join(folder_path, filename)
#                         client_socket.sendall(b"CVV" + filename.encode() + b'--EOF--')  # 파일 이름 전송
#                         send_file(client_socket, filepath)
#                         print(f'{filename} 파일이 전송되었습니다.')
    # response = client_socket.recv(4096)  # 서버 응답 대기

# 실시간 스트리밍으로 합성 영상 저장 함수

def startVideo():
    handleImg = cv2.imread("./source/handle.png", cv2.IMREAD_UNCHANGED)
    while True:
        file_names = os.listdir("../camera/camera")
        composit_file_names = os.listdir("../camera/composit")
        for file_name in file_names:
            if "composit_" + file_name in composit_file_names:
                    continue
            cap = cv2.VideoCapture(f"../camera/camera/{file_name}") # 동영상 캡쳐 객체 생성  ---①
            if cap.read()[0] != False:
                capW = 640
                capH = 480
                fps = 60
                visual = Visual()
                count = 0
                random_value = 0
                i = 0
                data_jump = 0 
                save_file = saveVideoWriter(cap, capW, capH, file_name)
                if cap.isOpened():
                    try:    
                        ecu_dataframe, unique_id = can_data_csv_read(file_name)
                        camera_dict = time_log_csv(pd.read_csv(f"../camera/time_log/{file_name.replace('.mp4', '.csv')}"))
                        reduction_dataframe = data_reduction(ecu_dataframe, unique_id)
                    except:
                        continue
                    while True:
                        ret, video = cap.read()      # 다음 프레임 읽기      --- ②
                        count += 1
                        print(ret)
                        if ret:
                            ecu_data, camera_1sec_frame_sum, time_jump = data_synchronization(reduction_dataframe,camera_dict, unique_id, i)
                            print(f"합성 중... {count}")
                            # print(ecu_data)
                            if camera_1sec_frame_sum == count:
                                data_jump = 0
                                count = 0
                                i += 1
                            # print(ecu_data)
                            # # print(frame_ecu_data)
                            # if not frame_ecu_data == False:
                            #     for id in unique_id:
                            #         # print(frame_ecu_data)
                            #         print(frame_ecu_data[id].loc[data_jump + frame_time_jump])
                            visual.resize(capW, capH, video)
                            random_value += (random.randint(-3, 3))
                            visual.board_graphic(40, r= 250, g=240, b=230 )
                            visual.borad_data(ecu_data, data_jump, time_jump)
                            # print() if ecu_data[790.0].empty else visual.board_text("one", 100, 100,0,255,0)


                            # visual.board_text("eng", int((-140+int(visual.capW/4))), visual.board_value2+30, 0,255,0)
                            # visual.board_text("axcel", int((10+int(visual.capW/4))), visual.board_value2+30, 0,255,0)
                            # visual.board_text("press", int((170+int(visual.capW/4))), visual.board_value2+30, 0,255,0)
                            # visual.board_text("gear", int((340+int(visual.capW/4))), visual.board_value2+30, 0,255,0)

                            visual.handleImageToVideo(random_value=random_value, handleImg=handleImg)
                            visual.CountTime()
                            print() if ecu_data[790.0].empty else visual.graph_show(visual.video, list(ecu_data[790.0]["RPM"])[data_jump + time_jump])
                            save_file.write(visual.video)
                            visual.board_text("one", 100,100,0,255,0)
                            data_jump = data_jump + time_jump
                            print("data jump + time jump" , data_jump, time_jump)


                            # cv2.imshow("video", visual.video) # 화면에 표시  --- ③
                            cv2.waitKey(1)            # 25ms 지연(40fps로 가정)   --- ④
                        else:                       # 다음 프레임 읽을 수 없슴,
                            break             # 재생 완료
                    print("continue")
                else:
                    print("can't open video_composit.")      # 캡쳐 객체 초기화 실패
            cap.release()
            send_video_version2(f"../camera/composit/","CVV")
            # thread = threading.Thread(target=send_video_version2(f"../camera/composit/","CVV"))
            # thread.daemon = True
            # thread.start()
            break

            



#합성 영상만 확인하는 함수
def startVideo_old(video_file):
    handleImg = cv2.imread("./source/handle.png", cv2.IMREAD_UNCHANGED)
    cap = cv2.VideoCapture(video_file) # 동영상 캡쳐 객체 생성  ---①
    capW = 640
    capH = 480
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, w/3) # 가로
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h/3) # 세로
    # print("변환된 동영상 너비(가로) : {}, 높이(세로) : {}".format(w, h))
    visual = Visual()
    random_value = 0
    save_file = saveVideoWriter_old(cap, capW, capH)
    if cap.isOpened():                 # 캡쳐 객체 초기화 확인
        while True:
            ret, video = cap.read()      # 다음 프레임 읽기      --- ②
            if ret:  
                visual.resize(capW, capH, video)
                random_value += (random.randint(-3, 3))
                visual.board_graphic(40, r= 250, g=240, b=230 )
                visual.handleImageToVideo(random_value=random_value, handleImg=handleImg)
                visual.CountTime()
                visual.graph_show(visual.video, random_value)
                save_file.write(visual.video)
                cv2.imshow(video_file, visual.video) # 화면에 표시  --- ③
                cv2.waitKey(30)            # 25ms 지연(40fps로 가정)   --- ④
            else:                       # 다음 프레임 읽을 수 없슴,
                break                   # 재생 완료
    else:
        print("can't open video_composit.")      # 캡쳐 객체 초기화 실패
    cap.release()                       # 캡쳐 자원 반납
    cv2.destroyAllWindows()


def saveVideoWriter(cap, capW, capH, file):
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(f"../camera/composit/composit_{file}", fourcc, fps, (capW, capH))
    return out

def saveVideoWriter_old(cap, capW, capH):
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = round(1000/fps)
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter('./source/result.avi', fourcc, fps, (capW, capH))
    return out

import time
from unittest.mock import patch

def mock_time():
    return 1717054130


# 카메라(웹캠) 프레임 읽기
def streamVideo():
    capW = 640
    capH = 480
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    cap = cv2.VideoCapture(0)              # 0번 카메라 장치 연결 ---①, 1번은 웹캠
    duration = 10 #녹화 시간
    fps = cap.get(cv2.CAP_PROP_FPS)
    a = 0
    while True:
        count = 0
        count_list = []
        time_list = []
        temp = time.time() - 1717054130
        if a == 0:
            timestamp = 1717054130
            # timestamp를 이용해 datetime 객체를 생성합니다.
            now = datetime.datetime.fromtimestamp(timestamp)
            now = now.strftime("%Yy_%mm_%dd_%Hh_%Mm_%Ss")
            a += 1
        else:
            now = datetime.datetime.now()
            now = now.strftime("%Yy_%mm_%dd_%Hh_%Mm_%Ss")
        out = cv2.VideoWriter(f"../camera/camera/{now}.mp4",fourcc, fps,(capW, capH))
        if cap.isOpened():
            print(now)
            start_time = time.time()                   
            while True:
                # prin  t(count)
                ret, img = cap.read()
                count += 1           # 다음 프레임 읽기
                if ret:
                    print(count)
                    count_list.append(count)
                    time_list.append(int(time.time())- temp)
                    out.write(img)
                    # cv2.imshow("img", img)
                    cv2.waitKey(1)
                    if (time.time() - start_time) > duration:
                        break
                else:
                    print('no frame')
                    break
        else:
            print("can't open camera.")
            continue
        csv_file = pd.DataFrame({'count': count_list, 'time': time_list})
        csv_file.to_csv(f"../camera/time_log/{now}.csv")
        out.release()
        send_video_version2(f"../camera/camera/","ORG")
        # thread = threading.Thread(target=send_video_version2(f"../camera/camera/","ORG"))
        # thread.daemon = True
        # thread.start()

 # 그래프를 생성하는 함수
# def draw_graph(data):
#     fig = Figure(figsize=(5, 2), dpi=100)
#     canvas = FigureCanvas(fig)
#     ax = fig.add_subplot(111)
#     ax.(1, "rpm")
#     ax.plot(data, 'r-')
#     ax.set_title('Real-time Graph')
#     ax.set_xlabel('Frame')
#     ax.set_ylabel('Brightness')
#     ax.grid(True)

#     canvas.draw()
#     graph_image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8')
#     graph_image = graph_image.reshape(canvas.get_width_height()[::-1] + (3,))
    
#     return graph_image

# # 비디오 캡처 초기화
# cap = cv2.VideoCapture(0)

# # 그래프에 표시할 데이터
# data = []

# while True:
#     ret, frame = cap.read()
#     if not ret:
#         break
    
#     # 임의의 데이터 추가 (여기서는 프레임의 밝기 평균값)
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     avg_brightness = np.mean(gray)
#     data.append(avg_brightness)
    
#     # 데이터의 길이를 제한
#     if len(data) > 100:
#         data.pop(0)
    

    
#     # 화면에 표시
#     cv2.imshow('Frame with Graph', frame)
    
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()



if __name__ == "__main__":
    host = '192.168.112.1'
    port = 12345

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    thread = threading.Thread(target=streamVideo)
    thread.daemon = True
    thread.start()
    
    # thread2 = threading.Thread(target=can_net)
    # thread2.daemon = True
    # thread2.start()
    
    driveVideo = "./source/drive.mp4"
    # startVideo_old(driveVideo)
    startVideo()

    # client_socket.close()# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ


