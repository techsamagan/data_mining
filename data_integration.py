import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Chicago Community Area demographics (2020 Census + ACS estimates)
# Source: City of Chicago Data Portal - Community Area boundaries & census data
COMMUNITY_DEMOGRAPHICS = {
    1:  ("Rogers Park",           54991),
    2:  ("West Ridge",            71942),
    3:  ("Uptown",                58057),
    4:  ("Lincoln Square",        39533),
    5:  ("North Center",          37588),
    6:  ("Lake View",             98514),
    7:  ("Lincoln Park",          67464),
    8:  ("Near North Side",       99617),
    9:  ("Edison Park",           11525),
    10: ("Norwood Park",          37023),
    11: ("Jefferson Park",        27573),
    12: ("Forest Glen",           18827),
    13: ("North Park",            18491),
    14: ("Albany Park",           51542),
    15: ("Portage Park",          65544),
    16: ("Irving Park",           60169),
    17: ("Dunning",               42164),
    18: ("Montclare",             13426),
    19: ("Belmont Cragin",        80484),
    20: ("Hermosa",               25860),
    21: ("Avondale",              38609),
    22: ("Logan Square",          72459),
    23: ("Humboldt Park",         56323),
    24: ("West Town",             84335),
    25: ("Austin",               100309),
    26: ("West Garfield Park",    17433),
    27: ("East Garfield Park",    19992),
    28: ("Near West Side",        53258),
    29: ("North Lawndale",        34794),
    30: ("South Lawndale",        73595),
    31: ("Lower West Side",       33756),
    32: ("Loop",                  45396),
    33: ("Near South Side",       24271),
    34: ("Armour Square",         14045),
    35: ("Douglas",               20690),
    36: ("Oakland",                5918),
    37: ("Fuller Park",            2876),
    38: ("Grand Boulevard",       21929),
    39: ("Kenwood",               18363),
    40: ("Washington Park",       11717),
    41: ("Hyde Park",             30757),
    42: ("Woodlawn",              25983),
    43: ("South Shore",           49767),
    44: ("Chatham",               30585),
    45: ("Avalon Park",           10044),
    46: ("South Chicago",         28640),
    47: ("Burnside",               2916),
    48: ("Calumet Heights",       13091),
    49: ("Roseland",              39954),
    50: ("Pullman",                7325),
    51: ("South Deering",         13673),
    52: ("East Side",             23042),
    53: ("West Pullman",          27993),
    54: ("Riverdale",              6560),
    55: ("Hegewisch",             10027),
    56: ("Garfield Ridge",        35090),
    57: ("Archer Heights",        14641),
    58: ("Brighton Park",         44148),
    59: ("McKinley Park",         15812),
    60: ("Bridgeport",            33322),
    61: ("New City",              43169),
    62: ("West Elsdon",           17467),
    63: ("Gage Park",             39805),
    64: ("Clearing",              22038),
    65: ("West Lawn",             42120),
    66: ("Chicago Lawn",          55015),
    67: ("West Englewood",        28715),
    68: ("Englewood",             24369),
    69: ("Greater Grand Crossing",32602),
    70: ("Ashburn",               39147),
    71: ("Auburn Gresham",        45076),
    72: ("Beverly",               20777),
    73: ("Washington Heights",    26606),
    74: ("Mount Greenwood",       18628),
    75: ("Morgan Park",           22922),
    76: ("O'Hare",                12756),
    77: ("Edgewater",             56521),
}

def main():
    df = pd.read_csv('final_preprocessed_crimes_2024.csv')

    # Build demographics lookup table
    demo_df = pd.DataFrame.from_dict(
        COMMUNITY_DEMOGRAPHICS, orient='index',
        columns=['Area_Name', 'Population']
    ).reset_index().rename(columns={'index': 'Community Area'})

    # Merge demographics into crime data
    df = df.merge(demo_df, on='Community Area', how='left')

    # Crimes per 1,000 residents (crime rate) by area
    area_crimes = df.groupby('Community Area').agg(
        Crime_Count=('Arrest', 'count'),
        Area_Name=('Area_Name', 'first'),
        Population=('Population', 'first')
    ).reset_index()

    area_crimes['Crime_Rate_Per_1k'] = (area_crimes['Crime_Count'] / area_crimes['Population'] * 1000).round(1)
    area_crimes = area_crimes.sort_values('Crime_Rate_Per_1k', ascending=False)

    print("Top 10 Community Areas by Crime Rate (per 1,000 residents):")
    print(area_crimes[['Area_Name', 'Crime_Count', 'Population', 'Crime_Rate_Per_1k']].head(10).to_string(index=False))

    # --- Chart 1: Top 20 areas by crime rate ---
    top20 = area_crimes.head(20)
    fig, ax = plt.subplots(figsize=(12, 7))
    bars = ax.barh(top20['Area_Name'][::-1], top20['Crime_Rate_Per_1k'][::-1],
                   color=plt.cm.RdYlGn_r(top20['Crime_Rate_Per_1k'][::-1] / top20['Crime_Rate_Per_1k'].max()))
    ax.set_xlabel('Crimes per 1,000 Residents', fontsize=12)
    ax.set_title('Top 20 Chicago Community Areas\nby Crime Rate per 1,000 Residents (2024)', fontsize=13, fontweight='bold')
    ax.axvline(area_crimes['Crime_Rate_Per_1k'].mean(), color='navy', linestyle='--', linewidth=1.5,
               label=f'City Average ({area_crimes["Crime_Rate_Per_1k"].mean():.1f})')
    ax.legend()
    plt.tight_layout()
    plt.savefig('crime_rate_by_area.png', dpi=150, bbox_inches='tight')
    plt.close()

    # --- Chart 2: Crime count vs population scatter ---
    fig, ax = plt.subplots(figsize=(10, 7))
    scatter = ax.scatter(
        area_crimes['Population'], area_crimes['Crime_Count'],
        c=area_crimes['Crime_Rate_Per_1k'], cmap='RdYlGn_r', s=60, alpha=0.8
    )
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Crime Rate per 1,000 residents')

    # Label top 5 highest crime-rate areas
    for _, row in area_crimes.head(5).iterrows():
        ax.annotate(row['Area_Name'], (row['Population'], row['Crime_Count']),
                    textcoords='offset points', xytext=(5, 3), fontsize=7)

    ax.set_xlabel('Community Area Population (2020 Census)', fontsize=12)
    ax.set_ylabel('Total Crime Count (2024)', fontsize=12)
    ax.set_title('Population vs Crime Count by Community Area\n(Color = Crime Rate per 1,000 residents)', fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig('population_vs_crime.png', dpi=150, bbox_inches='tight')
    plt.close()

    # Save the integrated dataset
    df.to_csv('integrated_chicago_crimes_2024.csv', index=False)

    print("\nData Integration complete!")
    print(f"  Merged population data for {demo_df.shape[0]} community areas")
    print(f"  Highest crime rate area: {area_crimes.iloc[0]['Area_Name']} ({area_crimes.iloc[0]['Crime_Rate_Per_1k']} per 1k)")
    print(f"  Lowest crime rate area:  {area_crimes.iloc[-1]['Area_Name']} ({area_crimes.iloc[-1]['Crime_Rate_Per_1k']} per 1k)")
    print("  Saved: integrated_chicago_crimes_2024.csv")
    print("  Saved: crime_rate_by_area.png")
    print("  Saved: population_vs_crime.png")

    return area_crimes

if __name__ == '__main__':
    main()
