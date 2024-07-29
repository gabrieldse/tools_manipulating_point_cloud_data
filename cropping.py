import open3d as o3d

pcd = o3d.io.read_point_cloud("data/multiway_registration.pcd")



# Visualize and create a SelectionPolygonVolume
# vis = o3d.visualization.VisualizerWithEditing()
# vis.create_window()
# vis.add_geometry(pcd)
# vis.run()  # user picks points to form a polygon
# vis.destroy_window()

print("Load a polygon volume and use it to crop the original point cloud")
vol = o3d.visualization.read_selection_polygon_volume(
    "data.json")
plane = vol.crop_point_cloud(pcd)
o3d.visualization.draw_geometries([plane])