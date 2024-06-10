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
import atexit
import time
from unittest.mock import patch
import queue


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
    print(target_files)
    for count, value in enumerate(target_files):
        try:
            df = pd.read_csv("../camera/csv/{}".format(value))
            df['time'] = df['time'].astype(int)
            df['time'] = df['time'].astype(float)
            dataframe.append(df)
        except:
            pass

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
       try:
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
       except:
            pass
    return reduction_dataframe

def data_synchronization(dataframe, camera_dict, unique_id, i):
        ecu_data = {}
        for id in unique_id:
            ecu_data[id] = dataframe[id][(dataframe[id]['time'] == float(list(camera_dict.keys())[i])) & (dataframe[id]["ID"] == id)]
        camera_frame_sum = camera_dict[list(camera_dict.keys())[i]]
        # low = int(len(ecu_data[unique_id[0]][list(ecu_data[unique_id[0]].keys())[0]]))
        # for i in range(0, 4):
        #     if low > int(len(ecu_data[unique_id[i]][list(ecu_data[unique_id[i]].keys())[0]])):
        #         low = int(len(ecu_data[unique_id[i]][list(ecu_data[unique_id[i]].keys())[0]]))
        low = int(len(ecu_data[unique_id[4]][list(ecu_data[unique_id[4]].keys())[0]]))
        frame_time_jump = int(low / camera_frame_sum)
        # frame_time_jump += 1

        if frame_time_jump == 0:
            frame_time_jump = 1
        #frame_time_jump = 1
        return ecu_data, camera_frame_sum, frame_time_jump

def send_file(sock, filepath):#rase 1 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    try:
        with open(filepath, 'rb') as f:
            file_data = f.read()
            # 파일 데이터 전송
            sock.sendall(file_data)
            sock.sendall(b'--EOF--') 
            # 파일 전송 종료 신호 전송
    except:
        pass
    # sock.sendall(b'--EOF--')# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ


#send_video_version_2 

def send_video_version2(folder_path, video_status):#rase main ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    send_count = 1
    if video_status == "ORG":
        file_list = ""
        server_request = 0
        client_socket.sendall("LCA".encode())
        file_list = client_socket.recv(4096)  # 서버 응답 대기
        file_list_check = file_list.decode().split("-")
        
        while True:
            if int(file_list_check[1]) <= len(file_list.decode()):
                break
            file_list += client_socket.recv(4096)
        for filename in os.listdir(folder_path):
            if filename.endswith(".mp4"):
                if file_list.decode().find("LCA") != -1:
                    if file_list.decode().find(filename) != -1:
                        continue      
                    if "NOT_FILE" in file_list.decode():
                        filepath = os.path.join(folder_path, filename)
                        print("ORG", filename, "--EOF--")
                        client_socket.sendall(b"ORG" + filename.encode() + b'--EOF--')  # 파일 이름 전송
                        send_file(client_socket, filepath)
                        response = client_socket.recv(4096)
                        if "ERROR" in response.decode():
                            break
                        print(f'{filename} 파일이 전송되었습니다.')
                        #remove(response, filepath, "ORG")
                        #send_count -= 1
                        #if send_count == 0:
                        #    break
                    else:
                        filepath = os.path.join(folder_path, filename)
                        print("ORG", filename, "--EOF--")
                        client_socket.sendall(b"ORG" + filename.encode() + b'--EOF--')  # 파일 이름 전송
                        send_file(client_socket, filepath)
                        response = client_socket.recv(4096)
                        if "ERROR" in response.decode():
                            break
                        print(f'{filename} 파일이 전송되었습니다.')
                        #remove(response, filepath, "ORG")
                        #send_count -= 1
                        #if send_count == 0:
                        #    break
    elif video_status == "CVV":
        file_list = ""
        server_request = 0
        client_socket.sendall("LCA".encode())
        file_list = client_socket.recv(4096)  # 서버 응답 대기
        file_list_check = file_list.decode().split("-")
        
        while True:
            if int(file_list_check[1]) <= len(file_list.decode()):
                break
            file_list += client_socket.recv(4096)
                
        for filename in os.listdir(folder_path):
            if filename.endswith(".mp4"):
                if file_list.decode().find("LCA") != -1:
                    if file_list.decode().find(filename) != -1:
                        continue
                    if "NOT_FILE" in file_list.decode():
                        filepath = os.path.join(folder_path, filename)
                        print("CVV", filename, "--EOF--")
                        client_socket.sendall(b"CVV" + filename.encode() + b'--EOF--')  # 파일 이름 전송
                        send_file(client_socket, filepath)
                        response = client_socket.recv(4096)
                        print(response)
                        if "ERROR" in response.decode():
                            break
                        print(f'{filename} 파일이 전송되었습니다.')
                        #remove(response, filepath, "CVV")
                        #send_count -= 1
                        #if send_count == 0:
                        #    break
                    else:
                        filepath = os.path.join(folder_path, filename)
                        print("CVV", filename, "--EOF--")
                        client_socket.sendall(b"CVV" + filename.encode() + b'--EOF--')  # 파일 이름 전송
                        send_file(client_socket, filepath)
                        response = client_socket.recv(4096)
                        print(response)
                        if "ERROR" in response.decode():
                            break
                        print(f'{filename} 파일이 전송되었습니다.')
                        #remove(response, filepath, "CVV")
                        #send_count -= 1
                        #if send_count == 0:
                        #    break


