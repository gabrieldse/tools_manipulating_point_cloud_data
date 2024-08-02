import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import os



class PointCloudAnimator:
    def __init__(self, pdc_files):
        self.pdc_files = pdc_files
        self.current_frame = 0

        # Create a new figure for plotting
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d',)  # Use 3D subplot
        self.scat = None
        
        # Initialize plot
        self.update_plot()

        # Connect key press event to the handler
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

    def read_point_cloud(self, file_path):
        # Load the point cloud using Open3D
        pcd = o3d.io.read_point_cloud(file_path)
        return np.asarray(pcd.points)

    def update_plot(self,store_state=0):
        # Load the point cloud file for the current frame
        file_path = self.pdc_files[self.current_frame]
        points = self.read_point_cloud(file_path)

        # Save current axis limits and camera orientation
        if store_state == 1:
            self.saved_xlim = self.ax.get_xlim()
            self.saved_ylim = self.ax.get_ylim()
            self.saved_zlim = self.ax.get_zlim()
            self.saved_elev = self.ax.elev
            self.saved_azim = self.ax.azim

        # Clear previous plot
        self.ax.clear()
        
        # Plot the point cloud
        self.scat = self.ax.scatter(points[:, 0], points[:, 1], points[:, 2], c=points[:, 2], cmap='viridis', s=10)
        
        # Set axis labels and title
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.set_title(f"Frame {self.current_frame + 1} - {os.path.basename(file_path)}")
        
        # Restore axis limits and camera orientation
        if hasattr(self, 'saved_xlim'):
            self.ax.set_xlim(self.saved_xlim)
            self.ax.set_ylim(self.saved_ylim)
            self.ax.set_zlim(self.saved_zlim)
            self.ax.view_init(elev=self.saved_elev, azim=self.saved_azim)
        
        # Redraw the figure
        self.fig.canvas.draw()

    def on_key_press(self, event):
        if event.key == 'right':
            # Move to next frame
            self.current_frame = (self.current_frame + 1) % len(self.pdc_files)
            self.update_plot(store_state=1)
        elif event.key == 'left':
            # Move to previous frame
            self.current_frame = (self.current_frame - 1) % len(self.pdc_files)
            self.update_plot(store_state=0)


def crop_bag_time_clouds(direction=0,time=5,directory="/home/sqdr/Desktop/unilidar_proj/tool_manipulating_point_cloud/rosbag"):
    zero_time = 1722585852.499159336 # name of the first file
    final_time = 1722585928.234170198 # name of the last file - pcd
    # start_time = zero_time + 138 # 137
    # end_time = zero_time + 145 # 160

    if direction == 0:
        # decreasing order
        start_time = final_time
        final_time = final_time - time
    elif direction == 1:
        start_time = zero_time
        final_time = zero_time + time

    print(f'zero time = {zero_time} ')
    print(f'start time = {start_time} ')
    print(f'end time = {final_time} ')

    point_clouds = [] # list of pointclouds in the selected time interval

    current_time = start_time

    # Loop through the files in the directory
    for file_name in os.listdir(directory):
        # Check if the file is a PCD file and starts with a number in the specified range
        if file_name.endswith(".pcd"):
            try:
                prefix = float(file_name.split('.')[0])
                if start_time <= prefix <= final_time:
                    # Construct the full file path
                    file_path = os.path.join(directory, file_name)
                    # Read the point cloud
                    # pcd = o3d.io.read_point_cloud(file_path)
                    # pcd_down = pcd.voxel_down_sample(voxel_size=voxel_size)
                    # Append to the list of point clouds
                    point_clouds.append(file_path)
                    # point_clouds_down.append(pcd_down)
                    #print(f"Loaded {file_path}")
            except ValueError:
                # If the file name does not start with a valid number, skip it
                continue
       

    return point_clouds

def main(pdc_files):
    
    animator = PointCloudAnimator(pdc_files)
    plt.show()


if __name__ == "__main__":
    # List of .pdc files (replace with your actual file paths)
    pcd_files = crop_bag_time_clouds()
    pcd = o3d.io.read_point_cloud([pcd_files])

    # Visualize and create a SelectionPolygonVolume
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window()
    vis.add_geometry(pcd)
    vis.run()  # user picks points to form a polygon
    vis.destroy_window()
    cropped = o3d.visualization.draw_geometries_with_editing([pcd_files])

    # pdc_files = ["1722001459.792622566.pcd","1722001459.902050734.pcd","1722001460.020745754.pcd"]
    
    # Run the interactive plot
    # main(pdc_files)

# if __name__ == "__main__":
#     # List of .pdc files (replace with your actual file paths)
#     pdc_files = ["1722001459.792622566.pcd","1722001459.902050734.pcd","1722001460.020745754.pcd"]
    
#     # Run the animation
#     main(pdc_files, interval=2000)  # Interval in milliseconds


