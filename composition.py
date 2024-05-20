import cv2
import numpy as np
import random
import time
# from can_network import canData
from visualization import Visual
import os 
import threading
import socket
import datetime
import pandas as pd


def can_data_csv_read(root):
    root = "source/can_data_2024-05-17_001.csv"
    dataframe = pd.read_csv("source/can_data_2024-05-17_001.csv")
    print(dataframe)
    
def send_file(sock, filepath):#rase 1 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    with open(filepath, 'rb') as f:
        file_data = f.read()
    # 파일 데이터 전송
    sock.sendall(file_data)
    # 파일 전송 종료 신호 전송
    
    sock.sendall(b'--EOF--')# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

def send_video(folder_path, video_status):#rase main ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
          
    if video_status == "ORG":
        print("들어감")
        for filename in os.listdir(folder_path):
            if filename.endswith(".mp4"):
                client_socket.sendall("LCA".encode())
                file_list = client_socket.recv(4096)  # 서버 응답 대기
                if file_list.decode().find(filename) != -1:
                    continue
                
                if file_list.decode() == "NOT_FILE":
                    filepath = os.path.join(folder_path, filename)
                    client_socket.sendall(b"ORG" + filename.encode() + b'--EOF--')  # 파일 이름 전송
                    send_file(client_socket, filepath)
                    print(f'{filename} 파일이 전송되었습니다.')
                else:
                    filepath = os.path.join(folder_path, filename)
                    client_socket.sendall(b"ORG" + filename.encode() + b'--EOF--')  # 파일 이름 전송
                    send_file(client_socket, filepath)
                    print(f'{filename} 파일이 전송되었습니다.')
    else: 
        for filename in os.listdir(folder_path):
            if filename.endswith(".mp4"):
                client_socket.sendall("LCB".encode())
                file_list = client_socket.recv(4096)  # 서버 응답 대기
                if file_list.decode().find(filename) != -1:
                    continue
                if file_list.decode() == "NOT_FILE":
                    filepath = os.path.join(folder_path, filename)
                    client_socket.sendall(b"CVV" + filename.encode() + b'--EOF--')  # 파일 이름 전송
                    send_file(client_socket, filepath)
                    print(f'{filename} 파일이 전송되었습니다.')
                else:
                    filepath = os.path.join(folder_path, filename)
                    client_socket.sendall(b"CVV" + filename.encode() + b'--EOF--')  # 파일 이름 전송
                    send_file(client_socket, filepath)
                    print(f'{filename} 파일이 전송되었습니다.')
    response = client_socket.recv(4096)  # 서버 응답 대기

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
                f = open(f"../camera/check_time_log/{file_name}.txt", 'w')
                fps = 60
                visual = Visual()
                count = 0
                random_value = 0
                save_file = saveVideoWriter(cap, capW, capH,file_name)
                if cap.isOpened(): 
                    while True:
                        ret, video = cap.read()      # 다음 프레임 읽기      --- ②
                        count += 1
                        if ret: 
                            f.write(f"{count} {int(time.time())} \n")
                            print(f"합성 중... {count}")
                            visual.resize(capW, capH, video)
                            random_value += (random.randint(-3, 3))
                            visual.board_graphic(40, r= 128, g=128, b=128 )
                            visual.handleImageToVideo(random_value=random_value, handleImg=handleImg)
                            visual.CountTime()
                            save_file.write(visual.video)
                            # cv2.imshow("video", visual.video) # 화면에 표시  --- ③
                            cv2.waitKey(1)            # 25ms 지연(40fps로 가정)   --- ④
                        else:                       # 다음 프레임 읽을 수 없슴,
                            break             # 재생 완료
                    f.close()
                    cap.release()
                    send_video(f"../camera/composit/","CVV")
                else:
                    print("can't open video_composit.")      # 캡쳐 객체 초기화 실패

    # cap.release()                       # 캡쳐 자원 반납
    # cv2.destroyAllWindows()


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

# 카메라(웹캠) 프레임 읽기
def streamVideo():
    capW = 640
    capH = 480
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    cap = cv2.VideoCapture(0)              # 0번 카메라 장치 연결 ---①, 1번은 웹캠
    duration = 30 #녹화 시간
    fps = cap.get(cv2.CAP_PROP_FPS)
    while True:
        count = 0
        now = datetime.datetime.now()
        now = now.strftime("%Yy_%mm_%dd_%Hh_%Mm_%Ss")
        f = open(f"../camera/time_log/{now}.txt", 'w')
        out = cv2.VideoWriter(f"../camera/camera/{now}.mp4",fourcc, fps,(capW, capH))
        if cap.isOpened():
            start_time = time.time()                   
            while True:
                # print(count)
                ret, img = cap.read()
                count += 1           # 다음 프레임 읽기
                if ret:
                    f.write(f"{count} {int(time.time())} \n")
                    out.write(img)
                    cv2.imshow("img", img)
                    cv2.waitKey(1)
                    if (time.time() - start_time) > duration:
                        break
                else:
                    print('no frame')
                    break
        else:
            print("can't open camera.")
            break
        f.close()
        out.release()
        send_video(f"../camera/camera/","ORG")


if __name__ == "__main__":
    host = '192.168.0.107'
    port = 12345
                            
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    thread = threading.Thread(target=streamVideo)
    thread.daemon = True
    thread.start()
    
    driveVideo = "./source/drive.mp4"
    startVideo()
    # client_socket.close()# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ


