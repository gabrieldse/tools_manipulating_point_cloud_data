import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
import argparse
import scipy.optimize # for sin fit

'''


'''
''' Animate the x,y,z rows of a data frame '''
def animate_xyz_df(data, skip_points,nrows=20000):
    # Read the CSV file
    data = data
    pd.options.display.max_columns = None
    # print(data.head())

    # print(only_points_coord.head())
    # print(only_points_coord.min())
    # print(only_points_coord.max())

    # Extract columns
    if 'Time/s' in data.columns:
        time = data['Time/s']
        azimuth = data['Azimuth/deg']
        zenith = data['Zenith/deg']
    elif 'x' in data.columns:
        time = data['x']
        azimuth = data['y']
        zenith = data['z']
    elif 'X'  in data.columns:
        time = data['X']
        azimuth = data['Y']
        zenith = data['Z']
        

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
        # ax.set_xlim([time.min(), time.max()])
        # ax.set_ylim([azimuth.min(), azimuth.max()])
        # ax.set_zlim([zenith.min(), zenith.max()])

        ax.set_xlim([-10, +10])
        ax.set_ylim([-10, +10])
        ax.set_zlim([0, +5])

        # Initialize the point cloud
        point_cloud, = ax.plot([], [], [], 'ro',markersize=1)

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

''' Animate the zenith and azimuth rows of a data frame '''
def animate_polar_df(data, skip_points,nrows=20000):
    # Read the CSV file
    data = data
    azimuth = data['azimuth']
    zenith = data['zenith']
    time = data['index']

    #convert to cartesian (R=1 for normalization)
    r = 30

    # Convert to Cartesian coordinates
    x = r * np.sin(np.deg2rad(zenith)) * np.cos(np.deg2rad(azimuth))
    y = r * np.sin(np.deg2rad(zenith)) * np.sin(np.deg2rad(azimuth))
    z = r * np.cos(np.deg2rad(zenith))
    
    # ** correct for mirror values
    z = np.abs(z)

    # Function to update the plot with skipped points
    def update_plot(skip_points):
        # Skip points based on the step size
        x_skipped = x[::skip_points]
        y_skipped = y[::skip_points]
        z_skipped = z[::skip_points]

        # Set up the figure and 3D axis
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Labels
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

        # Set the limits for the axes based on the data
        ax.set_xlim([x.min(), x.max()])
        ax.set_ylim([y.min(), y.max()])
        ax.set_zlim([z.min(), z.max()])

        # ax.set_xlim([-10, +10])
        # ax.set_ylim([-10, +10])
        # ax.set_zlim([0, +5])

        # Initialize the point cloud
        point_cloud, = ax.plot([], [], [], 'ro',markersize=4)

        # Update function for animation
        def update(frame):
            # Update the point cloud data
            point_cloud.set_data( x_skipped[:frame+1], y_skipped[:frame+1])
            point_cloud.set_3d_properties(z_skipped[:frame+1])
            return point_cloud,

        # Create the animation
        ani = FuncAnimation(fig, update, frames=len(x_skipped), interval=10, blit=True)
        # Show the plot
        plt.show()

    # Call the function with the desired number of points to skip
    update_plot(skip_points)

def filter_csv_2_xyz_intesity_polar(file_path,nrows=50000):
    df = pd.read_csv(file_path, delimiter=',', nrows=nrows)

    # extract point coordinates
    if 'X'  in df.columns:
        x = df['X']
        y = df['Y']
        z = df['Z']
        reflectivity = df['Reflectivity']
    elif 'x' in df.columns:
        x = df['x']
        y = df['y']
        z = df['z']
    elif 'Time/s' in df.columns:
        x = df['Time/s']
        y = df['Azimuth/deg']
        z = df['Zenith/deg']

    # Calculate polar coordinates
    zenith = []
    azimuth = []
    r = np.sqrt(x**2 + y**2 + z**2)
    azimuth = np.degrees(np.arctan2(y, x)) % 360  # Ensure azimuth is between 0 and 360 degrees
    zenith = np.where(r != 0, np.degrees(np.arccos(z / r)), 0)

    df_extended = pd.DataFrame({
        'x': x,
        'y': y,
        'z': z,
        'intensity': reflectivity,
        'azimuth': azimuth,
        'zenith': zenith
    })

    return df_extended

