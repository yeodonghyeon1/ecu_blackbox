# import csv

# # 초기 값 설정
# start_time = 1717054131
# count = 1
# rows = []

# # 10초 동안의 데이터 생성
# for _ in range(200):  # 10초 * 20 = 200개의 데이터 생성
#     rows.append([start_time, count])
#     count += 1
#     if count % 20== 0:
#         start_time += 1

# # CSV 파일 생성
# with open('time_count_data.csv', 'w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerow(['time', 'count'])  # 컬럼 헤더 작성
#     writer.writerows(rows)

# print("CSV 파일이 성공적으로 생성되었습니다.")


# import time
# from unittest.mock import patch

# # 타임스탬프를 고정된 값으로 반환하는 함수를 정의합니다.
# def mock_time():
#     return 1717054130

# # time.time() 함수를 mock_time() 함수로 패치하여 호출
# with patch('time.time', mock_time):
#     current_time = time.time()
#     print("Mocked time.time():", current_time)
#     # 다른 코드에서도 동일하게 1717054130이 출력됩니다.
    
# # 이 블록을 벗어나면 time.time()은 다시 원래의 기능으로 돌아갑니다.
# real_time = time.time()
# print("Real time.time()", real_time)


import time

# 초기 유닉스 타임스탬프 값
initial_timestamp = 1717054130
# 모킹이 시작된 시점의 실제 시간
start_time = time.time()

def custom_time():
    # 현재 시간에서 시작 시간간격을 계산하고, initial_timestamp에 더해줌
    elapsed = time.time() - start_time
    return initial_timestamp + elapsed

# 기존 time.time() 함수를 저장
original_time = time.time

# time.time() 함수를 custom_time 함수를 사용하도록 대체
time.time = custom_time

# 해당 블록 내부에서 시간 경과를 확인하는 예제
print("Initial mocked time.time():", time.time())
time.sleep(1)  # 1초 대기
print("After 1 second, mocked time.time():", time.time())
time.sleep(2)  # 2초 대기
print("After 2 more seconds, mocked time.time():", time.time())

# 다시 원래의 time.time() 함수로 복원
time.time = original_time

# 복원된 time.time() 호출 시 실제 시간 반환
print("Restored real time.time():", time.time())
