from pymavlink import mavutil
import struct
# import matplotlib.pyplot as plt
# from datetime import datetime
# import matplotlib.dates as mdates

serial_port = '/dev/ttyUSB0'
baud_rate = 2000000

# Initialize MAVLink connection with the serial port and baud rate
mavlink_connection = mavutil.mavlink_connection(serial_port, baud=baud_rate)

# Struct format: I = uint32_t, f = float, H = uint16_t, B = uint8_t, 120s = 120 bytes
struct_format = 'IIIIIffffffffffffffffHHB120s'

def handle_ret_lidar_distance_data_packet(msg):
    global timestamps, imu_temperatures, apd_temperatures
    global last_imu_temperature, last_apd_temperature

    binary_data = msg.data
    header = binary_data[:10] # 10 first bites are some header informations
    check_sum = binary_data[-2:] # 2 last bits are checksum
    struct_data = binary_data[10:219]

    # Unpack the data based on the format
    unpacked_data = struct.unpack(struct_format, struct_data)

    field_names = [
        'lidar_sync_delay_time',
        'time_stamp_s_step',
        'time_stamp_us_step',
        'sys_rotation_period',
        'com_rotation_period',
        'com_horizontal_angle_start',
        'com_horizontal_angle_step',
        'sys_vertical_angle_start',
        'sys_vertical_angle_span',
        'apd_temperature',
        'dirty_index',
        'imu_temperature',
        'up_optical_q',
        'down_optical_q',
        'apd_voltage',
        'imu_angle_x_offset',
        'imu_angle_y_offset',
        'imu_angle_z_offset',
        'b_axis_dist',
        'theta_angle',
        'ksi_angle',
        'packet_id',
        'payload_size',
        'lidar_work_status',
        'reflect_data'
    ]

    print(f"\n --------------  {msg.get_type()} | {len(msg.data)} ----------------")
    print(f"h = {len(header)}, d = {len(struct_data)}, cs = {len(check_sum)}")

    # Extract temperatures and timestamp
    imu_temperature = unpacked_data[field_names.index('imu_temperature')]
    apd_temperature = unpacked_data[field_names.index('apd_temperature')]
    #data = unpack_data[field_names.index('variable_from_the_list')]


def parse_mavlink():
    while True:
        try:
            msg = mavlink_connection.recv_match()
            if msg:
                if msg.get_type() == "UNKNOWN_17" and len(msg.data) == 221:
                    handle_ret_lidar_distance_data_packet(msg)

        except KeyboardInterrupt:
            print("Exiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    parse_mavlink()