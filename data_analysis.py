import time
import os
import argparse
import subprocess

import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
import matplotlib.mlab as mlab
from scipy.optimize import curve_fit
from pypcd4 import PointCloud

def load_point_clouds(directory):
    ''' It gets only pcd points from a specific time frame '''
    zero_time = 1722001459.792622566
    start_time = zero_time + 137 # 137
    end_time = zero_time + 160 # 160

    print(f'zero time = {zero_time} ')
    print(f'start time = {start_time} ')
    print(f'end time = {end_time} ')

    point_clouds = []

    # Loop through the files in the directory
    for file_name in os.listdir(directory):
        # Check if the file is a PCD file and starts with a number in the specified range
        if file_name.endswith(".pcd"):
            try:
                prefix = float(file_name.split('.')[0])
                if start_time <= prefix <= end_time:
                    file_path = os.path.join(directory, file_name)
                    pcd = o3d.io.read_point_cloud(file_path)
                    # pcd_down = pcd.voxel_down_sample()
                    point_clouds.append(pcd)
            except ValueError:
                # If the file name does not start with a valid number, skip it
                continue


    print(f"Loaded {len(point_clouds)} scans!")
    return point_clouds

def crop_pcd_files_within_interval(direction=0,time=5,directory="/home/sqdr/Desktop/unilidar_proj/tool_manipulating_point_cloud/pcd/P23_71.9_vert"):
    
    # get first and last time
    file_names = [f for f in os.listdir(directory) if f.endswith(".pcd")]
    # print(f'debug file names: {file_names}')
    sorted_file_names = sorted(file_names)     # Sort filenames in ascending order
    # print(f'sorted file names: {sorted_file_names}')
    first_file = sorted_file_names[0]
    last_file = sorted_file_names[-1]
    zero_time = int(first_file.split('.')[0]) # name of the first file
    final_time = int(last_file.split('.')[0]) # name of the last file - pcd
    # start_time = zero_time + 138 # 137
    # end_time = zero_time + 145 # 160

    if direction == 0:
        # decreasing order
        start_time = final_time
        final_time = final_time - time
    elif direction == 1:
        start_time = zero_time
        final_time = zero_time + time

    print(f'zero time = {zero_time} ')
    print(f'start time = {start_time} ')
    print(f'final time = {final_time} ')

    point_clouds = [] # list of pointclouds in the selected time interval

    # Loop through the files in the directory
    for file_name in os.listdir(directory):
        # Check if the file is a PCD file and starts with a number in the specified range
        if file_name.endswith(".pcd"):
            try:
                prefix = float(file_name.split('.')[0])

                if direction == 1:
                    # print("[debug] on monte")
                    # crescent order
                    if start_time <= prefix <= final_time:
                        # Construct the full file path
                        file_path = os.path.join(directory, file_name)
                        point_clouds.append(file_path)
                elif direction == 0:
                    # print("[debug] on descend")
                    # decrescent order
                    if final_time <= prefix <= start_time:
                        file_path = os.path.join(directory, file_name)
                        point_clouds.append(file_path)
            except ValueError:
                # If the file name does not start with a valid number, skip it
                continue
       

    return point_clouds

def merge_points(pcd_paths,save_pcd_file_as):
    pcd_combined = o3d.geometry.PointCloud()
    for point_id in range(len(pcd_paths)):
        current_pcd = o3d.io.read_point_cloud(pcd_paths[point_id])
        # pcds[point_id].transform(pose_graph.nodes[point_id].pose) #TODO
        pcd_combined += current_pcd
        # print("je combine")
    o3d.io.write_point_cloud(save_pcd_file_as,pcd_combined)
    # o3d.visualization.draw_geometries_with_editing([pcd_combined_down])

    return pcd_combined

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

def plot_point_cloud_with_plane(ply_file, a, b, c, d):
    ply_directory = os.path.dirname(ply_file)
    file_name, file_extension = os.path.splitext(os.path.basename(ply_file))
    print(f'---------- {file_name}---------------------')

    print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")
    D = (np.abs(d))/np.sqrt(a**2+b**2+c**2)
    print(f"Distance LiDAR to the plane : {D:.2f} meters ")
    
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
    ax.set_title(f'Plane a = {a:.2f}, b = {b:.2f}, c = {c:.2f}, d = {d:.2f} \n fit on {file_name} \n Distance to lidar = {D:.2f}')
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

    #plt.show()
    

