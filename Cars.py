#Question 2#
import pandas as pd

# Load the CSV file
df = pd.read_csv("CARS.csv")

# Group by 'Origin' and count the number of cars in each group
origin_counts = df.groupby('Origin').size().reset_index(name='Car Count')

# Display the result
print(origin_counts)

#Question 3#
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
df = pd.read_csv("CARS.csv")

# Group by 'Origin' and count the number of cars in each group
origin_counts = df.groupby('Origin').size().reset_index(name='Car Count')

# Create the bar chart
plt.figure(figsize=(8, 6))
bars = plt.bar(origin_counts['Origin'], origin_counts['Car Count'])

# Add values on top of each bar
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + 2, str(height),
             ha='center', va='bottom', fontsize=10)

# Add titles and labels
plt.title('Number of Cars by Origin')
plt.xlabel('Origin')
plt.ylabel('Number of Cars')
plt.tight_layout()
plt.show()

#Question 4#
import pandas as pd

# Load the CSV file
df = pd.read_csv("CARS.csv")

# Count missing values in each column
missing_values = df.isnull().sum().reset_index()
missing_values.columns = ['Column', 'Missing Values']

# Display the result
print(missing_values)

#Question 5#
import pandas as pd

# Load the CSV file
df = pd.read_csv("CARS.csv")

# Remove the row where 'Weight' is missing
df = df[df['Weight'].notnull()]

# Optional: Confirm the row is deleted
print(df['Weight'].isnull().sum())  # Should print 0

