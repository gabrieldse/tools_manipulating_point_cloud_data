import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

'''
A 2D array representing a 360° x 90° field of view with a 5 mrad x 5 mrad grid resolution. (1 mrad = 1 milliradian = an angle where the arc length is 1/1000th of the radius of the circle.)
to generate a graph to compare with the LIVOX graph
(https://www.livoxtech.com/3296f540ecf5458a8829e01cf429798e/downloads/Point%20cloud%20characteristics.pdf) graph
'''

'''
arc length = theta x radius
interval = circuference lenght / arc lenght 
360 = 2 pi rad 
    -> 2pi/5mrad = 1256,67 intervals
90 = pi / 2 rad 
    -> pi/2/5mrad = 314,16 intervals
'''

def process_data(file_path, nscans, threshold):
    # Read the CSV file
    scan_points_total = 2160 * nscans
    df = pd.read_csv(file_path, delimiter=',', nrows=scan_points_total)
    azimuth = df["azimuth"]
    zenith = df["zenith"]

    # Define the dimensions of the 2D array
    rows, cols = int(314.16), int(1256.67)  # reasonable values

    # Initialize variables
    fov_per = []
    fov_2d_array = np.zeros((rows, cols))
    number = 0

    # Process each scan
    current_scan_point = 0
    for j in range(1, nscans + 1):  # Number of scans
        for i in range(current_scan_point, current_scan_point + 2160):  # Number of points per scan
            # Correct zenith values
            if zenith[i] > 90:
                zenith[i] -= 90

            pixel_v = int(zenith[i] / 90 * rows)
            pixel_h = int(azimuth[i] / 360 * cols)

            # Update the 2D array
            if 0 <= pixel_v < rows and 0 <= pixel_h < cols:
                fov_2d_array[pixel_v, pixel_h] += 1
        
        # Calculate the percentage coverage
        number = np.sum(fov_2d_array > 0)
        last_fov_per = number / (rows * cols) * 100
        fov_per.append(last_fov_per)
        print(f"Completed scan {j}/{nscans}")
        
        current_scan_point += 2160

    # Apply threshold
    fov_2d_array[fov_2d_array < threshold] = 0

    # Plot the 2D array
    plt.figure()
    plt.imshow(fov_2d_array, cmap='hot')
    plt.colorbar()
    plt.title(f'Final plot after {nscans} scans')
    
    # Plot the FOV coverage
    plt.figure()
    plt.plot(range(1, len(fov_per) + 1), fov_per)
    plt.title(f'FOV coverage after {len(fov_per)} scans')
    plt.xlabel('Scan Index')
    plt.ylabel('Coverage [%]')
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process scan data and plot results.')
    parser.add_argument('file_path', type=str, help='Path to the CSV file containing the data')
    parser.add_argument('nscans', type=int, help='Number of scans to process')
    parser.add_argument('--threshold', type=float, default=0, help='Threshold for the 2D array')
    
    args = parser.parse_args()
    
    process_data(args.file_path, args.nscans, args.threshold)


