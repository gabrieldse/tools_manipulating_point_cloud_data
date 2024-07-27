# examples/Python/Basic/pointcloud.py

import numpy as np
import open3d as o3d
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

if __name__ == "__main__":

    print("Load a ply point cloud, print it, and render it")
    pcd = o3d.io.read_point_cloud("/home/sqdr/ROSDOCKER/noetic/src/data_bag/second_take_pcd/1722001459.792622566.pcd")
    pcd2 = o3d.io.read_point_cloud("/home/sqdr/ROSDOCKER/noetic/src/data_bag/second_take_pcd/1722001459.902050734.pcd")
    print(pcd)
    print(type(pcd))
    p = np.asarray(pcd.points)
    print(p)

    # o3d.visualization.draw_geometries([pcd])
    # o3d.visualization.draw_geometries([pcd,pcd2])

    # MATPLOTLIB plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    #ax.plot(p[:,0],p[:,1],p[:,2])
    ax.scatter(p[:,0],p[:,1],p[:,2])
    plt.show()



    # print("Downsample the point cloud with a voxel of 0.05")
    # downpcd = pcd.voxel_down_sample(voxel_size=0.0005)
    # o3d.visualization.draw_geometries([downpcd])

    # print("Recompute the normal of the downsampled point cloud")
    # downpcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
    #     radius=0.1, max_nn=30))
    # o3d.visualization.draw_geometries([downpcd])

    # print("Print a normal vector of the 0th point")
    # print(downpcd.normals[0])
    # print("Print the normal vectors of the first 10 points")
    # print(np.asarray(downpcd.normals)[:10, :])
    # print("")

    print("Load a polygon volume and use it to crop the original point cloud")
    vol = o3d.visualization.read_selection_polygon_volume(
        "crop/rectangle.json")
    chair = vol.crop_point_cloud(pcd)
    o3d.visualization.draw_geometries([chair])
    print("")

    # print("Paint chair")
    # chair.paint_uniform_color([1, 0.706, 0])
    # o3d.visualization.draw_geometries([chair])
    # print("")