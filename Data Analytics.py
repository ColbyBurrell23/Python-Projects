import pandas as pd  # For working with DataFrames


# Load Titanic dataset (update the path as needed)
# Example of full path:
# df = pd.read_csv("C:/Users/YourUsername/Downloads/titanic.csv")
titanic = pd.read_csv("titanic.csv")  # Assumes the file is in the same folder as the script

# Preview the first few rows of the dataset
print(titanic.head())  # Shows the first 5 rows


print(titanic.tail())  # Shows the last 5 rows
print(titanic.sample(10))  # Shows 10 random rows
print(titanic.shape)  # Prints (rows, columns)

# --- 3. Indexing Examples with iloc (integer location) ---

#note: .iloc stands for "integer location" — it's used to access rows and columns by number, not by label. Think of .iloc as saying:  "Give me the thing at row number X and column number Y."
#index implies ROW in Python.

print(titanic.iloc[0:5, :])  # First 5 rows, all columns
print(titanic.iloc[:, :])  # All rows, all columns
print(titanic.iloc[5:, :5])  # From row 5 onward, first 5 columns


