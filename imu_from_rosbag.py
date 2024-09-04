#!/usr/bin/env python3
import rospy
import sys
import rosbag
import numpy as np
import csv
import os
from os.path import expanduser
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq


# Matplotlib configuration 
plt.rcParams['axes.grid'] = True

def main(args):
    rospy.init_node('Extract_IMU_data_from_bag_node')

    t0 = rospy.get_time()
    print(f"t0 = {t0}")
    
    secs = int(t0)
    print(secs)
    nsecs = t0 - secs

    """"""""""""""
    " Parameters "
    """"""""""""""
    bagfile = rospy.get_param('~bagfile_path', args[1])
    topic = rospy.get_param('~imu_topic_name', '/unilidar/imu')

    """""""""""""""""""""""""""""
    " IMU data  Directory Path  "
    """""""""""""""""""""""""""""
    extractDataPath = "/home/ws/src/data_lidar/filtered_data/2AUG_parking/imu" # expanduser("~") + '/imu_data_raw/'
    if not os.path.isdir(extractDataPath):
        os.mkdir(extractDataPath)

    print(f"\nIMU raw data will be saved in the following directory: \n\n\n\t {extractDataPath}\n")

    """""""""""""""""
    " Parse Bagfile "
    """""""""""""""""
    bag = rosbag.Bag(bagfile)

    N = bag.get_message_count(topic)  # number of measurement samples

    data = np.zeros((6, N))  # preallocate vector of measurements
    time_sample = np.zeros((3, N))  # preallocate vector of measurements

    cnt = 0
    avgSampleRate = 0
    for topic, msg, t in bag.read_messages(topics=[topic]):
        data[0, cnt] = msg.linear_acceleration.x
        data[1, cnt] = msg.linear_acceleration.y
        data[2, cnt] = msg.linear_acceleration.z
        data[3, cnt] = msg.angular_velocity.x
        data[4, cnt] = msg.angular_velocity.y
        data[5, cnt] = msg.angular_velocity.z
        time_sample[0, cnt] = msg.header.stamp.secs
        time_sample[1, cnt] = msg.header.stamp.nsecs
        if cnt > 0:
            initial_time_seconds = time_sample[0, 0] + time_sample[1, 0] / 1e9
            current_time_seconds = time_sample[0, cnt] + time_sample[1, cnt] / 1e9
            previous_time_seconds = time_sample[0, cnt-1] + time_sample[1, cnt-1] / 1e9
            time_sample[2, cnt] = current_time_seconds - initial_time_seconds
            
            avgSampleRate += time_sample[1, cnt]
            print(avgSampleRate)
        cnt += 1

    if cnt > 1:
        sampleRate = avgSampleRate / (cnt - 1)
        print(sampleRate)
    else:
        sampleRate = 0

    bag.close()

    print(f"[{rospy.get_time() - t0:0.2f} seconds] Bagfile parsed\n")

    """""""""""""""
    " write to csv "
    """""""""""""""
    fname = 'allan_A_xyz_G_xyz_'
    csv_file_path = os.path.join(extractDataPath, f'{fname}_rate_{sampleRate:.2f}.csv')
    with open(csv_file_path, 'wt', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(('Time', 'Ax', 'Ay', 'Az', 'Gx', 'Gy', 'Gz'))

        for i in range(data.shape[1]):
            writer.writerow((time_sample[2, i], data[0, i], data[1, i], data[2, i], data[3, i], data[4, i], data[5, i]))
            
    """"""""""""""""""""""""
    " Plot time values     "
    """"""""""""""""""""""""
    
    # Read the CSV file into a pandas DataFrame
    data = pd.read_csv(csv_file_path)

    # Extract columns
    time = data['Time']
    ax = data['Ax']
    ay = data['Ay']
    az = data['Az']
    gx = data['Gx']
    gy = data['Gy']
    gz = data['Gz']

    # Create a new figure for the time-domain plots
    plt.figure(figsize=(12, 8))

    # Plot each sensor's data against time
    plt.subplot(2, 1, 1)
    plt.plot(time, ax, label='Ax', color='r')
    plt.plot(time, ay, label='Ay', color='g')
    plt.plot(time, az, label='Az', color='b')
    plt.xlabel('Time [s]')
    plt.ylabel('Acceleration [m/s2]')
    plt.title('Acceleration vs Time')
    plt.legend()
    plt.ylim(-5, +5)

    plt.subplot(2, 1, 2)
    plt.plot(time, gx, label='Gx', color='r')
    plt.plot(time, gy, label='Gy', color='g')
    plt.plot(time, gz, label='Gz', color='b')
    plt.xlabel('Time [s]')
    plt.ylabel('Angular Velocity [degrees/s***]')
    plt.title('Angular Velocity vs Time')
    plt.legend()
    plt.ylim(-0.10, +0.10)


    # plt.subplot(3, 1, 3)
    # plt.plot(time, ax, label='Ax', color='r', alpha=0.5)
    # plt.plot(time, ay, label='Ay', color='g', alpha=0.5)
    # plt.plot(time, az, label='Az', color='b', alpha=0.5)
    # plt.plot(time, gx, label='Gx', color='r', linestyle='--')
    # plt.plot(time, gy, label='Gy', color='g', linestyle='--')
    # plt.plot(time, gz, label='Gz', color='b', linestyle='--')
    # plt.grid()
    # plt.xlabel('Time')
    # plt.ylabel('Combined Data')
    # plt.title('Combined Plot')
    # plt.legend()

    # Adjust layout
    plt.tight_layout()

    # Show plot
    # plt.show()
    
    """""""""""""""""""""""""""""
    " Plot frequency values     "
    """""""""""""""""""""""""""""
    
    # Fourier Transform
    fs = 1 / sampleRate  # Sampling frequency
    fs = 227
    
    
    # Calculate Fourier Transform
    N = len(time)

    T = time[1] - time[0]  # Sampling interval
    yf_ax = fft(ax.to_numpy()-(ax.to_numpy()).mean())
    yf_ay = fft(ay.to_numpy()-(ay.to_numpy()).mean())
    yf_az = fft(az.to_numpy()-(az.to_numpy()).mean())
    yf_gx = fft(gx.to_numpy()-(gx.to_numpy()).mean())
    yf_gy = fft(gy.to_numpy()-(gy.to_numpy()).mean())
    yf_gz = fft(gz.to_numpy()-(gz.to_numpy()).mean())
    xf = fftfreq(N, T)[:N//2]
    
    # T = time[1] - time[0]  # Sampling interval
    # yf_ax = fft(ax.to_numpy())
    # yf_ay = fft(ay.to_numpy())
    # yf_az = fft(az.to_numpy())
    # yf_gx = fft(gx.to_numpy())
    # yf_gy = fft(gy.to_numpy())
    # yf_gz = fft(gz.to_numpy())
    # xf = fftfreq(N, T)[:N//2]

    print(f"fs = {fs}. sampleRate={sampleRate}. N = {N}. time={time}, T={T}")
    # Create a new figure for the frequency-domain plots
    plt.figure(figsize=(12, 8))

    # Plot Fourier Transforms
    plt.subplot(2, 1, 1)
    plt.plot(xf, 2.0/N * np.abs(yf_ax[:N//2]), label='Ax', color='r')
    plt.plot(xf, 2.0/N * np.abs(yf_ay[:N//2]), label='Ay', color='g')
    plt.plot(xf, 2.0/N * np.abs(yf_az[:N//2]), label='Az', color='b')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Acceleration Frequency Spectrum')
    plt.legend()
    # plt.xlim(1, 4)
    # plt.ylim(1, 16)

    plt.subplot(2, 1, 2)
    plt.plot(xf, 2.0/N * np.abs(yf_gx[:N//2]), label='Gx', color='r')
    plt.plot(xf, 2.0/N * np.abs(yf_gy[:N//2]), label='Gy', color='g')
    plt.plot(xf, 2.0/N * np.abs(yf_gz[:N//2]), label='Gz', color='b')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Angular Velocity Frequency Spectrum')
    plt.legend()
    # plt.xlim(1, 4)
    # plt.ylim(1, 16)

    # plt.subplot(3, 1, 3)
    # plt.plot(xf, 2.0/N * np.abs(yf_ax[:N//2]), label='Ax', color='r', alpha=0.5)
    # plt.plot(xf, 2.0/N * np.abs(yf_ay[:N//2]), label='Ay', color='g', alpha=0.5)
    # plt.plot(xf, 2.0/N * np.abs(yf_az[:N//2]), label='Az', color='b', alpha=0.5)
    # plt.plot(xf, 2.0/N * np.abs(yf_gx[:N//2]), label='Gx', color='r', linestyle='--')
    # plt.plot(xf, 2.0/N * np.abs(yf_gy[:N//2]), label='Gy', color='g', linestyle='--')
    # plt.plot(xf, 2.0/N * np.abs(yf_gz[:N//2]), label='Gz', color='b', linestyle='--')
    # plt.xlabel('Frequency (Hz)')
    # plt.ylabel('Combined Amplitude')
    # plt.title('Combined Frequency Spectrum')
    # plt.legend()

    # Adjust layout
    plt.tight_layout()

    # Show plot
    plt.show()


if __name__ == '__main__':
    main(sys.argv)
