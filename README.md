# ECU Blackbox & Server 프로젝트

## 프로젝트 개요
이 프로젝트는 차량의 ECU(Electronic Control Unit) 데이터를 수집하고 시각화하는 블랙박스 시스템과 이를 위한 서버를 구현한 것입니다.

## 주요 기능

### ECU Blackbox
- **실시간 데이터 수집**
  - CAN 통신을 통한 차량 ECU 데이터 수집
  - 웹캠을 통한 실시간 영상 녹화
  - 엔진 온도, 차량 속도, RPM, 기어 상태 등 차량 정보 수집

- **데이터 시각화**
  - 실시간 차량 데이터 그래프 표시
  - 핸들 각도 시각화
  - 시간 정보 표시
  - RPM 게이지 표시

- **데이터 저장 및 전송**
  - 녹화된 영상 파일 저장
  - 수집된 ECU 데이터 CSV 파일 저장
  - 서버로 데이터 전송

### ECU Server
- **데이터 수신 및 관리**
  - 클라이언트로부터 영상 및 데이터 파일 수신
  - 파일 시스템 관리
  - 웹 인터페이스 제공

- **실시간 통신**
  - WebSocket을 통한 실시간 데이터 통신
  - 클라이언트-서버 간 양방향 통신

## 시스템 구성
- **클라이언트 (ECU Blackbox)**
  - Python 기반 데이터 수집 및 처리
  - OpenCV를 활용한 영상 처리
  - CAN 통신 모듈
  - 멀티스레딩 기반 동시 처리

- **서버 (ECU Server)**
  - Flask 기반 웹 서버
  - Socket.IO를 활용한 실시간 통신
  - 파일 저장 및 관리 시스템

## 설치 및 실행 방법

### 요구사항
- Python 3.x
- OpenCV
- Flask
- Socket.IO
- 기타 필요한 Python 패키지

### 실행 방법
1. ECU Blackbox 실행
```bash
python main.py
```

2. ECU Server 실행
```bash
python app.py
```

## 주요 파일 구조
```
ECU Blackbox/
├── main.py              # 메인 실행 파일
├── composition.py       # 영상 합성 및 처리
├── visualization.py     # 데이터 시각화
├── can_network.py       # CAN 통신 처리
└── source/             # 리소스 파일

ECU Server/
├── app.py              # 서버 메인 파일
├── templates/          # 웹 템플릿
└── static/            # 정적 파일
```

## 라이선스
MIT License

## 기여자
- @yeodonghyeon1
- @keonung08
- @KBohyeon
- @Sonyungeon
- @zmdmths