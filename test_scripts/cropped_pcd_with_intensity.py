import os
import numpy as np
import open3d as o3d
from pypcd4 import PointCloud


def intensity_to_color(intensity_array):
    # Normalize intensity values to the range [0, 1]
    normalized_intensity = np.clip(intensity_array / 255.0, 0, 1)
    # Repeat the normalized intensity values across 3 channels (R, G, B) to get grayscale colors
    colors = np.repeat(normalized_intensity[:, np.newaxis], 3, axis=1)
    return colors

# Load all PCD files and convert to numpy arrays
folder_path = "/home/sqdr/ROSDOCKER/noetic/src/data_lidar/filtered_data/2AUG_parking/pcd_combined_with_intensity"
output_file = "test.pcd"
ply_path = "/home/sqdr/ROSDOCKER/noetic/src/data_lidar/data_filtering_scripts/test_scripts/cropped.ply"
pcd_files = [f for f in os.listdir(folder_path) if f.endswith('.pcd')]
point_clouds = []

for pcd_file in pcd_files:
    file_path = os.path.join(folder_path, pcd_file)
    try:
        '''
        load combined pcd, assign the 0-255 to the RBG channels, crop it in the interactive mode
        '''
        print(f"Cropping this file: {pcd_file}")
        pc = PointCloud.from_path(file_path)
        pc_open = o3d.io.read_point_cloud(file_path)
        array = pc.numpy(("x", "y", "z", "intensity"))
        intensity = array[:,3]
        colors = intensity_to_color(intensity)
        colors = colors.astype(np.float64)
        pc_open.colors = o3d.utility.Vector3dVector(colors)
        o3d.visualization.draw_geometries_with_editing([pc_open])
       
        
        '''
        load cropped pcd, prints mean of colors:
        '''
        # Extract points and intensity
        base_name, _ = os.path.splitext(pcd_file)
        ply_path = os.path.join("/home/sqdr/ROSDOCKER/noetic/src/data_lidar/filtered_data/2AUG_parking/ply",base_name + ".ply")
        pc_cropped = o3d.io.read_point_cloud(ply_path)
        mean = np.mean(np.asarray(pc_cropped.colors),axis=0)[0]*255
        print(f"File analysed: {ply_path}. MEAN: {mean:.2f}")
        print("-------------------------------------")
        
    except Exception as e:
        print(f"Failed to process {file_path}: {e}")



