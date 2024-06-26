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
        self.board_value2 = board_value
        cv2.rectangle(self.video, (0, board_value), (self.capW, self.capH), (r, g, b), -1)
        cv2.rectangle(self.video, (0, board_value+1), (self.capW, self.capH-1), (r+240, g+255, b+240), -1)
        cv2.rectangle(self.video, (0, board_value+2), (self.capW, self.capH-2), (r+240, g+255, b+240), -1)
        cv2.rectangle(self.video, (0, board_value+3), (self.capW, self.capH-3), (r+240, g+255, b+240), -1)
        cv2.rectangle(self.video, (0, board_value+4), (self.capW, self.capH-4), (r+255, g+228, b+225), -1)
        cv2.rectangle(self.video, (0, board_value+5), (self.capW, self.capH-5), (r+122, g+122, b+122), -1)
        cv2.rectangle(self.video, (0, board_value-10), (self.capW, self.capH-5), (r+122, g+122, b+122), -1)

        cv2.rectangle(self.video, (10, board_value + 5), (int(self.capW/4), self.capH-5), (r, g, b), -1)
        

        cv2.rectangle(self.video, (10+int(self.capW/4), board_value + 5), (int(self.capW/4)*2, self.capH-5), (r, g, b), -1)
        cv2.rectangle(self.video, (10+int(self.capW/4)*2, board_value + 5), (int(self.capW/4) *3, self.capH-5), (240, 255, 240), -1)
        cv2.rectangle(self.video, (10+int(self.capW/4)*3, board_value + 5), (int(self.capW/4)*4, self.capH-5), (240, 255, 240), -1)
        # cv2.rectangle(self.video, (10+int(self.capW/6)*4, board_value + 5), (int(self.capW/6)*5, self.capH-5), (r, g, b), -1)
        # cv2.rectangle(self.video, (10+int(self.capW/6)*5, board_value + 5), (int(self.capW/6)*6, self.capH-5), (r, g, b), -1)
        # self.board_text("eng", int((-140+int(self.capW/4))), board_value+30, 0,255,0)
        # self.board_text("axcel", int((10+int(self.capW/4))), board_value+30, 0,255,0)
        # self.board_text("press", int((170+int(self.capW/4))), board_value+30, 0,255,0)
        # self.board_text("gear", int((340+int(self.capW/4))), board_value+30, 0,255,0)

        cv2.putText(self.video, str("CUR_GR"), (int((330+int(self.capW/4))), self.board_value2-1), cv2.FONT_HERSHEY_TRIPLEX  , 0.4, (0,0,0))
        cv2.putText(self.video, str("VS"), (int((170+int(self.capW/4))), self.board_value2-1), cv2.FONT_HERSHEY_TRIPLEX, 0.4, (0,0,0))
        cv2.putText(self.video, str("RPM"), (int((10+int(self.capW/4))), self.board_value2-1), cv2.FONT_HERSHEY_TRIPLEX, 0.4, (0,0,0))
        cv2.putText(self.video, str("eng_temp"), (int((-150+int(self.capW/4))), self.board_value2-1), cv2.FONT_HERSHEY_TRIPLEX, 0.4, (0,0,0))
   
    def handleImageToVideo(self, random_value, handleImg):
        handleImg = cv2.resize(handleImg, (120, 120))
        
        
        h, w = handleImg.shape[:2]
        (cX, cY) = (w // 2, h // 2)
        
        M = cv2.getRotationMatrix2D((cX, cY), random_value, 1.0)
        handleImg = cv2.warpAffine(handleImg, M, (w, h))


        _, mask = cv2.threshold(handleImg[:,:,3] , 1 ,255, cv2.THRESH_BINARY)
        # print(mask.shape)
        mask_inv = cv2.bitwise_not(mask)
        roi = self.video[480:480+h , 10:10+w]
        handleImg = cv2.cvtColor(handleImg, cv2.COLOR_BGRA2BGR)
        masked_img = cv2.bitwise_and(handleImg, handleImg, mask=mask)
        masked_video = cv2.bitwise_and(roi, roi, mask=mask_inv)
        
        added = masked_img + masked_video
        self.video[480:480+h, 10:10+w] = added
    
    def rpm(self, random_value, rpmImg):
        rpmImg = cv2.resize(rpmImg, (120, 120))
        
        h, w = rpmImg.shape[:2]
        # (cX, cY) = (w // 2, h // 2)
        # M = cv2.getRotationMatrix2D((cX, cY), random_value, 1.0)
        # rpmImg = cv2.warpAffine(rpmImg, M, (w, h))
        _, mask = cv2.threshold(rpmImg[:,:,3] , 1 ,255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        roi = self.video[480:480+h , 10:10+w]
        rpmImg = cv2.cvtColor(rpmImg, cv2.COLOR_BGRA2BGR)

        masked_img = cv2.bitwise_and(rpmImg, rpmImg, mask=mask)
        masked_video = cv2.bitwise_and(roi, roi, mask=mask_inv)
        added = masked_img + masked_video
        self.video[480:480+h, 10:10+w] = added
        # h, w = rpmImg.shape[:2]
        # (cX, cY) = (w // 2, h // 2)
        
        # M = cv2.getRotationMatrix2D((cX, cY), random_value, 1.0)
        # rpmImg = cv2.warpAffine(rpmImg, M, (w, h))


        # _, mask = cv2.threshold(rpmImg[:,:,3] , 1 ,255, cv2.THRESH_BINARY)
        # # print(mask.shape)
        # mask_inv = cv2.bitwise_not(mask)
        # roi = self.video[480:480+h , 10:10+w]
        # handleImg = cv2.cvtColor(rpmImg, cv2.COLOR_BGRA2BGR)
        # masked_img = cv2.bitwise_and(handleImg, handleImg, mask=mask)
        # masked_video = cv2.bitwise_and(roi, roi, mask=mask_inv)
        
        # added = masked_img + masked_video
        # self.video[480:480+h, 10:10+w] = added
    
    def borad_data(self, ecu_data, data_jump, time_jump, before_data):

        #1 box
        try:
            if data_jump == 0:
                print() if ecu_data[809.0].empty else self.board_text( before_data["eng_temp"],
                                                                        int((-140+int(self.capW/4))), 
                                                                        self.board_value2+30, 0,255,0)            
            else:
                print() if ecu_data[809.0].empty else self.board_text(list(ecu_data[809.0]["eng_temp"])[data_jump + time_jump],
                                                                        int((-140+int(self.capW/4))), 
                                                                        self.board_value2+30, 0,255,0)
                before_data["eng_temp"] =list(ecu_data[809.0]["eng_temp"])[data_jump + time_jump]
        except:
            pass       

        #2 box
        try:
            if data_jump == 0:
                print() if ecu_data[790.0].empty else self.board_text(before_data["VS"],
                                                                        int((170+int(self.capW/4))), 
                                                                        self.board_value2+30, 0,255,0)
            else:
                print() if ecu_data[790.0].empty else self.board_text(list(ecu_data[790.0]["VS"])[data_jump + time_jump],
                                                                        int((170+int(self.capW/4))), 
                                                                        self.board_value2+30, 0,255,0)
                before_data["VS"] = list(ecu_data[790.0]["VS"])[data_jump + time_jump]
        except:
            pass
        #3 box
        try:
            if data_jump == 0:
                print() if ecu_data[790.0].empty else self.board_text(before_data["RPM"],
                                                                        int((10+int(self.capW/4))), 
                                                                        self.board_value2+30, 0,255,0)
            else:
                print() if ecu_data[790.0].empty else self.board_text(list(ecu_data[790.0]["RPM"])[data_jump + time_jump],
                                                                        int((10+int(self.capW/4))), 
                                                                        self.board_value2+30, 0,255,0)
                before_data["RPM"] = list(ecu_data[790.0]["RPM"])[data_jump + time_jump]
        except:
            pass              

        #4 box
        try:
            if data_jump == 0:
                print() if ecu_data[1087.0].empty else self.board_text(before_data["CUR_GR"],
                                                                            int((340+int(self.capW/4))), 
                                                                            self.board_value2+30, 0,255,0)
            else:
                print() if ecu_data[1087.0].empty else self.board_text(self.Gear(list(ecu_data[1087.0]["CUR_GR"])[data_jump + time_jump]),
                                                                            int((340+int(self.capW/4))), 
                                                                            self.board_value2+30, 0,255,0)
                before_data["CUR_GR"] = self.Gear(list(ecu_data[1087.0]["CUR_GR"])[data_jump + time_jump])
        except:
            pass


    def Gear(self, data):
        if data == 0:
            return "P"
        elif data == 7:
            return "R"
        elif data == 6:
            return "N"
        elif data == 5:
            return "D"
        elif data == 3:
            return "3"
        elif data == 2:
            return "2"
        elif data == 1:
            return "1"
        else:
            return 0

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
        
        fig = Figure(figsize=(2, 2), dpi=80)
        canvas = FigureCanvas(fig)
        fig.patch.set_alpha(1)

        ax = fig.add_subplot(111)
        ax.set_ylim([0, 1500])
        ax.bar(1, data, color='gray', edgecolor='black', linewidth=2, width=0.4)
        ax.set_facecolor('#F5F5DC')
        ax.set_xticks([])
        ax.set_title('Real-time RPM figures', fontsize=6)
        ax.set_xlabel('RPM', fontsize=6)
        # ax.set_ylabel('', fontsize=6)
        
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(2)
        
        fig.tight_layout(pad=1.0)

        canvas.draw()
        graph_image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8')
        graph_image = graph_image.reshape(canvas.get_width_height()[::-1] + (3,))
        return graph_image
    
    def graph_show(self, frame , data, data2):
            # 그래프 이미지 생성
            
        graph_image = self.draw_graph2(data, data2)
        
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

        #print(700-graph_w, graph_w+700-graph_w)
        # 프레임 위에 그래프 이미지 배치
        frame[640-graph_h-self.board_value:graph_h+640-graph_h-self.board_value, 630-graph_w:graph_w+630-graph_w] = graph_image_bgr


    def draw_graph2(self, data, data2):
            
        fig = Figure(figsize=(8, 2), dpi=60)
        canvas = FigureCanvas(fig)
        fig.patch.set_alpha(1)

        ax = fig.add_subplot(212)
        ax.set_xlim([0, 100])  # x축 범위 설정
        ax.set_facecolor('#F5F5DC')
        ax.set_yticks([])  # y축 눈금 제거
        ax.set_title('Real-time break-press figures', fontsize=10)
        ax.set_ylabel('break-press', fontsize=8)  # y축 라벨 수정
        # ax.set_xlabel('RPM', fontsize=6)  # x축 라벨 수정

        # # 두 번째 그래프
        ax2 = fig.add_subplot(211)  # 2행 1열 중 두 번째 위치
        ax2.set_xlim([0, 100])  # x축 범위 설정    
        ax2.set_facecolor('#F5F5DC')
        ax2.set_yticks([])  # y축 눈금 제거
        ax2.set_title('Second Real-time Accel figures', fontsize=10)  # 두 번째 그래프의 제목
        ax2.set_ylabel('accel-press', fontsize=8)  # y축 라벨 수정
        # ax2.set_xlabel('accel', fontsize=6)  # x축 라벨 수정

        # ax2.barh("accel-press", data, color='gray', edgecolor='black', linewidth=2, height=0.4)  # y축에 "break-press" 추가
        # ax.barh("break-press", data, color='gray', edgecolor='black', linewidth=2, height=0.4)  # y축에 "break-press" 추가


        ax2.barh("accel-press", data, color='gray', edgecolor='black', linewidth=2, height=0.4)  # y축에 "break-press" 추가
        ax.barh("break-press", data2, color='gray', edgecolor='black', linewidth=2, height=0.4)  # y축에 "break-press" 추가

        for spine in ax.spines.values():
            spine.set_edgecolor('black')
            spine.set_linewidth(2)
            
            fig.tight_layout(pad=1.0)

            canvas.draw()
            graph_image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8')
            graph_image = graph_image.reshape(canvas.get_width_height()[::-1] + (3,))
            return graph_image