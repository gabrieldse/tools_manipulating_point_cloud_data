import numpy as np
import open3d as o3d

if __name__ == "__main__":

    print("Load a ply point cloud, print it, and render it")
    pcd = o3d.io.read_point_cloud("converted/1695357725.135129690.pcd")

    points = np.asarray(pcd.points)
    pcd.

    for i in range(10):
        print(f"Point {i}: {points[i]}")