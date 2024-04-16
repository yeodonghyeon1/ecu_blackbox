import cv2
import numpy as np
import random
import time
from can_network import canData

# 동영상 파일 읽기
def startVideo(video_file, handleImg):
    
    cap = cv2.VideoCapture(video_file) # 동영상 캡쳐 객체 생성  ---①
    capW = 640
    capH = 480
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, w/3) # 가로
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, h/3) # 세로
    # print("변환된 동영상 너비(가로) : {}, 높이(세로) : {}".format(w, h))
    
    random_value = 0
    save_file = saveVideoWriter(cap, capW, capH)
    if cap.isOpened():                 # 캡쳐 객체 초기화 확인
        while True:
            ret, video = cap.read()      # 다음 프레임 읽기      --- ②
            if ret:  
                random_value += (random.randint(-3, 3))
                
                video = cv2.resize(video, (capW, capH), interpolation=cv2.INTER_CUBIC)# 프레임 읽기 정상
                video = compositionImageToVideo(video, handleImg,random_value=random_value)
                save_file.write(video)
                cv2.imshow(video_file, video) # 화면에 표시  --- ③
                cv2.waitKey(30)            # 25ms 지연(40fps로 가정)   --- ④
            else:                       # 다음 프레임 읽을 수 없슴,
                break                   # 재생 완료
    else:
        print("can't open video.")      # 캡쳐 객체 초기화 실패
    cap.release()                       # 캡쳐 자원 반납
    cv2.destroyAllWindows()


def saveVideoWriter(cap, capW, capH):
    fps = cap.get(cv2.CAP_PROP_FPS)
    delay = round(1000/fps)
    fourcc = cv2.VideoWriter_fourcc(*'DIVX')
    out = cv2.VideoWriter('./source/result.avi', fourcc, fps, (capW, capH))
    return out
    
def CountTime():
    curTime = time.time()
    return curTime


def compositionImageToVideo(video, handleImg, random_value):
    
    handleImg = cv2.resize(handleImg, (120, 120))
    
    print(random_value)
    h, w = handleImg.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    
    M = cv2.getRotationMatrix2D((cX, cY), random_value, 1.0)
    handleImg = cv2.warpAffine(handleImg, M, (w, h))
    curTime = CountTime()
    cv2.putText(video, str(curTime), (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))


    _, mask = cv2.threshold(handleImg[:,:,3] , 1 ,255, cv2.THRESH_BINARY)
    # print(mask.shape)
    mask_inv = cv2.bitwise_not(mask)
    roi = video[300:300+h , 100:100+w]
    handleImg = cv2.cvtColor(handleImg, cv2.COLOR_BGRA2BGR)
    masked_img = cv2.bitwise_and(handleImg, handleImg, mask=mask)
    masked_video = cv2.bitwise_and(roi, roi, mask=mask_inv)
    
    added = masked_img + masked_video
    video[300:300+h, 100:100+w] = added
    
    return video


# 카메라(웹캠) 프레임 읽기
def streamVideo():
    cap = cv2.VideoCapture(0)               # 0번 카메라 장치 연결 ---①
    if cap.isOpened():                      # 캡쳐 객체 연결 확인
        while True:
            ret, img = cap.read()           # 다음 프레임 읽기
            if ret:
                cv2.imshow('camera', img)   # 다음 프레임 이미지 표시
                if cv2.waitKey(1) != -1:    # 1ms 동안 키 입력 대기 ---②
                    break                   # 아무 키라도 입력이 있으면 중지
            else:
                print('no frame')
                break
    else:
        print("can't open camera.")
    cap.release()                           # 자원 반납
    cv2.destroyAllWindows()



if __name__ == "__main__":
    handleImg = cv2.imread("./source/handle.png", cv2.IMREAD_UNCHANGED)
    driveVideo = "./source/drive.mp4"
    
    startVideo(driveVideo, handleImg)


