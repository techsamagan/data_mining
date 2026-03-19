import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler

# 1. Load the CLEANED data from your previous step
df = pd.read_csv('cleaned_chicago_crimes_2024.csv')

# 2. Min-Max Normalization (Scaling to [0, 1])
# Essential for Clustering (K-Means) so Lat/Long have equal weight
min_max_scaler = MinMaxScaler()
df[['Lat_MinMax', 'Long_MinMax']] = min_max_scaler.fit_transform(df[['Latitude', 'Longitude']])

# 3. Z-Score Normalization (Standardization)
# Good for PCA and Regression models
std_scaler = StandardScaler()
df[['District_Z', 'Ward_Z']] = std_scaler.fit_transform(df[['District', 'Ward']])

# 4. Verify the results
print("--- Min-Max Transformation (Latitude) ---")
print(f"Min: {df['Lat_MinMax'].min()}, Max: {df['Lat_MinMax'].max()}")

print("\n--- Z-Score Transformation (District) ---")
print(f"Mean: {round(df['District_Z'].mean(), 2)}, StdDev: {df['District_Z'].std()}")

# 5. Save the transformed data for your Model
df.to_csv('transformed_chicago_crimes_2024.csv', index=False)
print("\nSuccess! Transformed data saved to 'transformed_chicago_crimes_2024.csv'")