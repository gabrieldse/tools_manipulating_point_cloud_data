import os
import glob
import pandas as pd
import numpy as np

def spherical_to_cartesian(azimuth, zenith, radius=10):
    # Convert degrees to radians
    azimuth_rad = np.radians(azimuth)
    zenith_rad = np.radians(zenith)
    
    # Calculate Cartesian coordinates
    x = radius * np.sin(zenith_rad) * np.cos(azimuth_rad)
    y = radius * np.sin(zenith_rad) * np.sin(azimuth_rad)
    z = radius * np.cos(zenith_rad)
    
    return x, y, z

def convert_spherical_csv_2_cartesian_csv(input_file_path, output_file_path):
    # Read the CSV file
    data = pd.read_csv(input_file_path)
    
    # Ensure the CSV has the correct columns
    if not {'Time/s', 'Azimuth/deg', 'Zenith/deg'}.issubset(data.columns):
        raise ValueError("Input CSV must contain 'Time/s', 'Azimuth/deg', and 'Zenith/deg' columns")
    
    # Calculate Cartesian coordinates
    x, y, z = spherical_to_cartesian(data['Azimuth/deg'], data['Zenith/deg'])
    
    # Create a new DataFrame with the desired structure
    converted_data = pd.DataFrame({
        'Time/s': x,
        'Azimuth/deg': y,
        'Zenith/deg': z
    })
    
    # Write the new DataFrame to a CSV file
    converted_data.to_csv(output_file_path, index=False)

def convert_all_csvs_in_folder(input_folder, output_folder):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Get all CSV files in the input directory
    csv_files = glob.glob(os.path.join(input_folder, '*.csv'))
    
    for csv_file in csv_files:
        # Get the base name of the file to create the output file path
        base_name = os.path.basename(csv_file)
        output_file_path = os.path.join(output_folder, base_name)
        
        # Convert the CSV file
        convert_spherical_csv_2_cartesian_csv(csv_file, output_file_path)













    # Define the function to generate vertical angles
    # PS: The amount of points per turn sould be multiple of two

def generate_vertical_angles(azimuth_steps_number, zenith_step_number,round_numbers):
    data = []
    data2 = [1]
    points_per_turn = 180/zenith_step_number

    for i in range(round_numbers):
        for _ in range(azimuth_steps_number):
            value0 = 90
            data.append(value0)
            
            # Increases the angle at a constant STEP for the first half
            up = int(points_per_turn/2)
            #print("going up", up)
            for _ in range(int(points_per_turn)):
                value1 = value0 - zenith_step_number
                data.append(value1)  # Append only the value1, not a tuple
                value0 = value1
        
        # Store the last azimuth from the first half loop
        # value0 = last_azimuth
        
        # Second half loop
        #print("going down", up)
        # for _ in range(int(points_per_turn/2)):
        #     value1 = value0 - step
        #     data.append(-value1)  # Append only the value1, not a tuple
        #     value0 = value1  # Update value0 to the new value1
    
    return data,data2

# Define the function to generate CSV with the formula
def generate_csv_with_formula(output_file_path):
    time_step = 4.17e-06
    print("time step wrong", time_step)
    points_per_turn = 60 * 2
    zenith_step = 180 / points_per_turn
    azimuth_number = 8
    azimuth_step = 180/azimuth_number
    round_numbers = 10
    zenith_angles = generate_vertical_angles(azimuth_number, zenith_step,round_numbers)

    # Generate the time column
    num_rows = len(zenith_angles)
    print("number of row =", num_rows)
    time = np.arange(0, num_rows * time_step, time_step)

    # Generate the azimuth column
    print("azimuth_array",np.arange(0, 360, azimuth_step))
    print("repeat x times, x = ",int(len(zenith_angles)/azimuth_number/round_numbers))
    azimuth = np.repeat(np.arange(0, 360, azimuth_step), int(len(zenith_angles)/azimuth_number))[:num_rows]
    

    # Generate the zenith column
    zenith = np.tile(zenith_angles, num_rows // len(zenith_angles) + 1)[:num_rows]

    # Create the DataFrame
    print("len time =",len(time))
    print('len azimuth antes = ', len(azimuth))
    print("zenith len = ", len(zenith))

    data = pd.DataFrame({'Time/s': time, 'Azimuth/deg': azimuth, 'Zenith/deg': zenith})
    
    # Save the DataFrame to a CSV file
    data.to_csv(output_file_path, index=False)

    return 0


# print("DEBUG VERTICAL ANGLE")
time_step = 4.17e-06
points_per_turn = 60 * 2
print("points per turn:", points_per_turn)
zenith_step = 180 / points_per_turn
print("zenith_step: ", zenith_step)
azimuth_number = 8
azimuth_step = 180/azimuth_number
print("azimuth step",azimuth_step)
round_numbers = 10
zenith_angles,data2 = generate_vertical_angles(azimuth_number, zenith_step,round_numbers)
print("zenith angles =",zenith_angles)
print("data2 = ",data2)


# unitree_sphe = 'csv_polar/unitree_polar.csv'
# generate_csv_with_formula(unitree_sphe)
# unitree_cart = 'csv_cartesian/unitree_cartesian.csv'
# convert_spherical_csv_2_cartesian_csv(unitree_sphe,unitree_cart)
