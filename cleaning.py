import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Load the dataset (Make sure your CSV filename matches exactly)

filename = 'Crimes_-_2024_20260318.csv'
df = pd.read_csv(filename)

print(f"--- Initial Data Load: {len(df)} rows ---")

# 2. Data Cleaning: Handling Missing Values
# We drop rows with missing coordinates because we can't use them for mapping/clustering
df.dropna(subset=['Latitude', 'Longitude', 'District', 'Ward'], inplace=True)

# Fill Location Description with 'UNKNOWN' instead of dropping
df['Location Description'] = df['Location Description'].fillna('UNKNOWN')

# 3. Data Transformation: Parsing Dates
# Using the specific format to avoid the UserWarning and speed up processing
df['Date'] = pd.to_datetime(df['Date'], format='%m/%d/%Y %I:%M:%S %p')

# 4. Data Discretization: Feature Engineering
# Extracting numerical values from the Date for analysis
df['Hour'] = df['Date'].dt.hour
df['Month'] = df['Date'].dt.month
df['Day_of_Week'] = df['Date'].dt.dayofweek  # Monday=0, Sunday=6

# Creating "Time Period" bins as discussed in lecture
def get_time_period(hour):
    if 5 <= hour < 12: return 0  # Morning
    elif 12 <= hour < 17: return 1  # Afternoon
    elif 17 <= hour < 21: return 2  # Evening
    else: return 3  # Night

df['Time_Period_Bin'] = df['Hour'].apply(get_time_period)

# 5. Data Reduction: Attribute Subset Selection
# Drop ID columns and system-generated strings that don't help the model
cols_to_drop = ['ID', 'Case Number', 'IUCR', 'FBI Code', 'Updated On', 'Block', 'Location']
df.drop(columns=cols_to_drop, inplace=True)

# 6. Data Integration/Correlation Analysis (The Math Part)
# Convert Boolean columns to int for Correlation calculation
df['Arrest'] = df['Arrest'].astype(int)
df['Domestic'] = df['Domestic'].astype(int)

print("\n--- Correlation Matrix (Sample) ---")
print(df[['Arrest', 'Domestic', 'Hour', 'District', 'Ward']].corr())

# 7. Save the Cleaned Dataset for Step 3 (Modeling)
df.to_csv('cleaned_chicago_crimes_2024.csv', index=False)

print(f"\n--- Cleaning Complete: {len(df)} rows saved to 'cleaned_chicago_crimes_2024.csv' ---")

# Optional: Generate a Correlation Heatmap for your Report
plt.figure(figsize=(10, 8))
sns.heatmap(df[['Arrest', 'Domestic', 'Hour', 'District', 'Ward', 'Month']].corr(), annot=True, cmap='coolwarm')
plt.title('Feature Correlation Heatmap (Chicago Crime 2024)')
plt.savefig('correlation_heatmap.png')
print("Heatmap saved as 'correlation_heatmap.png'")