def remove(response, filepath, status):
    response = response.decode()
    if response != "ok":
       if "ORG" in status:
            os.remove(filepath)
       elif "CVV" in status:
            os.remove(filepath)
            
#send_video_version_1
def send_video(folder_path, video_status): #rase main ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
     if video_status == "ORG":
         for filename in os.listdir(folder_path):
             if filename.endswith(".mp4"):
                 client_socket.sendall("LCA".encode())
                 file_list = client_socket.recv(4096)  # 서버 응답 대기
                 # print(file_list)
                 if file_list.decode().find("LCA") != -1:
                     if file_list.decode().find(filename) != -1:
                         continue
                
                     if file_list.decode() == "LCA NOT_FILE":
                         filepath = os.path.join(folder_path, filename)
                         client_socket.sendall(b"ORG" + filename.encode() + b'--EOF--')  # 파일 이름 전송
                         send_file(client_socket, filepath)
                         response = client_socket.recv(4096)
                         # print(f'{filename} 파일이 전송되었습니다.')
                     else:
                         filepath = os.path.join(folder_path, filename)
                         client_socket.sendall(b"ORG" + filename.encode() + b'--EOF--')  # 파일 이름 전송
                         send_file(client_socket, filepath)
                         response = client_socket.recv(4096)
                         # print(f'{filename} 파일이 전송되었습니다.')
     else: 
         for filename in os.listdir(folder_path):
             if filename.endswith(".mp4"):
                 client_socket.sendall("LCA".encode())
                 file_list = client_socket.recv(4096)  # 서버 응답 대기
                 print(file_list)
                 if file_list.decode().find("LCA") != -1:
                     if file_list.decode().find(filename) != -1:
                         continue
                     if file_list.decode() == "LCA NOT_FILE":
                         filepath = os.path.join(folder_path, filename)
                         client_socket.sendall(b"CVV" + filename.encode() + b'--EOF--')  # 파일 이름 전송
                         send_file(client_socket, filepath)
                         response = client_socket.recv(4096)  # 서버 응답 대기
                         print(f'{filename} 파일이 전송되었습니다.')
                     else:
                         filepath = os.path.join(folder_path, filename)
                         client_socket.sendall(b"CVV" + filename.encode() + b'--EOF--')  # 파일 이름 전송
                         send_file(client_socket, filepath)
                         response = client_socket.recv(4096)  # 서버 응답 대기
                         print(f'{filename} 파일이 전송되었습니다.')
        

# 실시간 스트리밍으로 합성 영상 저장 함수

