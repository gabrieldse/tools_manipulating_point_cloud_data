import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import argparse

def plot_point_cloud_with_plane(ply_file, a, b, c, d):
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

def calculate_gaussian_noise(ply_file, a, b, c, d, threshold=0.01):
    # Load the point cloud
    pcd = o3d.io.read_point_cloud(ply_file)
    points = np.asarray(pcd.points)

    # Compute distances from the plane
    distances_abs = np.abs(a * points[:, 0] + b * points[:, 1] + c * points[:, 2] + d) / np.sqrt(a**2 + b**2 + c**2)
    distances = (a * points[:, 0] + b * points[:, 1] + c * points[:, 2] + d) / np.sqrt(a**2 + b**2 + c**2)

    # Filter points within 1 cm (0.01 meters) of the plane
    within_threshold = distances_abs < threshold
    points_within_threshold = points[within_threshold]
    distances_within_threshold = distances_abs[within_threshold]

    # Compute the Gaussian noise
    if len(distances_within_threshold) > 0:
        mean_distance = np.mean(distances_within_threshold)
        std_distance = np.std(distances_within_threshold)
        print(f"Mean distance to the plane: {mean_distance:.4f} meters")
        print(f"Standard deviation (noise) of distances: {std_distance:.4f} meters")

        # Plot the distances
        plt.figure(figsize=(10, 6))
        plt.hist(distances*100, bins=200, edgecolor='black')
        plt.title('Distance distribution to the plane at 1m. Scans 137-147 ')
        plt.xlabel('Distance (cm)')
        plt.ylabel('Number of Points')
        plt.grid(True)
        plt.show()

    else:
        print("No points within the specified threshold.")

# Example usage
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plots a point cloud and a specified plane. And calculate the distance distribution to this plane')
    parser.add_argument('file_name', type=str, help='The path to the point cloud file (e.g., plane_1m.ply)')
    args = parser.parse_args()
    # ply_file = "plane_1m.ply"  # Replace with your .ply file path
    # a, b, c, d = 1, -0.06, -0.05, -0.90  # Replace with your plane coefficients 137 - 147 values
    a, b, c, d = 1, -0.05, -0.07, -0.90  # Replace with your plane coefficients
    plot_point_cloud_with_plane(args.file_name, a, b, c, d)
    calculate_gaussian_noise(args.file_name, a, b, c, d, threshold=0.01)  # Threshold is 1 cm
