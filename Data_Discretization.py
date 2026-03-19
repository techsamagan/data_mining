import pandas as pd
import numpy as np

# 1. Load the transformed data from the previous step
df = pd.read_csv('transformed_chicago_crimes_2024.csv')

# 2. Equal-Width Binning: Discretizing 'Hour' into 'Time Periods'
# We divide the 24-hour day into 4 equal 6-hour blocks
def get_time_period(hour):
    if 0 <= hour < 6: return 'Late Night'
    elif 6 <= hour < 12: return 'Morning'
    elif 12 <= hour < 18: return 'Afternoon'
    else: return 'Evening'

df['Time_Period'] = df['Hour'].apply(get_time_period)

# 3. Concept Hierarchy Generation: Mapping 'Community Area' to 'City Sector'
# We reduce 77 individual areas into 4 broad geographic sectors
def get_sector(area_num):
    if area_num <= 20: return 'North Side'
    elif area_num <= 40: return 'Central/West'
    elif area_num <= 60: return 'South Side'
    else: return 'Far South/Southwest'

df['City_Sector'] = df['Community Area'].apply(get_sector)

# 4. Binary Discretization: Simplifying 'Location Description'
# We reduce dozens of locations into a simple 'Indoor' vs 'Outdoor' binary
outdoor_locations = ['STREET', 'SIDEWALK', 'ALLEY', 'PARKING LOT / GARAGE (NON-RESIDENTIAL)', 'PARK PROPERTY']
df['Is_Outdoor'] = df['Location Description'].apply(lambda x: 1 if x in outdoor_locations else 0)

# 5. Review the Discretization results
print("--- Discretization Sample ---")
print(df[['Hour', 'Time_Period', 'Community Area', 'City_Sector', 'Is_Outdoor']].head(10))

# 6. Save the final Preprocessed dataset
# This file is now fully Cleaned, Reduced, Transformed, and Discretized!
df.to_csv('final_preprocessed_crimes_2024.csv', index=False)

print("\nSuccess! Final preprocessed data saved to 'final_preprocessed_crimes_2024.csv'")