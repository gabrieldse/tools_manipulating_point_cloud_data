#!/usr/bin/env python3
import sys
import numpy as np
import csv
import os
from os.path import expanduser
import pandas as pd
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq
from scipy import signal

'''
Log files exported from .bin via the AMP Planner 2. 
              "export to ASCII log file"
Assumes time is exported in miliseconds round values.
'''
# Matplotlib configuration 
plt.rcParams['axes.grid'] = True

def main(args):
    """""""""""""""""""""""""""""
    " IMU data  Directory Path  "
    """""""""""""""""""""""""""""
    file_path = args[1]
    file_name = file_path.split("/")[-1]
    print
    
    save_path = os.path.dirname(args[0])

    """""""""""""""""
    " Parse LOG FILE "
    """""""""""""""""
    # open csv
    df = pd.read_csv(file_path, on_bad_lines='skip', low_memory=False) # ,nrows=3000

    # Filter rows where the first column is "IMU"
    imu_rows = df[df.iloc[:, 0] == "IMU"].copy()

    # Convert the second column to int and the ax-...-gz to float
    imu_rows.iloc[:, 1] = pd.to_numeric(imu_rows.iloc[:, 1], errors='coerce').astype('Int64')
    imu_rows.iloc[:, 2:8] = imu_rows.iloc[:, 2:8].apply(pd.to_numeric, errors='coerce').astype(float)

    time = imu_rows.iloc[:, 1]
    gx = imu_rows.iloc[:, 2]
    gy = imu_rows.iloc[:, 3]
    gz = imu_rows.iloc[:, 4]
    ax = imu_rows.iloc[:, 5]
    ay = imu_rows.iloc[:, 6]
    az = imu_rows.iloc[:, 7]

    N = len(ax)  # number of measurement samples

    fs = 1/((time.iloc[-1]-time.iloc[0])/((N-1)*1000)) #Sampling interval
    T = 1/fs
 
    # Calculate Fourier Transform
    yf_ax = fft(ax.to_numpy()-(ax.to_numpy()).mean())
    yf_ay = fft(ay.to_numpy()-(ay.to_numpy()).mean())
    yf_az = fft(az.to_numpy()-(az.to_numpy()).mean())
    yf_gx = fft(gx.to_numpy()-(gx.to_numpy()).mean())
    yf_gy = fft(gy.to_numpy()-(gy.to_numpy()).mean())
    yf_gz = fft(gz.to_numpy()-(gz.to_numpy()).mean())
    xf = fftfreq(N, T)[:N//2] 
    window = signal.windows.blackman(int(len(gx)/2))
    xf_black = xf * window

    """"""""""""""""""""""""
    " Plot time values     "
    """"""""""""""""""""""""

    # Create a figure for the time-domain plots
    plt.figure(figsize=(12, 8))
    time_s = np.linspace(time.iloc[0]/1000,time.iloc[-1]/1000,N) # time in seconds for plot

    # Plot each sensor's data against time
    plt.subplot(3, 1, 1)
    plt.plot(time_s, ax, label='Ax', color='r')
    plt.plot(time_s, ay, label='Ay', color='g')
    plt.plot(time_s, az, label='Az', color='b')
    plt.xlabel('Time [s]')
    plt.ylabel('Acceleration [m/s2]')
    plt.title('Acceleration vs Time')
    plt.legend()

    plt.subplot(3, 1, 2)
    plt.plot(xf, 2.0/N * np.abs(yf_ax[:N//2]), label='Ax', color='r')
    plt.plot(xf, 2.0/N * np.abs(yf_ay[:N//2]), label='Ay', color='g')
    plt.plot(xf, 2.0/N * np.abs(yf_az[:N//2]), label='Az', color='b')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Acceleration Frequency Spectrum')
    plt.legend()

    # plt.subplot(4, 1, 3)
    # plt.plot(np.log10(xf_black), 2.0/(N**2) * np.abs(yf_ax[:N//2])**2, label='Ax', color='r')
    # # plt.plot(xf, 2.0/(N**2) * np.abs(yf_ay[:N//2])**2, label='Ay', color='g')
    # # plt.plot(xf, 2.0/(N**2) * np.abs(yf_az[:N//2])**2, label='Az', color='b')
    # plt.xlabel('Frequency (Hz)')
    # plt.ylabel('Amplitude')
    # plt.title('Acceleration Frequency Spectrum with Black Windown')
    # plt.legend()

    plt.subplot(3, 1, 3)
    plt.plot(xf, 2.0/(N**2) * np.abs(yf_ax[:N//2])**2, label='Ax', color='r')
    plt.plot(xf, 2.0/(N**2) * np.abs(yf_ay[:N//2])**2, label='Ay', color='g')
    plt.plot(xf, 2.0/(N**2) * np.abs(yf_az[:N//2])**2, label='Az', color='b')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Acceleration Frequency Spectrum PSD')
    plt.legend()


   

    plt.tight_layout()
    # plt.show()
    
    """""""""""""""""""""""""""""
    " Plot frequency values     "
    """""""""""""""""""""""""""""

    

    '''
    Note : //  floor division operator - divides the number on the left by the number on the right and rounds down to the nearest whole number
    [:N//2] - from the first element to the middle one.
    '''

    # Create a new figure for the frequency-domain plots
    plt.figure(figsize=(12, 8))

    # Plot Fourier Transforms
    plt.subplot(2, 1, 1)
    '''
    Amplitude spectrum transformation of the FFT (2.0/N * yf) 
    '''
    

    plt.plot(time_s, gx, label='Gx', color='r')
    plt.plot(time_s, gy, label='Gy', color='g')
    plt.plot(time_s, gz, label='Gz', color='b')
    plt.xlabel('Time [s]')
    plt.ylabel('Angular Velocity [degrees/s***]')
    plt.title('Angular Velocity vs Time')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(xf, 2.0/N * np.abs(yf_gx[:N//2]), label='Gx', color='r')
    plt.plot(xf, 2.0/N * np.abs(yf_gy[:N//2]), label='Gy', color='g')
    plt.plot(xf, 2.0/N * np.abs(yf_gz[:N//2]), label='Gz', color='b')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude')
    plt.title('Angular Velocity Frequency Spectrum')
    plt.legend()

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

    print(f"---------------------{file_name}-----------------------------")
    print(f"Sample frequency = {fs:.2f} [Hz] \nPeriod = {T:.5f} [s]")
    # Show plot
    plt.show()

    


if __name__ == '__main__':
    main(sys.argv)
