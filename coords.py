import matplotlib.pyplot as plt
import pandas as pd

file_path = "output_data.csv"
df = pd.read_csv(file_path, delimiter=',')

# Check the DataFrame to understand its structure
print(df.head())


# df.rename( columns={0 :'index'}, inplace=True )
# print(df.head())
# Access columns
index = df["index"]
azimuth = df['Azimuth']
zenith = df['Zenith']


plt.figure(figsize=(14, 6))

# Plot Azimuth
plt.subplot(1, 2, 1)
plt.plot(df['index'][0:2000], df['Azimuth'][0:2000], 'o', label='Azimuth')
plt.xlabel('Index')
plt.ylabel('Azimuth (degrees)')
plt.title('Index vs Azimuth')
plt.grid(True)
plt.legend()

# Plot Zenith
plt.subplot(1, 2, 2)
plt.plot(df['index'][0:2000], df['Zenith'][0:2000], 'o', label='Zenith', color='orange')
plt.xlabel('Index')
plt.ylabel('Zenith (degrees)')
plt.title('Index vs Zenith')
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.show()