def startVideo():
    global send_variable
    handleImg = cv2.imread("./source/handle.png", cv2.IMREAD_UNCHANGED)
    # test = 0

    while True:
        file_names = os.listdir("../camera/camera")
        composit_file_names = os.listdir("../camera/composit")
        for file_name in file_names:
            if "composit_" + file_name in composit_file_names:
                    continue
            
            # if test == 0:
            #     cap = cv2.VideoCapture("./source/2024y_05m_30d_16h_28m_50s.mp4") # 동영상 캡쳐 객체 생성  ---①
            #     test += 1
            # else:
            cap = cv2.VideoCapture(f"../camera/camera/{file_name}") # 동영상 캡쳐 객체 생성  ---①
                
            print(file_name, "startVideo")
            if cap.read()[0] != False:
                print(file_name, "readVideo")
                capW = 640
                capH = 480
                window_width = 640
                window_height = 600
                right_margin = window_width - capW
                bottom_margin = window_height - capH    
                visual = Visual()
                count = 0
                random_value = 0
                i = 0
                data_jump = 5 
                index_error = 0
                before_data = {}
                save_file = saveVideoWriter(cap, window_width, window_height, file_name)
                if cap.isOpened():

                    ecu_dataframe, unique_id = can_data_csv_read(file_name)
                    camera_dict = time_log_csv(pd.read_csv(f"../camera/time_log/{file_name.replace('.mp4', '.csv')}"))
                    reduction_dataframe = data_reduction(ecu_dataframe, unique_id)

                    while True:
                        ret, video = cap.read()      # 다음 프레임 읽기      --- ②
                        count += 1
                        if ret:
                            visual.resize(capW, capH, video)
                            visual.video = cv2.copyMakeBorder(visual.video, 0, bottom_margin, 0, right_margin, cv2.BORDER_CONSTANT, value=[255,255, 255])
                            # visual.CountTime()
                            

                            try:
                                ecu_data, camera_1sec_frame_sum, time_jump = data_synchronization(reduction_dataframe,camera_dict, unique_id, i)
                                
                                # print(f"합성 중... {count}")
                                #print(ecu_data)

                                if camera_1sec_frame_sum == count:
                                    data_jump = 0
                                    count = 0
                                    i += 1

                                random_value += (random.randint(-3, 3))
                                visual.board_graphic(40, r= 250, g=240, b=230 )
                                visual.borad_data(ecu_data, data_jump, time_jump, before_data)
                                try:
                                    if data_jump == 0:
                                        print("헨들 에러") if ecu_data[688.0].empty else visual.handleImageToVideo(random_value=before_data["s_angle"] , handleImg=handleImg)
                                    else:
                                        print("헨들 에러") if ecu_data[688.0].empty else visual.handleImageToVideo(random_value=int(list(ecu_data[688.0]["s_angle"])[data_jump + time_jump]), handleImg=handleImg)
                                        before_data["s_angle"] = int(list(ecu_data[688.0]["s_angle"])[data_jump + time_jump])
                                except:
                                    try:
                                        print("헨들 에러") if ecu_data[688.0].empty else visual.handleImageToVideo(random_value=before_data["s_angle"] , handleImg=handleImg)
                                    except:
                                        pass

                                try:
                                    if data_jump == 0:
                                        print() if ecu_data[809.0].empty else visual.graph_show(visual.video, before_data["PV_AC_CAN"], before_data["break_PRES"])
                                    else:    
                                        print() if ecu_data[809.0].empty else visual.graph_show(visual.video, list(ecu_data[809.0]["PV_AC_CAN"])[data_jump + time_jump], list(ecu_data[544.0]["break_PRES"])[data_jump + time_jump])
                                        before_data["PV_AC_CAN"] = list(ecu_data[809.0]["PV_AC_CAN"])[data_jump + time_jump]
                                        before_data["break_PRES"] = list(ecu_data[544.0]["break_PRES"])[data_jump + time_jump]
                                except:
                                    try:
                                        print() if ecu_data[809.0].empty else visual.graph_show(visual.video, before_data["PV_AC_CAN"], before_data["break_PRES"])
                                    except:
                                        pass

                                save_file.write(visual.video)
                                print("time jump" , time_jump)
                                cv2.imshow("video", visual.video) # 화면에 표시  --- ③
                                cv2.waitKey(1)            # 25ms 지연(40fps로 가정)   --- ④
                                data_jump = data_jump + time_jump

                            except:
                                print("index error")
                                save_file.write(visual.video)
                                # cv2.imshow("video",data_jump = data_jump + time_jump visual.video) # 화면에 표시  --- ③
                        else:                       # 다음 프레임 읽을 수 없슴,
                            cap.release()
                            save_file.release()
                            send_queue.put(2)
                            break             # 재생 완료
                    print("continue")
                else:
                    print("can't open video_composit.")      # 캡쳐 객체 초기화 실패

            # thread = threading.Thread(target=send_video_version2(f"../camera/composit/","CVV"))
            # thread.daemon = True
            # thread.start()

            



