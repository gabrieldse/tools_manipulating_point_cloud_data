import time
import os
import argparse
import subprocess

import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt


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

def crop_bag_time_clouds(direction=0,time=5,directory="/home/sqdr/Desktop/unilidar_proj/tool_manipulating_point_cloud/pcd/P23_71.9_vert"):
    zero_time = 1722585852.499159336 # name of the first file
    final_time = 1722585928.234170198 # name of the last file - pcd
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

# 0.0001 = 1/10 mm
def calculate_gaussian_noise(ply_file, a, b, c, d, threshold=1):
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
        print(f"Mean distance to the plane: {100*mean_distance:.4f} centimetres")
        print(f"Standard deviation (noise) of distances: {100*std_distance:.4f} centimetres")

        # Plot the distances
        plt.figure(figsize=(10, 6))
        plt.hist(distances*100, bins=200, edgecolor='black',density=True)
        plt.title('Distance distribution to the plane at 1m. Scans 137-147 ')
        plt.xlabel('Distance (cm)')
        plt.ylabel('Number of Points')
        plt.grid(True)
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

bag_folder = 'filtered_data/bag'
bag_reindexed_folder = 'filtered_data/bag/reindexed'
pcd_folder = 'filtered_data/pcd'


file_names = [f for f in os.listdir(bag_folder) if f.endswith('.bag.active')] 
file_names_without_extension = [f.replace('.bag.active', '') for f in file_names]

for name in file_names_without_extension:
    f_path_full = os.path.join(bag_folder, name + '.bag.active') 
    f_path_bag_reindexed= os.path.join(bag_reindexed_folder, name + '.bag.active')
    pcd_file_path = os.path.join(pcd_folder,name)
    
    cmd_reindex_n_fix = f'''source /opt/ros/noetic/setup.bash && rosbag reindex --output-dir={bag_reindexed_folder} {f_path_full} '''
    cmd_convert = f'''source /opt/ros/noetic/setup.bash && rosrun pcl_ros bag_to_pcd {f_path_bag_reindexed} /unilidar/cloud {os.path.join(pcd_file_path,name)}'''
    try:
        subprocess.run(cmd_reindex_n_fix, shell=False, check=True, executable='/bin/bash')
        subprocess.run(cmd_convert, shell=False, check=True, executable='/bin/bash')
        
    except subprocess.CalledProcessError as e:
        print(f"Error running command for {name}: {e}")
    
print("All commands executed.")

# ---------------- PCD  to PLY -------------------------

# list of pcds to PCD combined
pcd_paths =  crop_bag_time_clouds(0,5,"/home/sqdr/Desktop/unilidar_proj/tool_manipulating_point_cloud/pcd/P23_71.9_vert")
print(pcd_paths)
save_pcd_file_as="/home/sqdr/Desktop/unilidar_proj/tool_manipulating_point_cloud/pcd/vertical_P23_71.9_KLX.pcd"
pcd_combined = merge_points(pcd_paths,save_pcd_file_as)
print(f"pcd_combined : {pcd_combined}")

# To manual crop:
# pcd = o3d.io.read_point_cloud("/home/sqdr/Desktop/unilidar_proj/tool_manipulating_point_cloud/pcd/vertical_P23_71.9_KLX.pcd")
# o3d.visualization.draw_geometries_with_editing([pcd_combined])

# re coppy the name of the pcd to save the file
# remove the path_ply/same_name.json

# -------------------- FIND PLANE and PLOT Noise distribution ------------------------------
            # ply_file_name = "ply/P23_71.9_vert.ply"
            # ply = o3d.io.read_point_cloud("ply/P23_71.9_vert.ply")
            # print(ply)

            # # Segment the plane TODO - change name of graph
            # plane_model, inliers = ply.segment_plane(distance_threshold=0.02, ransac_n=5, num_iterations=100)

            # [a, b, c, d] = plane_model
            # print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")
            # plot_point_cloud_with_plane(ply_file_name, a, b, c, d)
            # calculate_gaussian_noise(ply_file_name, a, b, c, d, threshold=1)  # Threshold is 1 cm

#ref next approach
#ref como talvez usa pose graph https://www.open3d.org/docs/latest/tutorial/Advanced/multiway_registration.html