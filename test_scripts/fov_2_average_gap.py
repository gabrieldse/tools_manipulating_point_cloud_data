import csv
import pandas as pd
import subprocess
import matplotlib.pyplot as plt
import numpy as np

def compute_average_gaps(fov_array):

    def compute_line_gaps(array):
        total_sum_of_averages = 0
        total_lines = 0
        
        for line in array:
            last_non_zero_pos = None
            line_sum_of_gaps = 0
            count_non_zero_elements = 0

            for index, value in enumerate(line):
                if value != 0:
                    if last_non_zero_pos is not None:
                        gap = index - last_non_zero_pos
                        line_sum_of_gaps += gap
                        count_non_zero_elements += 1

                    last_non_zero_pos = index

            if count_non_zero_elements > 1:
                line_average_gap = line_sum_of_gaps / (count_non_zero_elements - 1)
                total_sum_of_averages += line_average_gap
                total_lines += 1

        return total_sum_of_averages / total_lines if total_lines > 0 else None

    # Horizontal gaps
    horizontal_average_gap = compute_line_gaps(fov_array)

    # Vertical gaps
    vertical_average_gap = compute_line_gaps(fov_array.T)


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

    return horizontal_average_gap, vertical_average_gap, (360/314)*horizontal_average_gap, (88/314)*vertical_average_gap

def call_command(number_scans):
    # Define the command and its arguments
    number_scans = number_scans
    command = ["python3", "/home/sqdr/ROSDOCKER/noetic/src/point_lio_ws/data_filtering/test_scripts/fov_heatmap.py", "/home/sqdr/ROSDOCKER/noetic/src/point_lio_ws/data_filtering/data/output_data.csv", str(number_scans),"--no_plot"]

    # Run the command
    try:
        # subprocess.run() executes the command and waits for it to finish
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        
        # Print the standard output and error
        print("Standard Output:", result.stdout)
        print("Standard Error:", result.stderr)
        print("Return Code:", result.returncode)
    
    except subprocess.CalledProcessError as e:
        print("An error occurred while executing the command.")
        print("Error Output:", e.stderr)
        print("Return Code:", e.returncode)

# Example usage
filename = '/home/sqdr/ROSDOCKER/noetic/src/point_lio_ws/data_filtering/data/heatmap/cropped_fov_2D_array.csv'
horizontal_progression = []
vertical_progression = []
scan_number = 60

for item in range(1,scan_number):
    call_command(item)
    df = pd.read_csv(filename,delimiter=',')
    fov_array = df.to_numpy()

    _, _, horizontal_result, vertical_result = compute_average_gaps(fov_array)
    horizontal_progression.append(horizontal_result)
    vertical_progression.append(vertical_result)

print(horizontal_result)
# Correct:
x = np.linspace(0.1,(scan_number-1)/10,scan_number) 
print(x)
plt.plot(x, horizontal_progression, 'r--', linewidth=3, label='horizontal')
plt.plot(x, vertical_progression, 'b--', linewidth=3, label='vertical')

plt.title(f'Point Cloud Average Angular Gap')
plt.xlabel('Integration Time (s)')
plt.ylabel('Point Cloud Average Angular Gap (°)')
plt.legend()
plt.grid(True)
plt.show()

