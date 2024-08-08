from pypcd4 import PointCloud
import os
import argparse
import pandas as pd
import numpy as np

'''
Convert a .pcd file to a CSV file with additional fields for x, y, z, intensity, r, zenith, and azimuth.
'''

def pcd_2_csv(file_path, output_file): 
    # Load the PCD file
    pc = PointCloud.from_path(file_path)
    array: np.ndarray =  pc.numpy(("x", "y", "z", "intensity"))

    x = array[:, 0]
    y = array[:, 1]
    z = array[:, 2]
    intensity = array[:, 3]


    # Calculate additional fields
    r = np.sqrt(x**2 + y**2 + z**2)
    azimuth = np.degrees(np.arctan2(y, x)) % 360  # Azimuth between 0 and 360 degrees
    zenith = np.degrees(np.arccos(np.clip(z/ r, -1.0, 1.0)))  # Clip to avoid invalid values

    # Create DataFrame
    df = pd.DataFrame({
        'x': x,
        'y': y,
        'z': z,
        'intensity': intensity,
        'r': r,
        'zenith': zenith,
        'azimuth': azimuth
    })
    
    # Save DataFrame to CSV
    output_path = os.path.join(os.path.dirname(file_path), output_file)
    df.to_csv(output_path, index=False)
    print(f"CSV file saved to {output_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert a PCD file to CSV with additional fields.')
    parser.add_argument('file_path', type=str, help='Path to the PCD file')
    parser.add_argument('output_name', type=str, help='Name of the output CSV file')
    args = parser.parse_args()
    
    pcd_2_csv(args.file_path, args.output_name)
