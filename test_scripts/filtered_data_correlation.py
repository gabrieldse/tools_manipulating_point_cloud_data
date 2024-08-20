import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import StringIO

# Data from the CSV provided by the user
data = """dist,std,lx,reflex,orientation,gx,gy,gz,s
2.60,1.91,70.6,0,u,0,0,0,w
4.25,1.11,74.7,0,f,0,0,0,wb
4.22,1.34,11.0,0,f,0,0,0,wb
7.03,2.87,71.9,0,f,0,0,0,w
7.37,4.85,72.2,0,u,0,0,0,w
14.10,5.25,73.5,0,u,0,0,0,w
14.10,2.78,73.3,0,f,0,0,0,w
19.85,4.81,11.4,0,f,0,0,0,w
19.95,7.96,76,0,u,0,0,0,w
17.17,4.95,17.17,0,f,0,0,0,w
17.64,6.86,76,0,u,0,0,0,w
29.03,7,71.6,0,f,0,0,0,w
34.81,12.26,9.8,0,u,0,0,0,w
36.72,10.29,71.9,0,f,0,0,0,w
37.40,9.74,8,0,f,0,0,0,w"""

# Read the CSV data
df = pd.read_csv(StringIO(data))

# Define the color map based on non-numeric columns
color_map = {'u': 'blue', 'f': 'orange', 'w': 'green', 'wb': 'red'}

# Add a color column to the DataFrame
df['color'] = df['orientation'].map(color_map)

# Plot pairplot with seaborn
'''
The main diagonal is: kernel density estimation (KDE)
'''
sns.pairplot(df, vars=['dist', 'std', 'lx'], hue='orientation', palette=color_map)


# Additionally, plot correlation matrix heatmap
corr_matrix = df[['dist', 'std', 'lx']].corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Matrix')
plt.show()