import pandas as pd

# 1. Load the dataset

df = pd.read_csv('Crimes_-_2024_20260318.csv')
# 2. Check for missing values
print("Missing values per column:\n", df.isnull().sum())

# 3. Drop rows where essential location data is missing
# (Since we have 250k+ rows, losing a few hundred won't hurt your model)
df.dropna(subset=['Latitude', 'Longitude', 'District'], inplace=True)

# 4. Convert 'Date' to datetime objects
df['Date'] = pd.to_datetime(df['Date'])

# 5. Data Reduction: Drop columns that don't help the model
# (Attribute Subset Selection)
cols_to_drop = ['Case Number', 'IUCR', 'FBI Code', 'Updated On', 'Block']
df.drop(columns=cols_to_drop, inplace=True)

# 6. Fill minor missing values with a placeholder
df['Location Description'] = df['Location Description'].fillna('UNKNOWN')

print(f"Cleaning complete. Remaining rows: {len(df)}")