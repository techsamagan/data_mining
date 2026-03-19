import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Load the cleaned data
df = pd.read_csv('cleaned_chicago_crimes_2024.csv')

# 2. Select numerical features for Reduction
# We use location data because they are highly correlated (as seen in your heatmap)
features = ['Latitude', 'Longitude', 'District', 'Ward']
x = df[features]

# 3. Standardization (Crucial for PCA)
# PCA is sensitive to variances, so we must scale the data first
x_scaled = StandardScaler().fit_transform(x)

# 4. Apply PCA
# We reduce 4 columns down to 2 "Principal Components"
pca = PCA(n_components=2)
principalComponents = pca.fit_transform(x_scaled)

# Create a new DataFrame with the PCA results
pca_df = pd.DataFrame(data = principalComponents, 
                      columns = ['Principal Component 1', 'Principal Component 2'])

# 5. Visualize the Reduction
plt.figure(figsize=(10, 7))
sns.scatterplot(x='Principal Component 1', y='Principal Component 2', 
                data=pca_df, s=1, alpha=0.3)

plt.title('Data Reduction: PCA of Chicago Crime Locations (2024)')
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.2%} variance)')
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.2%} variance)')
plt.savefig('pca_reduction_plot.png')

print("PCA Complete!")
print(f"Total Variance Explained by 2 components: {sum(pca.explained_variance_ratio_):.2%}")