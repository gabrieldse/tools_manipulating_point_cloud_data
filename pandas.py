import pandas as pd
 
def load_pcd(file_path):

    with open(file_path, 'r') as f:

        lines = f.readlines()
 
    # Read the header to determine how to parse the file

    header = []

    data_start_index = 0

    for i, line in enumerate(lines):

        header.append(line.strip())

        if line.startswith('DATA'):

            data_start_index = i + 1

            break
 
    # Parse the header

    columns = []

    for line in header:

        if line.startswith('FIELDS'):

            columns = line.split()[1:]

            break
 
    # Read the data

    data = pd.read_csv(file_path, skiprows=data_start_index, delim_whitespace=True, header=None)

    data.columns = columns

    return data
 
def print_first_10_points_with_info(data):

    for i in range(10):

        point_info = f"Point {i}: "

        point_info += ", ".join([f"{col}: {data.at[i, col]}" for col in data.columns])

        print(point_info)
 
# Example usage

pcd_data = load_pcd("converted/1695357725.135129690.pcd")

print_first_10_points_with_info(pcd_data)

 