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

# Heatmap of FOV from csv (the csv need the azimuth and zenith columns)
```
python3 fov_heatmap.py <path_to_csv>  <number_of_individual_sacns> --threshold <thershold>
```

# Plane fit and gaussian noise distribution:
todo: pass path as argument
```
python3 data_analysis.py 
```

# Linear Regression of signal to noise ration*
todo: pass array as argument
```
python3 signal_noise_ratio.py
```

# Useful:

VSCODE extension to visualize .pcd files: pcd-viewer



