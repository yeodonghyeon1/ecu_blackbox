import datetime
import csv
import math

EMS11=0x316
EMS12=0x329
ESP12=0x220
TCU12=0x43F
SAS11=0x2B0
fieldnames=['time', 'ID', 'VS', 'RPM', 'eng_temp', 'break_on_off', 'TPS', 'PV_AC_CAN', 'CONF_TCU', 'break_PRES', 'CUR_GR', 's_angle', 's_speed']

def open_new_file(file_counter):
    now = datetime.datetime.now()
    filename = filename = now.strftime("%Yy_%mm_%dd_%Hh_%Mm_%Ss.csv")
    csv_header = ['Timestamp', 'ID', 'DLC', 'Data']
    return open("../camera/csv/{}".format(filename), 'w', newline='')

def extract_bits(data, start_bit, end_bit):
    binary_data = bin(data)[2:].zfill(64)
    extracted_bits = binary_data[start_bit:end_bit+1]
    return int(extracted_bits, 2)

def extract_bits_SAS(data, start_bit, end_bit):
    binary_data = bin(data)[2:].zfill(40)
    extracted_bits = binary_data[start_bit:end_bit+1]
    return int(extracted_bits, 2)

def extract_bits_break(data):
    binary_data = bin(data)[2:].zfill(16)
    extracted_bits = binary_data[2:13+1]
    return int(extracted_bits, 2)

def bits_puls(bits_front, bits_end):
   result = (bits_end << 8) | bits_front
   return result

def PV_AV_CAN(PV): #엑셀계패량 계산
   f_scale = 0.3906
   i_offset = 0
   result = i_offset + f_scale * PV
   return result

def break_val(val): # 브레이크 바 계산
   f_scale = 0.1
   f_offset = 0.0
   result = f_offset + f_scale * val
   result=floor_to(result)
   return result

def floor_to(value):
   factor = 10 ** 4
   return math.floor(value * factor) / factor

def TEMP_ENG(ENG): # 엔진 냉각수 계산
   f_scale = 0.75
   f_offset = -48.0
   result = f_offset + f_scale * ENG
   return result

def RPM_count(RPM): # RPM 계산
   i_offset = 0
   f_scale = 0.25
   result = i_offset + math.trunc(f_scale * RPM)
   return result

def SAS_angle(angle): #각도
   f_scale = 0.1
   f_offset = 0.0
   angle = int(angle)
   if angle >> 15 ==1:
     angle = ~angle+1
   result = f_offset + f_scale * angle
   return result

def SAS_speed(speed): #헨들 속도?
   f_scale = 4.0
   f_offset = 0.0
   result = f_offset + f_scale * speed
   return result

def process_data(message, data, file):
   csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
   if message.arbitration_id == EMS11:
       EMS11_VS = extract_bits(data, 48, 55) #속도
       EMS11_N1 = extract_bits(data, 16, 23)
       EMS11_N2 = extract_bits(data, 24, 31)
       EMS11_N3 = bits_puls(EMS11_N1, EMS11_N2)
       EMS11_N = RPM_count(EMS11_N3) #RPM
       csv_writer.writerow({'time': message.timestamp, 'ID': message.arbitration_id, 'VS': EMS11_VS, 'RPM': EMS11_N})
   elif message.arbitration_id == EMS12:
       EMS12_TEMP_ENG_t = extract_bits(data, 8, 15) #냉각수 온도
       EMS12_TEMP_ENG = TEMP_ENG(EMS12_TEMP_ENG_t)
       EMS12_BRAKE = extract_bits(data, 38, 39) # 브레이크 on/off 여부
       EMS12_TPS = extract_bits(data, 40, 47) #스로틀 각도가...
       EMS12_PV_AC_CAN_t = extract_bits(data, 48, 55) # 가속 폐달 값
       EMS12_PV_AC_CAN = PV_AV_CAN(EMS12_PV_AC_CAN_t)
       EMS12_CONF_TCU = extract_bits(data, 26, 28) # 기어박스 유형
       csv_writer.writerow({'time': message.timestamp, 'ID': message.arbitration_id, 'eng_temp': EMS12_TEMP_ENG, 'break_on_off': EMS12_BRAKE, 'TPS': EMS12_TPS, 'PV_AC_CAN': EMS12_PV_AC_CAN, 'CONF_TCU': EMS12_CONF_TCU})
   elif message.arbitration_id == ESP12:
       ESP12_CYL_PRES_1 = extract_bits(data, 24, 31) # 브레이크 바
       ESP12_CYL_PRES_2 = extract_bits(data, 32, 39)
       ESP12_CYL_PRES_s = bits_puls(ESP12_CYL_PRES_1, ESP12_CYL_PRES_2)
       ESP12_CYL_PRES_t = extract_bits_break(ESP12_CYL_PRES_s)
       ESP12_CYL_PRES = break_val(ESP12_CYL_PRES_t)
       csv_writer.writerow({'time': message.timestamp, 'ID': message.arbitration_id, 'break_PRES': ESP12_CYL_PRES})
   elif message.arbitration_id == TCU12:
       TCU12_CUR_GR = extract_bits(data, 12, 15) # 변속기
       csv_writer.writerow({'time': message.timestamp, 'ID': message.arbitration_id, 'CUR_GR': TCU12_CUR_GR})
   elif message.arbitration_id == SAS11:
       SAS11_angle_1 = extract_bits_SAS(data, 0, 7)
       SAS11_angle_2 = extract_bits_SAS(data, 8, 15)
       SAS11_angle_3 = bits_puls(SAS11_angle_1, SAS11_angle_2)
       SAS11_angle = SAS_angle(SAS11_angle_3) #핸들 각도
       SAS11_speed_1 = extract_bits_SAS(data, 16, 23)
       SAS11_speed = SAS_speed(SAS11_speed_1) #핸들 스피드
       csv_writer.writerow({'time': message.timestamp, 'ID': message.arbitration_id, 's_angle': SAS11_angle, 's_speed': SAS11_speed})

__all__ = ['EMS11', 'EMS12', 'ESP12', 'TCU12', 'SAS11', 'open_new_file', 'extract_bits', 'process_data']
