# why : to have a more realisic scan patter to the simulator: for unitree (and later mid 360 from the datasets)

# current problem: the values i converted are betwen 1 and 2 so its is definetly not correct

# bag 2 csv 'or data frame) (x, y, z, intensity, ring)


# df + 2 polar (add two columns)
# plot polar
# 
# analyse it, generate same patter,  


# BAG 2 DF
from pathlib import Path
from rosbags.highlevel import AnyReader
from rosbags.typesys import Stores, get_typestore

import inspect
import struct
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

bagpath = Path('/home/gabriel/Desktop/uniburger/data/unilidar-2023-09-22-12-42-04.bag')

# Create a type store to use if the bag has no message definitions.
typestore = get_typestore(Stores.ROS1_NOETIC)

def print_point_data(data):
    print("Point 1 start -----")
    
    for field, offset in offsets.items():
        data_type = data_types[field]
        size = struct.calcsize(data_type)
        field_data = data[offset:offset + size]
        
        if data_type == 'H':  # UINT16
            value = struct.unpack('<H', field_data)[0]
        else:  # FLOAT32
            value = struct.unpack('<f', field_data)[0]
        
        print(f"{field} = {value}")


# Initialize lists to store data
x_values = []
y_values = []
z_values = []
intensity_values = []
counter_scans = 0

indices = []
azimuth_angles = []
zenith_angles = []

# Create reader instance and open for reading.
with AnyReader([bagpath], default_typestore=typestore) as reader:
    connections = [x for x in reader.connections if x.topic == '/unilidar/cloud']
    for connection, timestamp, rawdata in reader.messages(connections=connections):
        msg = reader.deserialize(rawdata, connection.msgtype)
        # print(f" ~~~~~~~~~~ oia o comeco da data: {len(msg.data)}\n")
        # print(f"X (F32): {struct.unpack('<f', bytes(msg.data[0:4]))[0]}")
        # print(f"Y (F32): {struct.unpack('<f', bytes(msg.data[4:8]))[0]}")
        # print(f"Z (F32): {struct.unpack('<f', bytes(msg.data[8:12]))[0]}")
        # print(f"IDK (F32): {struct.unpack('<f', bytes(msg.data[12:16]))[0]}")
        # print(f"intensity (F32): {struct.unpack('<f', bytes(msg.data[16:20]))[0]}")
        # print(f"ring (Int16): {struct.unpack('<H', bytes(msg.data[20:22]))[0]}")
        # print(f"time (F32): {struct.unpack('<f', bytes(msg.data[24:28]))[0]}")

        #Extract data fields

        if counter_scans >= 2080*10*10: # 10s
            break
        start = 0
        for i in range(len(msg.data) // 32):
            print("Processing chunk", i/2000)
            
            # Extract each field from the chunk
            x = struct.unpack('<f', bytes(msg.data[start:start+4]))[0]
            y = struct.unpack('<f', bytes(msg.data[start+4:start+8]))[0]
            z = struct.unpack('<f', bytes(msg.data[start+8:start+12]))[0]
            intensity = struct.unpack('<f', bytes(msg.data[start+16:start+20]))[0]
            # Note: You should handle 'ring' and 'time' if needed
            
            # Update start index for next chunk
            start += 32
            
            # Append extracted values to lists
            x_values.append(x)
            y_values.append(y)
            z_values.append(z)
            intensity_values.append(intensity)

             # Compute azimuth and zenith
            r = np.sqrt(x**2 + y**2 + z**2)
            azimuth = np.degrees(np.arctan2(y, x)) % 360  # Ensure azimuth is between 0 and 360 degrees
            zenith = np.degrees(np.arccos(z / r)) if r != 0 else 0  # Ensure zenith is between 0 and 180 degrees

            azimuth_angles.append(azimuth)
            zenith_angles.append(zenith)

            print("Saved values:", x, y, z, intensity)
            counter_scans = counter_scans+1 # 100 = 10s
            
            # Increment message counter
            

        
        

        
        # for i in inspect.getmembers(msg):
        #     if not i[0].startswith('_'):
        #             if not inspect.ismethod(i[1]): 
        #                 print(f"look at this: {i} \n")

              
        
        # for field in msg.fields:
        #     if field.name == 'intensity':
        #         intensity_field = field
        #     elif field.name == 'ring':
        #         ring_field = field

        # print("Intensity Field:", intensity_field)
        # print("Ring Field:", ring_field)
        # field_value = getattr(msg.fields, x, None)
        # print(field_value)

        df = pd.DataFrame({
            'x': x_values,
            'y': y_values,
            'z': z_values,
            'intensity': intensity_values,
            'Azimuth': azimuth_angles,
            'Zenith': zenith_angles
        })

        
        
print(f"we had {counter_scans/2080} messages \n")

# Save DataFrame to CSV
df.to_csv('output_data.csv', index=True)
print("Data saved to output_data.csv")

plt.figure(figsize=(14, 6))

# Plot Azimuth
plt.subplot(1, 2, 1)
plt.plot(df['Index'], df['Azimuth'], 'o', label='Azimuth')
plt.xlabel('Index')
plt.ylabel('Azimuth (degrees)')
plt.title('Index vs Azimuth')
plt.grid(True)
plt.legend()

# Plot Zenith
plt.subplot(1, 2, 2)
plt.plot(df['Index'], df['Zenith'], 'o', label='Zenith', color='orange')
plt.xlabel('Index')
plt.ylabel('Zenith (degrees)')
plt.title('Index vs Zenith')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()




# troubleshooting
    # no pip install -> python3 -m ensurepip
    #  these messages are littleendian so the number 12.345 WOULD BE writeen 5 then 4 then 3 then 2 then 1...