import open3d as o3d
import json

# Load your point cloud
pcd = o3d.io.read_point_cloud("data/multiway_registration.pcd")

# Visualize and create a SelectionPolygonVolume
vis = o3d.visualization.VisualizerWithEditing()
vis.create_window()
vis.add_geometry(pcd)
vis.run()  # user picks points to form a polygon
vis.destroy_window()

# Get the picked points (indices)
picked_points = vis.get_picked_points()

# Create a SelectionPolygonVolume
vol = o3d.visualization.SelectionPolygonVolume()

# Define axis bounds and bounding polygon (you need to set these manually or interactively)
axis_max = 1.0  # Example value
axis_min = -1.0  # Example value
orthogonal_axis = "Z"  # Example value, can be "X", "Y", or "Z"
bounding_polygon = [[0, 0], [1, 0], [1, 1], [0, 1]]  # Example polygon, you should replace this with actual values

# Set these values to the SelectionPolygonVolume
# vol.axis_max = axis_max
# vol.axis_min = axis_min
# vol.orthogonal_axis = orthogonal_axis
# vol.bounding_polygon = o3d.utility.Vector2dVector(bounding_polygon)

# Format the data for JSON
data = {
    "axis_max": axis_max,
    "axis_min": axis_min,
    "bounding_polygon": bounding_polygon,
    "class_name": "SelectionPolygonVolume",
    "orthogonal_axis": orthogonal_axis,
    "version_major": 1,
    "version_minor": 0
}

# Save to JSON file
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Selection polygon saved to crop_selection.json")
