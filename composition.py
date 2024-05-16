import cv2
import numpy as np
import random
import time
from can_network import canData
from visualization import Visual
import os 
import threading
import socket

def send_file(sock, filepath):#rase 1 ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
    with open(filepath, 'rb') as f:
        file_data = f.read()
    # 파일 데이터 전송
    sock.sendall(file_data)
    # 파일 전송 종료 신호 전송
    
    sock.sendall(b'--EOF--')# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

def send_video(folder_path, video_status):#rase main ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
          
    if video_status == "org":
        print("들어감")
        for filename in os.listdir(folder_path):
            if filename.endswith(".mp4"):
                client_socket.sendall("LC".encode())
                file_list = client_socket.recv(4096)  # 서버 응답 대기
                print(file_list)
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
                client_socket.sendall("LC".encode())
                file_list = client_socket.recv(4096)  # 서버 응답 대기
                print(file_list)
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

# 동영상 파일 읽기
def startVideo(video_file, handleImg):
    file = 0
    while True:
        
        cap = cv2.VideoCapture(f"../camera2/{file}.mp4") # 동영상 캡쳐 객체 생성  ---①
        capW = 640
        capH = 480
        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, w/3) # 가로
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h/3) # 세로
        # print("변환된 동영상 너비(가로) : {}, 높이(세로) : {}".format(w, h))
        visual = Visual()
        random_value = 0
        

        save_file = saveVideoWriter(cap, capW, capH,file)
        if cap.isOpened():                 # 캡쳐 객체 초기화 확인
            while True:
                ret, video = cap.read()      # 다음 프레임 읽기      --- ②
                if ret: 
                    visual.resize(capW, capH, video)
                    random_value += (random.randint(-3, 3))
                    visual.board_graphic(40, r= 128, g=128, b=128 )
                    visual.handleImageToVideo(handleImg,random_value=random_value)
                    visual.CountTime()

                    save_file.write(visual.video)
                    cv2.imshow(video_file, visual.video) # 화면에 표시  --- ③
                    cv2.waitKey(30)            # 25ms 지연(40fps로 가정)   --- ④
                else:                       # 다음 프레임 읽을 수 없슴,
                    # 합성영상 보낼꺼믄 여기
                        
                    break             # 재생 완료
             #합성 2
                 
            #여기서 웹페이로 바로 전송
        else:
            print("can't open video.")      # 캡쳐 객체 초기화 실패
            continue
        
        file += 1
    cap.release()                       # 캡쳐 자원 반납
    cv2.destroyAllWindows()


def saveVideoWriter(cap, capW, capH, file):
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    out = cv2.VideoWriter(f"video/composit_{file}.mp4", fourcc, fps, (capW, capH))
    return out


# 카메라(웹캠) 프레임 읽기
def streamVideo():
    capW = 640
    capH = 480

    # 여러가지의 코덱종류가 있지만 윈도우라면 DIVX 를 사용
    # html로 띄울려면 코덱 avc1 써야함
    # fourcc = cv2.VideoWriter_fourcc('D','I','V','X')
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    cap = cv2.VideoCapture(0)               # 0번 카메라 장치 연결 ---①, 1번은 웹캠

    file = 0
    
    while True:
        count = 0
        while True:
            if os.path.isfile(f"../camera2/{file}.mp4"):
                file += 1
            else:
                out = cv2.VideoWriter(f"../camera2/{str(file)}.mp4",fourcc,20.0,(capW, capH))
                break

        if cap.isOpened():                      # 캡쳐 객체 연결 확인
            while True:
                print(count)

                ret, img = cap.read()
                count += 1           # 다음 프레임 읽기
                if ret:
                    out.write(img)
                    cv2.imshow("img", img)
                    cv2.waitKey(1)
                    if(count == 100):
                        break                  # 아무 키라도 입력이 있으면 중지
                else:
                    print('no frame')
                    #원본 
                    break
        else:
            print("can't open camera.")
            break
        send_video(f"../camera2/","org")

        # 원본영상 2
        
        out.release()


if __name__ == "__main__":
    host = '192.168.0.80'
    port = 12345
                            
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    handleImg = cv2.imread("./source/handle.png", cv2.IMREAD_UNCHANGED)
    driveVideo = "./source/drive.mp4"
    thread = threading.Thread(target=streamVideo)
    thread.daemon = True
    thread.start()
    
    
    startVideo(driveVideo, handleImg)
    client_socket.close()# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ


