from pymavlink import mavutil
import struct
# import matplotlib.pyplot as plt
# from datetime import datetime
# import matplotlib.dates as mdates

'''
NOT Tested

typedef struct __mavlink_ret_lidar_distance_data_packet_t {
 uint16_t packet_id; /*<  Data packet ID.*/
 uint16_t packet_cnt; /*<  Data packet count.*/
 uint16_t payload_size; /*<  Data packet payload size.*/
 uint8_t point_data[240]; /*<  Data packet distance data.*/
} mavlink_ret_lidar_distance_data_packet_t;
'''
serial_port = '/dev/ttyUSB0'
baud_rate = 2000000
mavlink_connection = mavutil.mavlink_connection(serial_port, baud=baud_rate)

# Struct format: I = uint32_t, f = float, H = uint16_t, B = uint8_t, 120s = 120 bytes
struct_format = '3H240B'

def handle_ret_imu_attitude_data_packet(msg):

    binary_data = msg.data
    header = binary_data[:10] # 10 first bites are some header informations
    check_sum = binary_data[-2:] # 2 last bits are checksum
    struct_data = binary_data[10:256] #Actual 246 bytes of data

    # Unpack the data based on the format
    unpacked_data = struct.unpack(struct_format, struct_data)


    field_names = {
        'packet_id',
        'packet_cnt',
        'payload_size',
        'point_data',
    }

    print(f"\n --------------  {msg.get_type()} | {len(msg.data)} ----------------")
    print(f"h = {len(header)}, d = {len(struct_data)}, cs = {len(check_sum)}")

    #data = unpack_data[field_names.index('variable_from_the_list')]


def parse_mavlink():
    while True:
        try:
            msg = mavlink_connection.recv_match()
            if msg:
                if msg.get_type() == "UNKNOWN_19" : #and len(msg.data) == 221
                    handle_ret_imu_attitude_data_packet(msg)

        except KeyboardInterrupt:
            print("Exiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    parse_mavlink()