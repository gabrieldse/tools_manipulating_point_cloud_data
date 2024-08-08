from pypcd4 import PointCloud
import numpy as np
import os
import matplotlib.pylab as plt
import matplotlib.colors as mcolors
from mpl_toolkits.mplot3d import Axes3D


################" FUSE
# folder_path = "/home/sqdr/ROSDOCKER/noetic/src/point_lio_ws/data_filtering/filtered_data/pcd/same_mirroir_2024-08-02-07-54-40"
# pcd_files = [f for f in os.listdir(folder_path) if f.endswith('.pcd')]
# point_clouds = []

# # Load all PCD files and convert to numpy arrays
# for pcd_file in pcd_files:
#     file_path = os.path.join(folder_path, pcd_file)
#     pc = PointCloud.from_path(file_path)
#     array = pc.numpy(("x", "y", "z", "intensity"))
#     point_clouds.append(PointCloud.from_xyzi_points(array))

# # Fuse all point clouds
# if point_clouds:
#     fused_pc = point_clouds[0]
#     for pc in point_clouds[1:]:
#         fused_pc += pc
# else:
#     raise ValueError("No PCD files found in the specified folder.")

# # Print fields of the combined point cloud
# print(fused_pc.fields)
# array =  fused_pc.numpy()
# name = "soleil mirroir.pcd"
# pc.save(os.path.join("/home/sqdr/ROSDOCKER/noetic/src/point_lio_ws/data_filtering/stage",name))

##################################################"" GET THE COLOR SCHEME
point_index = 243
file1 = "/home/sqdr/ROSDOCKER/noetic/src/point_lio_ws/data_filtering/stage/ombre blanc.pcd"
file2 = "/home/sqdr/ROSDOCKER/noetic/src/point_lio_ws/data_filtering/stage/ombre mirroir.pcd"
file3 = "/home/sqdr/ROSDOCKER/noetic/src/point_lio_ws/data_filtering/stage/solei blanc.pcd"
file4 = "/home/sqdr/ROSDOCKER/noetic/src/point_lio_ws/data_filtering/stage/soleil mirroir.pcd"


# pc = PointCloud.from_path(file4)
# array = pc.numpy()
# intensity = array[point_index, 3]  # Assuming intensity is the 4th field
# print(f"Intensity of point at index {point_index}: {intensity}")


##########################"" PLOT 

# Path to the folder containing PCD files
folder_path = "/home/sqdr/ROSDOCKER/noetic/src/point_lio_ws/data_filtering/stage/"

# List of PCD files in the folder
pcd_files = [f for f in os.listdir(folder_path) if f.endswith('.pcd')]
file_paths_array = [os.path.join(folder_path, pcd_file) for pcd_file in pcd_files]

# Print the list of files
print("PCD files:", pcd_files)

# Create a figure for all plots
fig = plt.figure(figsize=(15, 10))

# Loop over all file paths
for idx, file_path in enumerate(file_paths_array):
    # Load the point cloud
    pc = PointCloud.from_path(file_path)
    
    # Convert to NumPy array
    array = pc.numpy()  # Assuming this includes columns for x, y, z, and intensity

    # Extract individual arrays
    x = array[:, 0]
    y = array[:, 1]
    z = array[:, 2]
    intensity = array[:, 3]

    # Create a 3D scatter plot
    ax = fig.add_subplot(2, 2, idx + 1, projection='3d')  # Adjust subplot grid size as needed

    # Scatter plot with color mapping based on intensity
    sc = ax.scatter(x, y, z, c=intensity, cmap='viridis', s=10)  # Adjust the `s` parameter for point size

    # Add a color bar
    fig.colorbar(sc, ax=ax, label='Intensity')

    # Add labels and title
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'{pcd_files[idx]}')

# Adjust layout and show plot
plt.tight_layout()
plt.show()
