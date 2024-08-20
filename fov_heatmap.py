import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

def calculate_fov(file_path, nscans, threshold, show_plots):
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
        print(f"Completed scan {j}/{nscans} scans. {j/10}/{nscans/10} [seconds]")
        
        current_scan_point += 2160

    # Apply threshold
    fov_2d_array[fov_2d_array < threshold] = 0

    # Save array to csv
    df = pd.DataFrame(fov_2d_array)
    df.to_csv("fov_2D_array.csv", header=False, index=False)
    cropped_fov_array = fov_2d_array[120:220, 600:750]
    cropped_df = pd.DataFrame(cropped_fov_array)
    cropped_df.to_csv("cropped_fov_2D_array.csv", header=False, index=False)

    # Plot the 2D array if show_plots is True
    if show_plots:
        plt.figure()
        plt.imshow(fov_2d_array, cmap='hot')
        plt.colorbar()
        plt.title(f'Final plot after {nscans/10} seconds')
        
        # Plot the FOV coverage
        plt.figure()
        plt.plot(np.linspace(1, nscans/10,len(fov_per)), fov_per)
        plt.title(f'FOV coverage after {len(fov_per)/10} seconds')
        plt.xlabel('Seconds ')
        plt.ylabel('Coverage [%]')
        plt.grid()
        plt.ylim(0, 100)
        plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process scan data and plot results.')
    parser.add_argument('file_path', type=str, help='Path to the CSV file containing the data')
    parser.add_argument('nscans', type=int, help='Number of scans to process')
    parser.add_argument('--threshold', type=float, default=0, help='Threshold for the 2D array')
    parser.add_argument('--no_plot', action='store_true', help='Do not display plots')

    args = parser.parse_args()
    
    # Determine if plotting should be shown
    show_plots = not args.no_plot

    calculate_fov(args.file_path, args.nscans, args.threshold, show_plots)
