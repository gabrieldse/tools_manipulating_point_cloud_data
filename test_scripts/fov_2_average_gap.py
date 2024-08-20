import pandas as pd
import subprocess
import matplotlib.pyplot as plt
import numpy as np
import csv

def compute_average_gaps(fov_array):
    
    def compute_line_gaps(array):
        # Initialize the list to store line average gaps
        line_average_gaps = []
        
        num_rows, num_cols = array.shape
        
        def get_valid_range(index, length):
            start = max(0, index - 4)
            end = min(length, index + 4)  # index + 2 is exclusive
            return start, end
        
        def compute_gap(last_non_zero_pos, index, extended_line, start, end):
            min_hor_dist = float('inf')
            min_vert_dist = float('inf')

            if extended_line.ndim == 2:
                for row_index, col_index in np.ndindex(extended_line.shape):
                    element = extended_line[row_index, col_index]
                    if element != 0:
                        dist_vert = abs(row_index - (index - start))  # Vertical distance (row difference)
                        dist_hor = abs(col_index - index)  # Horizontal distance (column difference)

                        # Only consider horizontal distance if it is larger than vertical distance
                        if dist_hor > dist_vert and dist_hor < min_hor_dist:
                            min_hor_dist = dist_hor
                            min_vert_dist = dist_vert  # This is just informative but not used in the final result

            elif extended_line.ndim == 1:
                for i, value in enumerate(extended_line):
                    if value != 0:
                        current_hor_dist = abs(i - last_non_zero_pos)
                        if current_hor_dist < min_hor_dist:
                            min_hor_dist = current_hor_dist

            return min_hor_dist
        
        def process_line(line, extended_line, start, end):
            last_non_zero_pos = None
            line_sum_of_gaps = 0
            count_non_zero_elements = 0
            
            for index, value in enumerate(line):
                if value != 0:
                    if last_non_zero_pos is not None:
                        gap = compute_gap(last_non_zero_pos, index, extended_line, start, end)
                        line_sum_of_gaps += gap
                        count_non_zero_elements += 1
                    last_non_zero_pos = index
            
            if count_non_zero_elements > 4:
                line_average_gap = line_sum_of_gaps / (count_non_zero_elements - 1)
                line_average_gaps.append(line_average_gap)
        
        for i in range(num_rows):
            # Get valid range of lines to consider
            start_row, end_row = get_valid_range(i, num_rows)
            # Collect data from the lines within the range
            if end_row - start_row > 1:
                extended_line = np.concatenate(array[start_row:end_row], axis=0)
            else:
                extended_line = array[start_row:end_row][0]
            line = array[i]
            process_line(line, extended_line, start_row, end_row)
        
        # Calculate and return the average of all line average gaps
        if line_average_gaps:
            overall_average_gap = sum(line_average_gaps) / len(line_average_gaps)
        else:
            overall_average_gap = None
        
        return overall_average_gap, line_average_gaps

    # Horizontal gaps
    horizontal_average_gap, horizontal_gaps = compute_line_gaps(fov_array)
    print(f"Horizontal average gap = {horizontal_average_gap:.2f}")

    # Vertical gaps
    vertical_average_gap, vertical_gaps = compute_line_gaps(fov_array.T)
    print(f"Vertical average gap = {vertical_average_gap:.2f}")

    if horizontal_average_gap is not None:
        print(f"The final horizontal average gap is: {horizontal_average_gap:.2f} pixels ")
        print(f"with 314 lines, i.e : {(360/314)*horizontal_average_gap:.2f} degrees")
    else:
        print("No valid data to compute horizontal average gap.")

    if vertical_average_gap is not None:
        print(f"The final vertical average gap is: {vertical_average_gap:.2f} pixels ")
        print(f"with 314 lines, i.e : {(88/314)*vertical_average_gap:.2f} degrees")
    else:
        print("No valid data to compute vertical average gap.")

    # Save gaps to CSV
    with open('gaps.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Direction', 'Line Index', 'Gap'])
        
        # Write horizontal gaps
        for index, gap in enumerate(horizontal_gaps):
            writer.writerow(['Horizontal', index, gap])
        
        # Write vertical gaps
        for index, gap in enumerate(vertical_gaps):
            writer.writerow(['Vertical', index, gap])

    return horizontal_average_gap, vertical_average_gap, (360/314)*horizontal_average_gap, (88/314)*vertical_average_gap

def calculate_fov_heatmap(number_scans,file):
    # Define the command and its arguments
    number_scans = number_scans
    command = ["python3", "/home/sqdr/ROSDOCKER/noetic/src/data_lidar/data_filtering_scripts/fov_heatmap.py", str(file), str(number_scans),"--no_plot"] # ,"--no_plot"

    # Run the command
    try:
        # subprocess.run() executes the command and waits for it to finish
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Print the standard output and error
        # print("Standard Output:", result.stdout)
        # print("Standard Error:", result.stderr)
        # print("Return Code:", result.returncode)
    
    except subprocess.CalledProcessError as e:
        print("An error occurred while executing the command.")
        print("Error Output:", e.stderr)
        print("Return Code:", e.returncode)

file_to_analyse = "/home/sqdr/ROSDOCKER/noetic/src/data_lidar/ROSBAG/SITE_referece_measurements/output_data.csv"
fov_filename = '/home/sqdr/ROSDOCKER/noetic/src/data_lidar/data_filtering_scripts/test_scripts/fov_2D_array.csv'
horizontal_progression = []
vertical_progression = []
scan_number = 15

for number in range(1,scan_number):
    # Save the field of view of the the number on a file fov_2D_array.csv
    calculate_fov_heatmap(number,file_to_analyse)

    # Read this file
    df = pd.read_csv(fov_filename,delimiter=',')
    fov_array = df.to_numpy()

    # Takes the fov array and compute the average gaps against a certain criterium
    _, _, horizontal_result, vertical_result = compute_average_gaps(fov_array)
    horizontal_progression.append(horizontal_result)
    vertical_progression.append(vertical_result)

print(horizontal_result)
# Correct:
x = np.linspace(0.1,(scan_number)/10,scan_number-1) 
print(x)
plt.plot(x, horizontal_progression, 'r--', linewidth=3, label='horizontal')
plt.plot(x, vertical_progression, 'b--', linewidth=3, label='vertical')

plt.title(f'Point Cloud Average Angular Gap')
plt.xlabel('Integration Time (s)')
plt.ylabel('Point Cloud Average Angular Gap (°)')
plt.legend()
plt.grid(True)
plt.show()

