import cv2
import time
import datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure


class Visual:
    def __init__(self):
        pass

    def resize(self, capW, capH, video):
        video = cv2.resize(video, (capW, capH), interpolation=cv2.INTER_CUBIC)# 프레임 읽기 정상
        self.video = video
        self.capW = capW
        self.capH = capH

    def board_graphic(self, board_value, r,g,b):
        self.board_value = board_value
        board_value = self.capH - board_value
        cv2.rectangle(self.video, (0, board_value), (self.capW, self.capH), (r, g, b), -1)
        cv2.rectangle(self.video, (0, board_value+1), (self.capW, self.capH-1), (r+240, g+255, b+240), -1)
        cv2.rectangle(self.video, (0, board_value+2), (self.capW, self.capH-2), (r+240, g+255, b+240), -1)
        cv2.rectangle(self.video, (0, board_value+3), (self.capW, self.capH-3), (r+240, g+255, b+240), -1)
        cv2.rectangle(self.video, (0, board_value+4), (self.capW, self.capH-4), (r+255, g+228, b+225), -1)
        cv2.rectangle(self.video, (0, board_value+5), (self.capW, self.capH-5), (r+122, g+122, b+122), -1)
        cv2.rectangle(self.video, (10, board_value + 5), (int(self.capW/4), self.capH-5), (r, g, b), -1)
        

        cv2.rectangle(self.video, (10+int(self.capW/4), board_value + 5), (int(self.capW/4)*2, self.capH-5), (r, g, b), -1)
        cv2.rectangle(self.video, (10+int(self.capW/4)*2, board_value + 5), (int(self.capW/4) *3, self.capH-5), (240, 255, 240), -1)
        cv2.rectangle(self.video, (10+int(self.capW/4)*3, board_value + 5), (int(self.capW/4)*4, self.capH-5), (240, 255, 240), -1)
        # cv2.rectangle(self.video, (10+int(self.capW/6)*4, board_value + 5), (int(self.capW/6)*5, self.capH-5), (r, g, b), -1)
        # cv2.rectangle(self.video, (10+int(self.capW/6)*5, board_value + 5), (int(self.capW/6)*6, self.capH-5), (r, g, b), -1)
        self.board_text("eng", int((-140+int(self.capW/4))), board_value+30, 0,255,0)
        self.board_text("axcel", int((10+int(self.capW/4))), board_value+30, 0,255,0)
        self.board_text("press", int((170+int(self.capW/4))), board_value+30, 0,255,0)
        self.board_text("gear", int((340+int(self.capW/4))), board_value+30, 0,255,0)
    def handleImageToVideo(self, random_value, handleImg):
        handleImg = cv2.resize(handleImg, (120, 120))
        
        
        h, w = handleImg.shape[:2]
        (cX, cY) = (w // 2, h // 2)
        
        M = cv2.getRotationMatrix2D((cX, cY), random_value, 1.0)
        handleImg = cv2.warpAffine(handleImg, M, (w, h))


        _, mask = cv2.threshold(handleImg[:,:,3] , 1 ,255, cv2.THRESH_BINARY)
        # print(mask.shape)
        mask_inv = cv2.bitwise_not(mask)
        roi = self.video[300:300+h , 100:100+w]
        handleImg = cv2.cvtColor(handleImg, cv2.COLOR_BGRA2BGR)
        masked_img = cv2.bitwise_and(handleImg, handleImg, mask=mask)
        masked_video = cv2.bitwise_and(roi, roi, mask=mask_inv)
        
        added = masked_img + masked_video
        self.video[300:300+h, 100:100+w] = added
        

    def CountTime(self):
        now = datetime.datetime.now()
        now2 = datetime.datetime.now()
        now = now.strftime("%Y.%m.%d")
        now2 = now2.strftime("%H:%M:%S")
        cv2.putText(self.video, str(now), (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))
        cv2.putText(self.video, str(now2), (0, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))

    def board_text(self, num, x,y,r,g,b):
        cv2.putText(self.video, str(num), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (r, g, b))

    # 그래프를 생성하는 함수
    def draw_graph(self, data):
        
        fig = Figure(figsize=(2, 2), dpi=100)
        canvas = FigureCanvas(fig)
        fig.patch.set_alpha(1)

        ax = fig.add_subplot(111)
        ax.set_ylim([0, 100])
        ax.bar(1, data)
        ax.set_xticks([])
        ax.set_title('Real-time Graph')
        ax.set_xlabel('RPM')
        ax.set_ylabel('Brightness')
        canvas.draw()
        graph_image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8')
        graph_image = graph_image.reshape(canvas.get_width_height()[::-1] + (3,))
        return graph_image
    
    def graph_show(self, frame , data):
            # 그래프 이미지 생성
        graph_image = self.draw_graph(data)
        
        # 그래프 이미지를 OpenCV BGR 포맷으로 변환
        graph_image_bgr = cv2.cvtColor(graph_image, cv2.COLOR_RGB2BGR)
        
        # 그래프 이미지를 원본 프레임에 합성
        graph_h, graph_w, _ = graph_image_bgr.shape
        frame_h, frame_w, _ = frame.shape
        
        # 그래프 이미지가 프레임보다 크지 않도록 크기 조정
        if graph_w > frame_w:
            scale = frame_w / graph_w
            graph_image_bgr = cv2.resize(graph_image_bgr, (frame_w, int(graph_h * scale)))
            graph_h, graph_w, _ = graph_image_bgr.shape

        # 프레임 위에 그래프 이미지 배치
        frame[480-graph_h-self.board_value:graph_h+480-graph_h-self.board_value, 640-graph_w:graph_w+640-graph_w] = graph_image_bgr
