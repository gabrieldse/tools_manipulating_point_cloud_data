import open3d as o3d

# Load your point cloud
pcd = o3d.io.read_point_cloud("/home/sqdr/Desktop/unilidar_proj/tool_manipulating_point_cloud/data/scans.pcd")

# Visualize and create a SelectionPolygonVolume
vis = o3d.visualization.VisualizerWithEditing()
vis.create_window()
vis.add_geometry(pcd)
vis.run()  # user picks points to form a polygon
vis.destroy_window()