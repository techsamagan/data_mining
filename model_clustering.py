import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load the cleaned data
df = pd.read_csv('cleaned_chicago_crimes_2024.csv')

# 2. Select features for clustering (Coordinates)
coords = df[['Latitude', 'Longitude']]

# 3. Apply K-Means
# We will look for 10 main hotspots (K=10)
kmeans = KMeans(n_clusters=10, random_state=42)
df['Cluster'] = kmeans.fit_predict(coords)

# 4. Visualize the Hotspots
plt.figure(figsize=(10, 12))
sns.scatterplot(x='Longitude', y='Latitude', hue='Cluster', data=df, palette='viridis', s=1, alpha=0.5)
plt.scatter(kmeans.cluster_centers_[:, 1], kmeans.cluster_centers_[:, 0], 
            c='red', marker='X', s=200, label='Hotspot Centers')

plt.title('Chicago Crime Hotspots 2024 (K-Means Clustering)')
plt.legend()
plt.savefig('crime_clusters.png')
print("Model complete! Hotspot map saved as 'crime_clusters.png'")