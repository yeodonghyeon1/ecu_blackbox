import cv2
import time


class Visual:
    def __init__(self):
        pass

    def resize(self, capW, capH, video):
        video = cv2.resize(video, (capW, capH), interpolation=cv2.INTER_CUBIC)# 프레임 읽기 정상
        self.video = video
        self.capW = capW
        self.capH = capH

    def board_graphic(self, board_value, r,g,b):
        board_value = self.capH - board_value
        cv2.rectangle(self.video, (0, board_value), (self.capW, self.capH), (r, g, b), -1)
        cv2.rectangle(self.video, (0, board_value+1), (self.capW, self.capH-1), (r+72, g+72, b+72), -1)
        cv2.rectangle(self.video, (0, board_value+2), (self.capW, self.capH-2), (r+92, g+92, b+92), -1)
        cv2.rectangle(self.video, (0, board_value+3), (self.capW, self.capH-3), (r+102, g+102, b+102), -1)
        cv2.rectangle(self.video, (0, board_value+4), (self.capW, self.capH-4), (r+112, g+112, b+112), -1)
        cv2.rectangle(self.video, (0, board_value+5), (self.capW, self.capH-5), (r+122, g+122, b+122), -1)
        cv2.rectangle(self.video, (10, board_value + 5), (int(self.capW/6), self.capH-5), (r, g, b), -1)
        self.board_text(3, int((10+int(self.capW/6))/2), 200,0,255,0)

        cv2.rectangle(self.video, (10+int(self.capW/6), board_value + 5), (int(self.capW/6)*2, self.capH-5), (r, g, b), -1)
        cv2.rectangle(self.video, (10+int(self.capW/6)*2, board_value + 5), (int(self.capW/6) *3, self.capH-5), (r, g, b), -1)
        cv2.rectangle(self.video, (10+int(self.capW/6)*3, board_value + 5), (int(self.capW/6)*4, self.capH-5), (r, g, b), -1)
        cv2.rectangle(self.video, (10+int(self.capW/6)*4, board_value + 5), (int(self.capW/6)*5, self.capH-5), (r, g, b), -1)
        cv2.rectangle(self.video, (10+int(self.capW/6)*5, board_value + 5), (int(self.capW/6)*6, self.capH-5), (r, g, b), -1)

    def handleImageToVideo(self, handleImg, random_value):
        
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
        curTime = time.time()
        cv2.putText(self.video, str(curTime), (0, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0))

    def board_text(self, num, x,y,r,g,b):
        cv2.putText(self.video, str(num), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (r, g, b))