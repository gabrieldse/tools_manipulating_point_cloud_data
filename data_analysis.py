import time
import os
import open3d as o3d

print(time.time())
# Get only pcd points from a specific time frame


def load_point_clouds(voxel_size=0.0):
    zero_time = 1722001459.792622566
    start_time = zero_time + 137
    end_time = zero_time + 160

    print(f'zero time = {zero_time} ')
    print(f'start time = {start_time} ')
    print(f'end time = {end_time} ')

    directory = "/home/sqdr/ROSDOCKER/noetic/src/data_bag/second_take_pcd/"

    point_clouds = []

    current_time = start_time

    # Loop through the files in the directory
    for file_name in os.listdir(directory):
        # Check if the file is a PCD file and starts with a number in the specified range
        if file_name.endswith(".pcd"):
            try:
                prefix = float(file_name.split('.')[0])
                if start_time <= prefix <= end_time:
                    # Construct the full file path
                    file_path = os.path.join(directory, file_name)
                    # Read the point cloud
                    pcd = o3d.io.read_point_cloud(file_path)
                    # pcd_down = pcd.voxel_down_sample(voxel_size=voxel_size)
                    # Append to the list of point clouds
                    point_clouds.append(pcd)
                    # point_clouds_down.append(pcd_down)
                    #print(f"Loaded {file_path}")
            except ValueError:
                # If the file name does not start with a valid number, skip it
                continue


    print(f"Loaded {len(point_clouds)} scans!")
    return point_clouds


# fuse them
# o3d.visualization.draw_geometries(point_clouds)

# add posegraph

# crop and save the crop comibned file

# o3d.visualization.draw_geometries_with_editing([point_clouds])
def merge_points():
    voxel_size = 0.02
    pcds = load_point_clouds(voxel_size)
    pcd_combined = o3d.geometry.PointCloud()
    for point_id in range(len(pcds)):
        # pcds[point_id].transform(pose_graph.nodes[point_id].pose)
        pcd_combined += pcds[point_id]
    pcd_combined_down = pcd_combined.voxel_down_sample(voxel_size=voxel_size)
    o3d.io.write_point_cloud("multiway_registration.pcd", pcd_combined_down)
    # o3d.visualization.draw_geometries_with_editing([pcd_combined_down])

    return pcd_combined

#  print("Load a polygon volume and use it to crop the original point cloud")
#     vol = o3d.visualization.read_selection_polygon_volume(
#         "crop/rectangle.json")
#     plane = vol.crop_point_cloud(pcd)
#     o3d.visualization.draw_geometries([chair])

# calculate statistic ()


#load_point_clouds(voxel_size=0.0)
# pcd_combined = merge_points()
pcd = o3d.io.read_point_cloud("multiway_registration.pcd")
# o3d.visualization.draw_geometries_with_editing([pcd])
o3d.visualization.crop_point_cloud([pcd])
# vol = o3d.visualization.read_selection_polygon_volume(
#         "cropped_test.json")
# plane = vol.crop_point_cloud(pcd)
# o3d.visualization.draw_geometries([plane])

#ref next approach
#ref como talvez usa pose graph https://www.open3d.org/docs/latest/tutorial/Advanced/multiway_registration.html