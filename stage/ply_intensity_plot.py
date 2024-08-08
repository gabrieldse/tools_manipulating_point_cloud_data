# import open3d as o3d
# import numpy as np

# Load the point cloud
#pcd = o3d.io.read_point_cloud("/home/sqdr/ROSDOCKER/noetic/src/point_lio_ws/data_filtering/filtered_data/ply/72.7parking_contre_solei_blanche_74.7_2024-08-02-07-53-28.ply")

# pcd = o3d.io.read_point_cloud("/home/sqdr/ROSDOCKER/noetic/src/point_lio_ws/data_filtering/filtered_data/pcd/72.7parking_contre_solei_blanche_74.7_2024-08-02-07-53-28/1722585213.509805441.pcd")

# # Check if the point cloud has intensity data
# if not hasattr(pcd, 'color'):
#     raise ValueError("The loaded PCD file does not contain intensity data.")

# # Extract intensity data (assuming intensity data is stored as an additional field)
# intensity = np.asarray(pcd.intensities)  # Replace 'intensities' with the correct attribute if needed

# # Normalize intensity to [0, 1] for visualization
# intensity_normalized = (intensity - np.min(intensity)) / (np.max(intensity) - np.min(intensity))

# # Create colors based on intensity
# colors = np.zeros((len(intensity), 3))
# colors[:, 0] = intensity_normalized  # Red channel
# colors[:, 1] = 0  # Green channel
# colors[:, 2] = 0  # Blue channel

# # Set colors to the point cloudin
# pcd.colors = o3d.utility.Vector3dVector(colors)

# # Visualize the point cloud
# o3d.visualization.draw_geometries([pcd], window_name="Point Cloud with Intensity")



# print(np.asarray(pcd.points))
# print(np.asarray(pcd.colors))
# # # List all attributes and methods
# print("Attributes and methods using dir():")
# print(dir(pcd))

# # Get detailed information
# print("\nDetailed information using help():")
# help(pcd)


# # Compute intensity (example: distance from origin)
# points = np.asarray(pcd.points)
# intensity = np.linalg.norm(points, axis=1)

# # Normalize intensity to [0, 1]
# intensity_normalized = (intensity - np.min(intensity)) / (np.max(intensity) - np.min(intensity))

# # Create colors based on intensity
# colors = np.zeros_like(points)
# colors[:, 0] = intensity_normalized  # Red channel
# colors[:, 1] = 0  # Green channel
# colors[:, 2] = 0  # Blue channel

# # Set colors to the point cloud
# pcd.colors = o3d.utility.Vector3dVector(colors)

# # Visualize the point cloud
# o3d.visualization.draw_geometries([pcd], window_name="Point Cloud with Intensity")


import open3d as o3d
import numpy as np
import os

def combine_point_clouds_with_intensity(pcd_paths, save_pcd_file_as):
    pcd_combined = o3d.geometry.PointCloud()

    # Initialize lists to hold combined points and intensities
    combined_points = []
    combined_intensities = []

    for pcd_path in pcd_paths:
        # Read the current point cloud
        current_pcd = o3d.io.read_point_cloud(pcd_path)

        # Extract points and intensities
        points = np.asarray(current_pcd.points)
        intensities = np.asarray(current_pcd.colors)[:, 0]  # Assuming intensity is stored in color's red channel

        # Append points and intensities
        combined_points.append(points)
        combined_intensities.append(intensities)

    # Concatenate all points and intensities
    combined_points = np.vstack(combined_points)
    combined_intensities = np.concatenate(combined_intensities)

    # Create a new point cloud and assign the combined points
    pcd_combined.points = o3d.utility.Vector3dVector(combined_points)

    # Handle intensity. Here, simply taking the average intensity for overlapping points.
    if combined_intensities.size > 0:
        # Assuming intensity is stored in the color channels (RGB)
        combined_colors = np.zeros((combined_points.shape[0], 3))
        combined_colors[:, 0] = combined_intensities  # Assuming intensity in red channel
        combined_colors[:, 1] = combined_intensities  # Replicate for green and blue channels if needed
        combined_colors[:, 2] = combined_intensities
        pcd_combined.colors = o3d.utility.Vector3dVector(combined_colors)

    # Save the combined point cloud
    o3d.io.write_point_cloud(save_pcd_file_as, pcd_combined)

    return pcd_combined

pcd_directory = "/home/ws/src/point_lio_ws/test/pcd"
file_names_with_path = []
file_names_array = [f for f in os.listdir(pcd_directory)] 
for file_name in file_names_array:
    file_name_with_path = os.path.join(pcd_directory,file_name)
    file_names_with_path.append(file_name_with_path)

combine_point_clouds_with_intensity(file_names_with_path,os.path.join(pcd_directory,"combined.pcd"))