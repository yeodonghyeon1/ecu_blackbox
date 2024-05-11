import socket
import os

def send_file(sock, filepath):
    # 파일 전송 함수
    with open(filepath, 'rb') as f:
        sock.sendall(f.read())

def main():
    host = '192.168.0.80'
    port = 12345
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    # camera2 폴더 내의 모든 파일 전송
    folder_path = '../camera2'
    for filename in os.listdir(folder_path):
        if filename.endswith(".mp4"):  # 동영상 파일 확인
            filepath = os.path.join(folder_path, filename)
            # 파일 이름을 먼저 전송
            client_socket.sendall(filename.encode())
            send_file(client_socket, filepath)
            print(f'{filename} 파일이 전송되었습니다.')
    
    client_socket.close()

if __name__ == '__main__':
    main()