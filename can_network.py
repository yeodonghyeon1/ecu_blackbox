import cantools
import can_network

def canData():
    can_bus = can_network.interface.Bus('slcan0', bustype='socketcan')
    data = can_bus.recv()
    print(data)
    data_data = data.data #can프로토콜의 data 필드 값
    #data_id = data.arbitration_id #can프로토콜 ID
    return data_data