# Define the Gaussian function
def gaussian(x, mu, sigma):
    return norm.pdf(x, mu, sigma)

def calculate_gaussian_noise(ply_file, a, b, c, d):
    ply_directory = os.path.dirname(ply_file)
    file_name, file_extension = os.path.splitext(os.path.basename(ply_file))

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

        print(f"Fitted mean distance of points to the plane: {mu_fitted:.4f} centimetres")
        print(f"Fitted standard deviation (noise) of distances: {sigma_fitted:.4f}")
        print(f"(Previous guessed standard deviation (noise) of distances: {np.std(distances_cm):.4f})")

        # Plot the distances and the fitted Gaussian
        plt.figure(figsize=(10, 6))
        plt.hist(distances_cm, bins=bins, edgecolor='black', density=True, alpha=0.6, label='Histogram of distances')

        # Plot the guess Gaussian curve
        x = np.linspace(np.min(distances_cm), np.max(distances_cm), 1000)
        p = gaussian(x, np.mean(distances_cm), np.std(distances_cm))
        plt.plot(x, p, 'r--', linewidth=3, label=f'Guessed Gaussian \n \u03C3 = {np.std(distances_cm):.2f} \n \u03BC = {np.mean(distances_cm):.2f} ')

        # Plot the fitted Gaussian curve
        p = gaussian(x, mu_fitted, sigma_fitted)
        plt.plot(x, p, 'g--', linewidth=3, label=f'Fitted Gaussian \n \u03C3 = {sigma_fitted:.2f} \n \u03BC = {mu_fitted:.2f} ')

        plt.title(f'{file_name}')
        plt.xlabel('Distance (cm)')
        plt.ylabel('Density')
        plt.legend()
        plt.grid(True)
        base_name, extension = os.path.splitext(ply_file)
        plt.show()

    else:
        print("No points within the specified threshold.")


# TODO initialize folder structure

# ---------------- BAG to PCD -------------------------
'''
1; Read all files in the folder named ".bag.active" and save their names (excluding the .bag extension) into a list.
2. Create a folder for each of these filenames inside the "pcd" directory.
3. Run a command for each filename in the list using the subprocess module.
'''

bag_folder = '/home/ws/src/point_lio_ws/data_filtering/data/21_august_fill_empty_values_ratio_graph_outdoors'
bag_reindexed_folder = '/home/ws/src/point_lio_ws/data_filtering/data/21_august_fill_empty_values_ratio_graph_outdoors/reindexed'
pcd_directory = '/home/sqdr/ROSDOCKER/noetic/src/point_lio_ws/data_filtering/data/21_august_fill_empty_values_ratio_graph_outdoors/pcd'
pcd_combined_folder = '/home/sqdr/ROSDOCKER/noetic/src/point_lio_ws/data_filtering/data/21_august_fill_empty_values_ratio_graph_outdoors/pcd_combined'
ply_directory = "/home/sqdr/ROSDOCKER/noetic/src/point_lio_ws/data_filtering/data/21_august_fill_empty_values_ratio_graph_outdoors/ply"


# file_names = [f for f in os.listdir(bag_folder) if f.endswith('.bag.active')] 
# file_names_without_extension = [f.replace('.bag.active', '') for f in file_names]

# for name in file_names_without_extension:
#     f_path_full = os.path.join(bag_folder, name + '.bag.active') 
#     f_path_bag_reindexed= os.path.join(bag_reindexed_folder, name + '.bag.active')
#     pcd_file_path = os.path.join(pcd_directory,name)
    
#     cmd_reindex_n_fix = f'''source /opt/ros/noetic/setup.bash && rosbag reindex --output-dir={bag_reindexed_folder} {f_path_full} '''
#     cmd_convert = f'''source /opt/ros/noetic/setup.bash && rosrun pcl_ros bag_to_pcd {f_path_bag_reindexed} /unilidar/cloud {os.path.join(pcd_file_path)}'''
#     try:
#         subprocess.run(cmd_reindex_n_fix, shell=True, check=True, executable='/bin/bash')
#         subprocess.run(cmd_convert, shell=True, check=True, executable='/bin/bash')
        
#     except subprocess.CalledProcessError as e:
#         print(f"Error running command for {name}: {e}")
    
# print("All .bag converted to .pcd successfully.")

