import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import MinMaxScaler

def main():
    df = pd.read_csv('final_preprocessed_crimes_2024.csv')

    # --- Elbow Method to justify K ---
    coords = df[['Lat_MinMax', 'Long_MinMax']].values
    inertias = []
    K_range = range(2, 16)

    print("Running elbow method (K=2 to 15)...")
    for k in K_range:
        km = KMeans(n_clusters=k, random_state=42, n_init=10)
        km.fit(coords)
        inertias.append(km.inertia_)
        print(f"  K={k:2d}  Inertia={km.inertia_:,.0f}")

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(list(K_range), inertias, 'o-', color='#1e50a2', linewidth=2, markersize=7)
    ax.axvline(x=10, color='red', linestyle='--', linewidth=1.5, label='Selected K=10')
    ax.fill_between(list(K_range), inertias, alpha=0.1, color='#1e50a2')
    ax.set_xlabel('Number of Clusters (K)', fontsize=12)
    ax.set_ylabel('Within-Cluster Sum of Squares (Inertia)', fontsize=12)
    ax.set_title('Elbow Method for Optimal K\nChicago Crime Geographic Clustering', fontsize=13, fontweight='bold')
    ax.set_xticks(list(K_range))
    ax.legend()
    plt.tight_layout()
    plt.savefig('elbow_curve.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: elbow_curve.png")

    # --- Enhanced K-Means (K=10) with geographic + temporal features ---
    scaler = MinMaxScaler()
    enhanced_features = scaler.fit_transform(
        df[['Latitude', 'Longitude', 'Hour', 'Is_Outdoor']]
    )

    kmeans = KMeans(n_clusters=10, random_state=42, n_init=10)
    df['Cluster'] = kmeans.fit_predict(enhanced_features)

    # Cluster profile: crime count, avg hour, arrest rate, outdoor rate
    profile = df.groupby('Cluster').agg(
        Crime_Count=('Arrest', 'count'),
        Arrest_Rate=('Arrest', 'mean'),
        Avg_Hour=('Hour', 'mean'),
        Outdoor_Rate=('Is_Outdoor', 'mean'),
        Avg_Lat=('Latitude', 'mean'),
        Avg_Long=('Longitude', 'mean'),
    ).round(3)
    profile['Arrest_Rate_Pct'] = (profile['Arrest_Rate'] * 100).round(1)
    profile = profile.sort_values('Crime_Count', ascending=False)

    print("\nCluster Profiles:")
    print(profile[['Crime_Count', 'Arrest_Rate_Pct', 'Avg_Hour', 'Outdoor_Rate']].to_string())

    # --- Chart 1: Enhanced cluster map ---
    fig, ax = plt.subplots(figsize=(10, 13))
    palette = sns.color_palette('tab10', 10)
    for cluster_id in range(10):
        mask = df['Cluster'] == cluster_id
        ax.scatter(
            df.loc[mask, 'Longitude'], df.loc[mask, 'Latitude'],
            color=palette[cluster_id], s=0.5, alpha=0.3, label=f'Cluster {cluster_id}'
        )

    centers = df.groupby('Cluster')[['Latitude', 'Longitude']].mean()
    ax.scatter(centers['Longitude'], centers['Latitude'],
               c='red', marker='X', s=250, zorder=5, label='Hotspot Centers', edgecolors='black', linewidths=0.5)

    ax.set_xlabel('Longitude', fontsize=11)
    ax.set_ylabel('Latitude', fontsize=11)
    ax.set_title('Enhanced K-Means Crime Hotspot Clusters (K=10)\nFeatures: Location + Time-of-Day + Indoor/Outdoor', fontsize=12, fontweight='bold')
    ax.legend(loc='upper right', markerscale=5, fontsize=8)
    plt.tight_layout()
    plt.savefig('crime_clusters.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: crime_clusters.png (enhanced)")

    # --- Chart 2: Cluster profiles bar chart ---
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    sorted_profile = profile.sort_index()

    axes[0].bar(sorted_profile.index, sorted_profile['Crime_Count'],
                color=palette, edgecolor='white')
    axes[0].set_xlabel('Cluster ID', fontsize=11)
    axes[0].set_ylabel('Number of Crimes', fontsize=11)
    axes[0].set_title('Crime Count per Cluster', fontsize=12, fontweight='bold')
    axes[0].set_xticks(sorted_profile.index)

    axes[1].bar(sorted_profile.index, sorted_profile['Arrest_Rate_Pct'],
                color=palette, edgecolor='white')
    axes[1].set_xlabel('Cluster ID', fontsize=11)
    axes[1].set_ylabel('Arrest Rate (%)', fontsize=11)
    axes[1].set_title('Arrest Rate per Cluster', fontsize=12, fontweight='bold')
    axes[1].set_xticks(sorted_profile.index)
    axes[1].axhline(df['Arrest'].mean() * 100, color='red', linestyle='--',
                    label=f'Overall avg ({df["Arrest"].mean()*100:.1f}%)')
    axes[1].legend()

    plt.suptitle('K-Means Cluster Analysis — Chicago Crime 2024', fontsize=13, fontweight='bold', y=1.01)
    plt.tight_layout()
    plt.savefig('cluster_profiles.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: cluster_profiles.png")

    return profile

if __name__ == '__main__':
    main()
