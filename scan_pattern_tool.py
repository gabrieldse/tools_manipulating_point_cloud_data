import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import argparse

def process_file(file_path, skip_points):
    # Read the CSV file
    data = pd.read_csv(file_path, delimiter=',')

    # Extract columns
    if 'Time/s' in data.columns:
        time = data['Time/s']
        azimuth = data['Azimuth/deg']
        zenith = data['Zenith/deg']
    else:
        time = data['x']
        azimuth = data['y']
        zenith = data['z']
        

    # Function to update the plot with skipped points
    def update_plot(skip_points):
        # Skip points based on the step size
        time_skipped = time[::skip_points]
        azimuth_skipped = azimuth[::skip_points]
        zenith_skipped = zenith[::skip_points]

        # Set up the figure and 3D axis
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Labels
        ax.set_xlabel('Time/s')
        ax.set_ylabel('Azimuth/deg')
        ax.set_zlabel('Zenith/deg')

        # Set the limits for the axes based on the data
        ax.set_xlim([time.min(), time.max()])
        ax.set_ylim([azimuth.min(), azimuth.max()])
        ax.set_zlim([zenith.min(), zenith.max()])

        # ax.set_xlim([-10, +10])
        # ax.set_ylim([-10, +10])
        # ax.set_zlim([0, +20])

        # Initialize the point cloud
        point_cloud, = ax.plot([], [], [], 'ro')

        # Update function for animation
        def update(frame):
            # Update the point cloud data
            point_cloud.set_data(time_skipped[:frame+1], azimuth_skipped[:frame+1])
            point_cloud.set_3d_properties(zenith_skipped[:frame+1])
            return point_cloud,

        # Create the animation
        ani = FuncAnimation(fig, update, frames=len(time_skipped), interval=1, blit=True)

        # Show the plot
        plt.show()

    # Call the function with the desired number of points to skip
    update_plot(skip_points)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process and animate a 3D plot from CSV data.')
    parser.add_argument('file_path', type=str, help='Path to the CSV file')
    parser.add_argument('--skip-points', type=int, default=10, help='Number of points to skip in the plot (default is 10)')
    args = parser.parse_args()

    process_file(args.file_path, args.skip_points)
