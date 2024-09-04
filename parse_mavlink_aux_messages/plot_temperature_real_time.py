from pymavlink import mavutil
import struct
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.dates as mdates

serial_port = '/dev/ttyUSB0'
baud_rate = 2000000

# Initialize MAVLink connection with the serial port and baud rate
mavlink_connection = mavutil.mavlink_connection(serial_port, baud=baud_rate)

# Struct format: I = uint32_t, f = float, H = uint16_t, B = uint8_t, 120s = 120 bytes
struct_format = 'IIIIIffffffffffffffffHHB120s'

# Initialize lists for plotting
timestamps = []
imu_temperatures = []
apd_temperatures = []

# Variables to store the last recorded temperatures
last_imu_temperature = None
last_apd_temperature = None

# Create a plot
plt.ion()  # Enable interactive mode
fig, ax = plt.subplots()
imu_line, = ax.plot([], [], 'r-', label='IMU Temperature')  # Line plot for IMU temperature
apd_line, = ax.plot([], [], 'b-', label='APD Temperature')  # Line plot for APD temperature
ax.set_xlabel('Time')
ax.set_ylabel('Temperature (°C)')
ax.set_title('Real-Time Temperature Plot')
ax.legend()

# Format the x-axis to show time
ax.xaxis.set_major_formatter(mdates.DateFormatter('%M:%S'))
ax.xaxis.set_major_locator(mdates.SecondLocator())

def handle_ret_lidar_distance_data_packet(msg):
    global timestamps, imu_temperatures, apd_temperatures
    global last_imu_temperature, last_apd_temperature

    binary_data = msg.data
    header = binary_data[:10]
    check_sum = binary_data[-2:]
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
    timestamp_s = unpacked_data[field_names.index('time_stamp_s_step')]
    timestamp_us = unpacked_data[field_names.index('time_stamp_us_step')]
    timestamp = datetime.fromtimestamp(timestamp_s + timestamp_us / 1e6)

    # Check if the new IMU temperature differs significantly from the last IMU temperature
    if last_imu_temperature is not None and abs(imu_temperature - last_imu_temperature) > 5:
        print(f"IMU temperature difference too large ({imu_temperature - last_imu_temperature:.2f} °C). Skipping plot update.")
    else:
        # Append IMU temperature data for plotting
        timestamps.append(timestamp)
        imu_temperatures.append(imu_temperature)
        last_imu_temperature = imu_temperature

    # Check if the new APD temperature differs significantly from the last APD temperature
    if last_apd_temperature is not None and abs(apd_temperature - last_apd_temperature) > 5:
        print(f"APD temperature difference too large ({apd_temperature - last_apd_temperature:.2f} °C). Skipping plot update.")
    else:
        # Append APD temperature data for plotting
        apd_temperatures.append(apd_temperature)
        last_apd_temperature = apd_temperature

    # Update the plot
    ax.clear()
    ax.plot(timestamps, imu_temperatures, 'r-', label='IMU Temperature')
    ax.plot(timestamps, apd_temperatures, 'b-', label='APD Temperature')
    ax.set_xlabel('Time')
    ax.set_ylabel('Temperature (°C)')
    ax.set_ylim([min(min(imu_temperatures, default=0), min(apd_temperatures, default=0)) - 1, 
                 max(max(imu_temperatures, default=0), max(apd_temperatures, default=0)) + 1])
    ax.set_title('Real-Time Temperature Plot')
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%M:%S'))
    ax.xaxis.set_major_locator(mdates.SecondLocator())
    plt.xticks(rotation=45)
    plt.grid()
    plt.draw()
    plt.pause(0.1)  # Adjust pause for your data rate

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
