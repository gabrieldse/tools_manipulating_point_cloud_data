# Install dependencies:

```
python3 -m pip install -r requirements.txt
```

Process:
1. data analysis - bag to pcd
2. manual selection - pcd ply
3. find_plane (via o3d) 
4. plot plane
5. 

4. python3 find_plane.py file_plane_1m_137_147.ply

RESALVAS:

OBS: I have to add the plane on 0 (at least center, maybe base to be more realistic)

# Analyse Data

# Select frames
    # .bag to .pcd
    # roscore
    # rosbag reindex P23_71.9_vert_2024-08-02-08-04-06.bag.active 
    # rosrun pcl_ros bag_to_pcd P23_71.9_vert_2024-08-02-08-04-06.bag.active /unilidar/cloud ./folder_of_pcd

# Merge pcd's

# Crop plane


# Perform plane analysis (find gaussian noise and plot it)