# ----------------  Multiple PCDs to  Combined PCD -------------------------

'''
Fuse diferent frames 
'''

# pcd_directories= [f for f in os.listdir(pcd_directory)] 
# # file_names_without_extension = [f.replace('.bag.active', '') for f in file_names]

# # list of pcds to PCD combined
# pcd_combined_path_list = []

# for pcd_data in pcd_directories:
#     file_names = [f for f in os.listdir(os.path.join(pcd_directory,pcd_data)) ]
#          # print(f'debug file names: {file_names}')
#     selected_frames =  crop_pcd_files_within_interval(direction=0,time=5,directory=os.path.join(pcd_directory,pcd_data))

#     point_clouds = []
#     for frame in selected_frames:
#         try: 
#             pc = PointCloud.from_path(frame)
#             array = pc.numpy(("x", "y", "z", "intensity"))
#             point_clouds.append(PointCloud.from_xyzi_points(array))
#         except Exception as e:
#             print(f"Failed to process {frame}: {e}")

#     # Fuse all point clouds
#     if point_clouds:
#         fused_pc = point_clouds[0]
#         for pc in point_clouds[1:]:
#             fused_pc += pc
#     else:
#         raise ValueError("No PCD files found in the specified folder.")

#     # Print fields of the combined point cloud
#     print(f"Current fields in .pcd : {fused_pc.fields}.")
#     print("Wait the pcd's are still being combined")
#     # array =  fused_pc.numpy()
#     parent_dir = os.path.dirname(pcd_data)
#     output_path = os.path.join(pcd_combined_folder, pcd_data + '.pcd')
#     try:
#         fused_pc.save(output_path)
#         print(f"Combined PCD file saved to {output_path}")
#     except Exception as e:
#         print(f"Failed to save the combined PCD file: {e}")
    
# print(f"combined pcd : {pcd_combined_path_list}")



# ------------------------ MANUAL CROP ----------------------------------
# '''
# TOdooo
# '''

# pcd_combined_folder_files= [f for f in os.listdir(pcd_combined_folder)] 
# print(pcd_combined_folder_files)
# for pcd_combined_file in pcd_combined_folder_files:
#     pcd = o3d.io.read_point_cloud(os.path.join(pcd_combined_folder,pcd_combined_file))
#     print(f'Currently selecting : {pcd_combined_file}. Copy this name before saving it as .ply in the correct directory {ply_directory}')
#     o3d.visualization.draw_geometries_with_editing([pcd])

# print("Finished cropping all the selected data.")

# -------------------- FIND PLANE and PLOT Noise distribution ------------------------------

############## Example for a whole folder:
ply_files = [f for f in os.listdir(ply_directory)] 
print(ply_files)
for ply_file in ply_files:
    ply_file_name = os.path.join(ply_directory,ply_file)
    ply = o3d.io.read_point_cloud(ply_file_name)
    # ply_file_name = "ply/P23_71.9_vert.ply"
    # ply = o3d.io.read_point_cloud("ply/P23_71.9_vert.ply")
    print(ply)

    # Segment the plane TODO - change name of graph
    plane_model, inliers = ply.segment_plane(distance_threshold=0.02, ransac_n=3, num_iterations=100) # 0.02 = 2 cm
    [a, b, c, d] = plane_model
    print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")
    plot_point_cloud_with_plane(ply_file_name, a, b, c, d)
    calculate_gaussian_noise(ply_file_name, a, b, c, d)  # Threshold is 1 cm

# ############## Example for a single file:
# ply_path = "data/filtered_data/ply/72.7parking_contre_solei_blanche_74.7_2024-08-02-07-53-28.ply"
# ply_directory = os.path.dirname(ply_path)
# file_name, file_extension = os.path.splitext(os.path.basename(ply_path))

# ply = o3d.io.read_point_cloud(ply_path)
# # Threshold at 2 meters so it wont filter any points, as the planes are already croped
# plane_model, inliers = ply.segment_plane(distance_threshold=2, ransac_n=3, num_iterations=100) 
# [a, b, c, d] = plane_model
# plot_point_cloud_with_plane(ply_path, a, b, c, d)
# calculate_gaussian_noise(ply_path, a, b, c, d)  # Threshold is 1 cm

#ref next approach
#ref como talvez usa pose graph https://www.open3d.org/docs/latest/tutorial/Advanced/multiway_registration.html