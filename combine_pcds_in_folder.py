from pypcd4 import PointCloud
import os
import argparse

'''
Combine all .pcd files in a folder while keeping only the fields x, y, z and intensity
'''

def pcd_folder_2_pcd_combined(folder_path,output_file):
    pcd_files = [f for f in os.listdir(folder_path) if f.endswith('.pcd')]
    point_clouds = []

    # Load all PCD files and convert to numpy arrays
    for pcd_file in pcd_files:
        file_path = os.path.join(folder_path, pcd_file)
        # print(file_path)
        try: 
            pc = PointCloud.from_path(file_path)
            array = pc.numpy(("x", "y", "z", "intensity"))
            point_clouds.append(PointCloud.from_xyzi_points(array))
        except Exception as e:
            print(f"Failed to process {file_path}: {e}")

    # Fuse all point clouds
    if point_clouds:
        fused_pc = point_clouds[0]
        for pc in point_clouds[1:]:
            fused_pc += pc
    else:
        raise ValueError("No PCD files found in the specified folder.")

    # Print fields of the combined point cloud
    print(f"Current fields in .pcd : {fused_pc.fields}.")
    print("Wait the pcd's are still being combined")
    # array =  fused_pc.numpy()
    parent_dir = os.path.dirname(folder_path)
    output_path = os.path.join(parent_dir,output_file)
    try:
        fused_pc.save(output_path)
        print(f"Combined PCD file saved to {output_path}")
    except Exception as e:
         print(f"Failed to save the combined PCD file: {e}")
    


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Combine all .pcd files in a folder while keeping only the fields x, y, z and intensity')
    parser.add_argument('folder_path', type=str, help='Path to the output file')
    parser.add_argument('output_file', type=str, help='Path to the folder containing pcd files')
    args = parser.parse_args()
    
    pcd_folder_2_pcd_combined(args.folder_path, args.output_file)
