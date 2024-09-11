Collection of Python scripts for manipulating and visualizing PointCloud data, as well as parsing auxiliary UART MAVLINK2 data from the Unitree L1 Lidar.

# Install dependencies:

```
python3 -m pip install -r requirements.txt
```
# Pointcloud Manipulation
### ROSBAG to .pcd of each frame 
You need to have sourced ROS1 for this script.(In case your rosbags are not correctly indexed, do: "rosbag reindex *.bag.active")

```bash
roscore & rosrun pcl_ros bag_to_pcd <file_name> <topic_name=/unilidar/cloud> <output_name>
```

#### Merge pcd's
Merge multiple pointclouds into a sigle pointcloud.

```bash
python3 combine_pcds_in_folder.py <folder_path> <output_file_name>
```

### Crop a merged pcd
The used script was the following based on Open3D's interactive visualization [open3D link](https://www.open3d.org/docs/0.11.1/tutorial/visualization/interactive_visualization.html)

```bash
python3 cropping.py
```

### Heatmap of FOV from csv 
The csv need the azimuth and zenith columns. The --no_plot is optional
```
python3 fov_heatmap.py <path_to_csv>  <number_of_individual_sacns> --threshold <thershold> --no_plot 
```


### Plane fit and gaussian noise distribution:
todo: pass path as argument
```
python3 data_analysis.py 
```

### Linear Regression of data 
todo: pass array as argument
```
python3 signal_noise_ratio.py
```

# Parse MAVLINK2 Unitree L1 data
Verify if the sensor is available at the correct serial port with 
```ls /dev/ttyUSB*"```

If necessery modify this part on the script:
```serial_port = '/dev/ttyUSB0'```

```
cd parse_mavlink_aux_messages

python3 plot_temperature_real_time.py

python3 raw_aux_data_parse.py

python3 raw_distance_parse.py

python3 raw_imu_parse.py
```

# Useful:

VSCODE extension to visualize .pcd files: pcd-viewer



