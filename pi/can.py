import can
import datetime
import time
import csv
import pi.define as de

def can_net():
   bus = can.interface.Bus(channel='can0', bustype='socketcan')
   file_counter = 1
   file = de.open_new_file(file_counter)
   start_time = time.time()
   writer = csv.DictWriter(file, fieldnames=de.fieldnames)
   writer.writeheader()

   try:
         while True:
            if time.time() - start_time >= 30:
               file.close()
               file_counter+=1
               file = de.open_new_file(file_counter)
               start_time = time.time()
               writer = csv.DictWriter(file, fieldnames=de.fieldnames)
               writer.writeheader()
            message=bus.recv()
            data = int.from_bytes(message.data, byteorder='big') #비트 연산을 위해 정수 변환
            if message.arbitration_id in [de.EMS11, de.EMS12, de.ESP12, de.TCU12, de.SAS11]:
               csv_writer = csv.writer(file)
               de.process_data(message, data, file)
               file.flush()

   finally:
      file.close()