#합성 영상만 확인하는 함수
def startVideo_old(video_file):
    handleImg = cv2.imread("./source/handle.png", cv2.IMREAD_UNCHANGED)
    cap = cv2.VideoCapture(video_file) # 동영상 캡쳐 객체 생성  ---①
    capW = 640
    capH = 480
    window_width = 640
    window_height = 600


    right_margin = window_width - capW
    bottom_margin = window_height - capH
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
                visual.video = cv2.copyMakeBorder(visual.video, 0, bottom_margin, 0, right_margin, cv2.BORDER_CONSTANT, value=[255,255, 255])

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
    fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
    # fourcc = cv2.VideoWriter_fourcc()
    out = cv2.VideoWriter(f"../camera/composit/composit_{file}", fourcc, fps, (capW, capH))
    return out

def saveVideoWriter_old(cap, capW, capH):
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = round(1000/fps)
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter('./source/result.avi', fourcc, fps, (capW, capH))
    return out


def mock_time():
    return 1717054130


# 카메라(웹캠) 프레임 읽기
def streamVideo():
    global send_variable
    capW = 640
    capH = 480

    window_width = 640
    window_height = 600


    right_margin = window_width - capW
    bottom_margin = window_height - capH


    fourcc = cv2.VideoWriter_fourcc('D', 'I', 'V', 'X')
    # fourcc = cv2.VideoWriter_fourcc(*'avc1')
    cap = cv2.VideoCapture(0)              # 0번 카메라 장치 연결 ---①, 1번은 웹캠
    duration = 30 #녹화 시간
    fps = 12.3
    print(fps)
    a = 0
    while True:
        count = 0
        count_list = []
        time_list = []
        # temp = time.time() - 1717054130
        # if a == 0:
        #     timestamp = 1717054130
        #     # timestamp를 이용해 datetime 객체를 생성합니다.
        #     now = datetime.datetime.fromtimestamp(timestamp)
        #     now = now.strftime("%Yy_%mm_%dd_%Hh_%Mm_%Ss")
        #     a += 1
        # else:
        now = datetime.datetime.now()
        now = now.strftime("%Yy_%mm_%dd_%Hh_%Mm_%Ss")
        visual = Visual()
        out = cv2.VideoWriter(f"../camera/camera/{now}.mp4",fourcc, fps,(capW, capH))
        if cap.isOpened():
            print(now)
            start_time = time.time()                   
            while True:
                ret, img = cap.read()
                count += 1           # 다음 프레임 읽기
                if ret:
                    print(count)
                    visual.resize(capW, capH, img)
                    # visual.video = cv2.copyMakeBorder(visual.video, 0, bottom_margin, 0, right_margin, cv2.BORDER_CONSTANT, value=[255,255, 255])
                    count_list.append(count)
                    # time_list.append(int(time.time())- temp)
                    time_list.append(int(time.time()))
                    visual.CountTime()

                    out.write(visual.video)
                    #cv2.imshow("img", visual.video)
                    # time.sleep(0.001)
                    if cv2.waitKey(1) & 0xFF == ord('x'):
                        break 
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
        #send_video_version2(f"../camera/camera/","ORG")
        #thread = threading.Thread(target=send_video_version2(f"../camera/camera/","ORG"))
        #thread.daemon = True
        #thread.start()
        send_queue.put(1)

def send_function():
    global send_queue
    while True:
        try:
            print("send_queue_size:", send_queue.qsize())
            if send_queue.empty() == False:
                send_key = send_queue.get()
                if send_key == 1:
                    send_video_version2(f"../camera/camera/","ORG")
                elif send_key == 2:
                    send_video_version2(f"../camera/composit/","CVV")
            else:
                time.sleep(0.5)
        except:
            pass

def handle_exit(client_socket):
    client_socket.sendall(b"END")


if __name__ == "__main__":
    host = '192.168.194.187'
    port = 12345
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    send_queue = queue.Queue()
    atexit.register(handle_exit, client_socket)

   
   
    
    # driveVideo = "./source/drive.mp4"
    # startVideo_old(driveVideo)    
    
    thread3 = threading.Thread(target=startVideo)
    thread3.daemon = True
    thread3.start()
    
    thread4 = threading.Thread(target=send_function)
    thread4.daemon = True
    thread4.start()
    
    thread4 = threading.Thread(target=can_net)
    thread4.daemon = True
    thread4.start()
    
    while True:
       time.sleep(3)
    # client_socket.close()# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ


