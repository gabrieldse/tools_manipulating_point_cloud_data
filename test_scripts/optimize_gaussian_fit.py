import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.optimize import curve_fit
import os
import glob

# Define the Gaussian function
def gaussian(x, mu, sigma):
    return norm.pdf(x, mu, sigma)

def calculate_gaussian_noise(ply_file, a, b, c, d):
    # Load the point cloud
    pcd = o3d.io.read_point_cloud(ply_file)
    points = np.asarray(pcd.points)

    # Compute distances from the plane
    distances = (a * points[:, 0] + b * points[:, 1] + c * points[:, 2] + d) / np.sqrt(a**2 + b**2 + c**2)
    distances_cm = distances * 100



    # Compute the Gaussian noise
    if len(distances_cm) > 0:
        bins = 100

        # Histogram of distances
        counts, bin_edges = np.histogram(distances_cm, bins=bins, density=True)
        bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

        # Fit the Gaussian function to the histogram
        popt, pcov = curve_fit(gaussian, bin_centers, counts, p0=[np.mean(distances_cm), np.std(distances_cm)])
        mu_fitted, sigma_fitted = popt
        
        print(f"Fitted mean distance to the plane: {mu_fitted:.4f} centimetres")
        print(f"Fitted standard deviation (noise) of distances: {sigma_fitted:.4f}")

        # Plot the distances and the fitted Gaussian
        plt.figure(figsize=(10, 6))
        plt.hist(distances_cm, bins=bins, edgecolor='black', density=True, alpha=0.6, label='Histogram of distances')

        # Plot the guess Gaussian curve
        x = np.linspace(np.min(distances_cm), np.max(distances_cm), 1000)
        p = gaussian(x, np.mean(distances_cm), np.std(distances_cm))
        plt.plot(x, p, 'r--', linewidth=3, label='Fitted Gaussian')

        # Plot the fitted Gaussian curve
        p = gaussian(x, mu_fitted, sigma_fitted)
        plt.plot(x, p, 'g--', linewidth=3, label='Fitted Gaussian')

        plt.title(f'{ply_file}')
        plt.xlabel('Distance (cm)')
        plt.ylabel('Density')
        plt.legend()
        plt.grid(True)
        base_name, extension = os.path.splitext(ply_file)
        plt.show()

    else:
        print("No points within the specified threshold.")

def plot_point_cloud_with_plane(ply_file, a, b, c, d):
    print(f'---------- {ply_file}---------------------')
    
    # Load the point cloud using Open3D
    pcd = o3d.io.read_point_cloud(ply_file)
    points = np.asarray(pcd.points)

    # Create a new figure for plotting
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Plot the point cloud
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], c='b', marker='o', s=1)

    # Define the grid for the plane
    x = np.linspace(np.min(points[:, 0]), np.max(points[:, 0]), 100)
    y = np.linspace(np.min(points[:, 1]), np.max(points[:, 1]), 100)
    X, Y = np.meshgrid(x, y)
    Z = (-d - a * X - b * Y) / c

    # Plot the plane
    ax.plot_surface(X, Y, Z, color='r', alpha=0.5)

    # Set labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Equalize the aspect ratio
    max_range = np.array([points[:, 0].max() - points[:, 0].min(), 
                          points[:, 1].max() - points[:, 1].min(),
                          points[:, 2].max() - points[:, 2].min()]).max()
    mid_x = 0.5 * (points[:, 0].max() + points[:, 0].min())
    mid_y = 0.5 * (points[:, 1].max() + points[:, 1].min())
    mid_z = 0.5 * (points[:, 2].max() + points[:, 2].min())
    
    ax.set_xlim(mid_x - max_range / 2, mid_x + max_range / 2)
    ax.set_ylim(mid_y - max_range / 2, mid_y + max_range / 2)
    ax.set_zlim(mid_z - max_range / 2, mid_z + max_range / 2)

    plt.show()

def process_files_in_folder(folder_path, a, b, c, d):
    # Get a list of all .ply files in the folder
    ply_files = glob.glob(os.path.join(folder_path, "*.ply"))

    # Loop through each file and process it
    for ply_file in ply_files:
        print(f'Processing file: {ply_file}')
        calculate_gaussian_noise(ply_file, a, b, c, d)
        plot_point_cloud_with_plane(ply_file, a, b, c, d)

# Example usage:
# file_path = "/home/sqdr/ROSDOCKER/noetic/src/point_lio_ws/data_filtering/data/filtered_data/ply/blanche_ombre_11.0_2024-08-02-07-56-08.ply"
# a, b, c, d = 1, 1, 1, -10  # Example plane coefficients
# calculate_gaussian_noise(file_path, a, b, c, d)
# plot_point_cloud_with_plane(file_path, a, b, c, d)

# Example for a folder:
# Define the folder path and plane coefficients
folder_path = "/home/sqdr/ROSDOCKER/noetic/src/point_lio_ws/data_filtering/data/filtered_data/ply"
a, b, c, d = 1, 1, 1, -10  # Example plane coefficients

# Call the function to process all files in the folder
process_files_in_folder(folder_path, a, b, c, d)
