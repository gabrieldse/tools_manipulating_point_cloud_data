import open3d as o3d
import argparse

def main(file_name):
    # Load the point cloud
    pcd = o3d.io.read_point_cloud(file_name)

    # Segment the plane
    plane_model, inliers = pcd.segment_plane(distance_threshold=0.02, ransac_n=3, num_iterations=1000)

    [a, b, c, d] = plane_model
    print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a point cloud file to fit a plane.')
    parser.add_argument('file_name', type=str, help='The path to the point cloud file (e.g., plane_1m.ply)')
    
    args = parser.parse_args()
    
    main(args.file_name)   

# inlier_cloud = pcd.select_by_index(inliers)
# inlier_cloud.paint_uniform_color([1, 0, 0])
# outlier_cloud = pcd.select_by_index(inliers, invert=True)
# o3d.visualization.draw_geometries([inlier_cloud, outlier_cloud])