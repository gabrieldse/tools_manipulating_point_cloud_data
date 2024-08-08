import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# import data

file_path = "/home/sqdr/Desktop/unilidar_pc_asus/data/referece_measurements/output_data.csv"
df = pd.read_csv(file_path, delimiter=',', nrows=200000)
# print(df.head())
azimuth = df["azimuth"]
zenith = df["zenith"]

# print(azimuth, zenith)

# # create mrad array
'''
A 2D array representing a 360° x 90° field of view with a 5 mrad x 5 mrad grid resolution. (1 mrad = 1 milliradian = an angle where the arc length is 1/1000th of the radius of the circle.)
to generate a graph to compare with the LIVOX graph
(https://www.livoxtech.com/3296f540ecf5458a8829e01cf429798e/downloads/Point%20cloud%20characteristics.pdf) grap
'''

'''
arc length = theta x radius
interval = circuference lenght / arc lenght 
360 = 2 pi rad 
    -> 2pi/5mrad = 1256,67 intervals
90 = pi / 2 rad 
    -> pi/2/5mrad = 314,16 intervals
'''
rows, cols =  314,1257
#rows,cols = 90,360
fov_2d_array = np.zeros((rows, cols))
# print(np.shape(fov_2d_array))

# reminder pandas start at 0 and np array also
i = 0


scan_points_total = 2160*5
for j in range (1,93):
    scan_points_total = 2160*j
    for i in range(scan_points_total-2160,scan_points_total):

        # c_zenith = zenith[i]
        # if  zenith[i] > 180:
        #     c_zenith = zenith[i] - 180 # current zenith


        pixel_v = int(zenith[i]/90*rows)
        pixel_h = int(azimuth[i]/360*cols)

        # print(zenith[i],azimuth[i])

        fov_2d_array[int(pixel_v)-1,int(pixel_h)-1] += 1

        i = i + 1

        # Display the array as an image
        #np.flipud(fov_2d_array) # flip the array vertically 

    if j % 10 == 0: 
        # zoom in a 20 x 40 square
        zoom_array = fov_2d_array[200:200 + 20, 900:900 + 40]
        # print(zoom_array)

        plt.figure()
        plt.imshow(zoom_array, cmap='hot')  # You can use different colormaps
        plt.colorbar()  # Optional: Adds a color bar to the side
        plt.title('2D Array as Image')

        




plt.figure()
plt.imshow(fov_2d_array, cmap='hot')  # You can use different colormaps
plt.colorbar()  # Optional: Adds a color bar to the side
plt.title(f'Final plot after {j} scans ')
plt.show()





# 0-360 / pas (x mrad) hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh
# 0 90 / pas (x mrad) 

# iterrate all poits and after division incremenet

# store array status after 1 scann (20000 ) points

# print array.