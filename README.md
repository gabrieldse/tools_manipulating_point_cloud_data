# Install dependencies:

```
python3 -m pip install -r requirements.txt
```

# ROSBAG 2 .pcd of each frame 
You need to have and source ROS1 for this step
```
roscore & rosrun pcl_ros bag_to_pcd <file_name> <topic_name=/unilidar/cloud> <output_name>
```

# Merge pcd's
python3 combine_pcds_in_folder.py <folder_path> <output_file_name>


# Useful:

VSCODE extension to visualize .pcd files: pcd-viewer



