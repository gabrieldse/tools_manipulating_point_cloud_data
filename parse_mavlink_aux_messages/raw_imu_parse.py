from pymavlink import mavutil
import struct
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

'''
NOT Tested

typedef struct __mavlink_ret_imu_attitude_data_packet_t {
 float quaternion[4]; /*<  Quaternion Array.*/
 float angular_velocity[3]; /*<  Three-axis angular velocity values.*/
 float linear_acceleration[3]; /*<  Three-axis acceleration values.*/
 uint16_t packet_id; /*<  Data packet ID.*/
} mavlink_ret_imu_attitude_data_packet_t;
'''

serial_port = '/dev/ttyUSB0'
baud_rate = 2000000

# Initialize MAVLink connection with the serial port and baud rate
mavlink_connection = mavutil.mavlink_connection(serial_port, baud=baud_rate)

# Struct format: I = uint32_t, f = float, H = uint16_t, B = uint8_t, 120s = 120 bytes
struct_format = '4f3f3fH'

def handle_ret_imu_attitude_data_packet(msg):
    # global timestamps, imu_temperatures, apd_temperatures
    # global last_imu_temperature, last_apd_temperature

    binary_data = msg.data
    header = binary_data[:10] # 10 first bites are some header informations
    check_sum = binary_data[-2:] # 2 last bits are checksum
    struct_data = binary_data[10:52] #Actual 42 bytes of data

    # Unpack the data based on the format
    unpacked_data = struct.unpack(struct_format, struct_data)

    quaternion = unpacked_data[0:4]
    angular_velocity = unpacked_data[4:7]
    linear_acceleration = unpacked_data[7:10]
    packet_id = unpacked_data[10]

    field_names = {
        'quaternion': quaternion,
        'angular_velocity': angular_velocity,
        'linear_acceleration': linear_acceleration,
        'packet_id': packet_id,
    }

    print(f"\n --------------  {msg.get_type()} | {len(msg.data)} ----------------")
    print(f"h = {len(header)}, d = {len(struct_data)}, cs = {len(check_sum)}")

    print("Quaternion:", field_names['quaternion'])
    print("Angular Velocity:", field_names['angular_velocity'])
    print("Linear Acceleration:", field_names['linear_acceleration'])
    print("Packet ID:", field_names['packet_id'])

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