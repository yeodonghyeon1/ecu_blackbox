import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

# 그래프를 생성하는 함수
def draw_graph(data):
    # fig = Figure(figsize=(5, 2), dpi=100)
    fig = plt.figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    ax.bar(1, data)
    # ax.xsticks(1, "rpm")
    ax.set_title('Real-time Graph')
    ax.set_xlabel('Frame')
    ax.set_ylabel('Brightness')
    # ax.grid(True)

    canvas.draw()
    graph_image = np.frombuffer(canvas.tostring_rgb(), dtype='uint8')
    graph_image = graph_image.reshape(canvas.get_width_height()[::-1] + (3,))
    
    return graph_image

# 비디오 캡처 초기화
cap = cv2.VideoCapture(0)

# 그래프에 표시할 데이터
# data = []

while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    # 임의의 데이터 추가 (여기서는 프레임의 밝기 평균값)
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # avg_brightness = np.mean(gray)
    # data.append(avg_brightness)
    data =1
    # 데이터의 길이를 제한
    # if len(data) > 100:
    #     data.pop(0)
    
    # 그래프 이미지 생성
    graph_image = draw_graph(data)
    
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
    frame[0:graph_h, 0:graph_w] = graph_image_bgr
    
    # 화면에 표시
    cv2.imshow('Frame with Graph', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()