def plot_polar_scan_patter(df):

    # Extract data
    df.index.name = 'index'
    df.head()
    if 'x' in df.columns:
        x = data['x']
        y = data['y']
        z = data['z']
        # intensity = data['intensity']
        zenith = data['zenith']
        azimuth = data['azimuth']
    elif 'X'  in df.columns:
        x = data['X']
        y = data['Y']
        z = data['Z']
        # intensity = data['intensity']
        zenith = data['zenith']
        azimuth = data['azimuth']

    plt.figure(figsize=(14, 6))

    # Plot Azimuth
    plt.subplot(1, 2, 1)
    plt.plot(df['index'], df['azimuth'], 'o', label='Azimuth')
    plt.xlabel('Point Index')
    plt.ylabel('Azimuth angle (degrees)')
    plt.title('Index vs Azimuth')
    plt.grid(True)
    plt.legend()

    # Plot Zenith
    plt.subplot(1, 2, 2)
    plt.plot(df['index'], df['zenith'], 'o', label='Zenith', color='orange')
    plt.xlabel('Point Index')
    plt.ylabel('Zenith angle(degrees)')
    plt.title('Index vs Zenith')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()
    plt.show()

def fit_sin(tt, yy):
    '''Fit sin to the input time sequence, and return fitting parameters "amp", "omega", "phase", "offset", "freq", "period" and "fitfunc"'''
    tt = np.array(tt)
    yy = np.array(yy)
    ff = np.fft.fftfreq(len(tt), (tt[1]-tt[0]))   # assume uniform spacing
    Fyy = abs(np.fft.fft(yy))
    guess_freq = abs(ff[np.argmax(Fyy[1:])+1])   # excluding the zero frequency "peak", which is related to offset
    guess_amp = np.std(yy) * 2.**0.5
    guess_offset = np.mean(yy)
    guess = np.array([guess_amp, 2.*np.pi*guess_freq, 0., guess_offset])

    def sinfunc(t, A, w, p, c):  return A * np.sin(w*t + p) + c
    popt, pcov = scipy.optimize.curve_fit(sinfunc, tt, yy, p0=guess)
    A, w, p, c = popt
    f = w/(2.*np.pi)
    fitfunc = lambda t: A * np.sin(w*t + p) + c
    return {"amp": A, "omega": w, "phase": p, "offset": c, "freq": f, "period": 1./f, "fitfunc": fitfunc, "maxcov": numpy.max(pcov), "rawres": (guess,popt,pcov)}

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process and animate a 3D plot from CSV data.')
    parser.add_argument('file_path', type=str, help='Path to the CSV file')
    parser.add_argument('--skip-points', type=int, default=10, help='Number of points to skip in the plot (default is 10)')
    parser.add_argument('--nrows', type=int,default=2048, help='Number of points you wish to import from the original csv')
    args = parser.parse_args()
    
    # Convert file
    # data = filter_csv_2_xyz_intesity_polar(args.file_path,args.nrows)
    # converted_data = data.to_csv('livox_indoor_4_scans_with_polar.csv', index=True)

    # Animate 
    #data = pd.read_csv('livox_indoor_1_scans_with_polar.csv', delimiter=',', nrows=20000)
    # data = converted_data
    # animate_xyz_df(data, args.skip_points)
    data = pd.read_csv('/home/sqdr/ROSDOCKER/noetic/src/point_lio_ws/data_filtering/data/output_data.csv',delimiter=',',nrows=2100)
    animate_polar_df(data, args.skip_points)

    #Plot scan patter in polar
    '''for know I have to add the 'index' as the first column's name'''
    # data = pd.read_csv(args.file_path, delimiter=',', nrows=args.nrows)
    plot_polar_scan_patter(data)

