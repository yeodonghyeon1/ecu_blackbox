import socket
import os

def recv_file(sock, filename):
    # 파일 수신 함수
    with open(filename, 'wb') as f:
        while True:
            data = sock.recv(4096)
            if not data:
                break
            print("a")
            f.write(data)

def main():
    host = '0.0.0.0'
    port = 12345
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print('서버가 시작되었습니다.')
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f'{addr}에 연결됨')

        while True:
            # 파일 이름 수신
            filename = client_socket.recv(4096).decode()
            if not filename:
                break
            print(f'파일 이름 수신: {filename}')
            save_path = os.path.join('../camera3', filename)
            client_socket.send(b'ok')  # 파일 이름 수신 확인
            
            recv_file(client_socket, save_path)
            
            print(f'{filename} 파일이 성공적으로 저장되었습니다.')
            client_socket.send(b'ok')  # 다음 파일 준비 완료
            
        client_socket.close()
        print('연결 종료')

    server_socket.close()
    
if __name__ == '__main__':
    main()