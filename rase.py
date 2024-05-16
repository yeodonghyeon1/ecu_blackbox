import socket
import os

def send_file(sock, filepath):#rase 1
    with open(filepath, 'rb') as f:
        file_data = f.read()
    # 파일 데이터 전송
    sock.sendall(file_data)
    # 파일 전송 종료 신호 전송
    sock.sendall(b'--EOF--')

def main():
    host = '192.168.0.80'
    port = 12345
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    
    folder_path = '../camera2'
    while True:
        for filename in os.listdir(folder_path):
            if filename.endswith(".mp4"):
                client_socket.sendall("LC".encode())
                file_list = client_socket.recv(4096)  # 서버 응답 대기
                print(file_list)
                if file_list.decode().find(filename) != -1:
                    continue
                if file_list.decode() == "NOT_FILE":
                    filepath = os.path.join(folder_path, filename)
                    client_socket.sendall(filename.encode() + b'--EOF--')  # 파일 이름 전송
                    send_file(client_socket, filepath)
                    print(f'{filename} 파일이 전송되었습니다.')
                else:
                    filepath = os.path.join(folder_path, filename)
                    client_socket.sendall(filename.encode() + b'--EOF--')  # 파일 이름 전송
                    send_file(client_socket, filepath)
                    print(f'{filename} 파일이 전송되었습니다.')
                response = client_socket.recv(4096)  # 서버 응답 대기

    client_socket.close()

if __name__ == '__main__':
    main()