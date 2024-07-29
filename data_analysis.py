import time
import os
import open3d as o3d


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

def merge_points(pcds,save_pcd_file_as):
    pcd_combined = o3d.geometry.PointCloud()
    for point_id in range(len(pcds)):
        # pcds[point_id].transform(pose_graph.nodes[point_id].pose)
        pcd_combined += pcds[point_id]
    o3d.io.write_point_cloud(save_pcd_file_as,pcd_combined)
    # o3d.visualization.draw_geometries_with_editing([pcd_combined_down])

    return pcd_combined

pcd_paths = load_point_clouds("/home/sqdr/ROSDOCKER/noetic/src/data_bag/second_take_pcd/")
save_pcd_file_as="wall_xm_137_167.pcd"
pcd_combined = merge_points(pcd_paths,save_pcd_file_as)


# pcd = o3d.io.read_point_cloud(pcd_combined)
o3d.visualization.draw_geometries_with_editing([pcd_combined])
# o3d.visualization.crop_point_cloud([pcd])
# vol = o3d.visualization.read_selection_polygon_volume(
#         "cropped_test.json")
# plane = vol.crop_point_cloud(pcd)
# o3d.visualization.draw_geometries([plane])

#ref next approach
#ref como talvez usa pose graph https://www.open3d.org/docs/latest/tutorial/Advanced/multiway_registration.html