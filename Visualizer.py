# Requires : pip install pandas seaborn matplotlib plotly scikit-learn
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# Load the data
data = pd.read_csv("summary_output.csv")

# 1. Correlation Heatmap (Static & Interactive)
def correlation_heatmap(data):
    # Compute the correlation matrix
    corr_matrix = data.corr(numeric_only=True)  # Use numeric_only=True to avoid warnings

    # Static Plot using Seaborn
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, cmap='coolwarm', annot=False)
    plt.title("Correlation Heatmap (Static)")
    plt.savefig("correlation_heatmap_static.png")
    plt.show()

    # Interactive Plot using Plotly
    fig = px.imshow(corr_matrix, color_continuous_scale='RdBu_r', title="Correlation Heatmap (Interactive)")
    fig.write_html("correlation_heatmap_interactive.html")
    fig.show()

# 2. Bar Plot for High-Frequency Words (Static & Interactive)
def bar_plot_high_freq_words(data, n=20):
    # Summing the feature columns and getting the top N words/actions
    top_words = data.sum(axis=0).sort_values(ascending=False).head(n)

    # Static Plot
    plt.figure(figsize=(10, 6))
    top_words.plot(kind='bar', color='skyblue')
    plt.title(f"Top {n} Most Frequent Words/Actions (Static)")
    plt.xlabel("Words/Actions")
    plt.ylabel("Frequency")
    plt.xticks(rotation=45)
    plt.savefig("bar_plot_static.png")
    plt.show()

    # Interactive Plot
    fig = px.bar(top_words, x=top_words.index, y=top_words.values, title=f"Top {n} Most Frequent Words/Actions (Interactive)", labels={'x':'Words/Actions', 'y':'Frequency'})
    fig.write_html("bar_plot_interactive.html")
    fig.show()

# 3. Box Plot for Distribution of Selected Features (Static & Interactive)
def box_plot_distribution(data, selected_features):
    # Static Plot using Seaborn
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=data[selected_features])
    plt.title("Box Plot of Selected Features (Static)")
    plt.xticks(rotation=45)
    plt.savefig("box_plot_static.png")
    plt.show()

    # Interactive Plot using Plotly
    fig = px.box(data, y=selected_features, title="Box Plot of Selected Features (Interactive)")
    fig.write_html("box_plot_interactive.html")
    fig.show()

# 4. Word Clustering using PCA (Static & Interactive)
def word_clustering_pca(data, n_components=2):
    # Standardize the data
    features = data.columns[1:]  # Assuming the first column is the 'Word' column
    x = data[features].fillna(0)  # Filling NaN values with 0 for PCA
    scaler = StandardScaler()
    x_scaled = scaler.fit_transform(x)

    # PCA to reduce to n_components dimensions
    pca = PCA(n_components=n_components)
    components = pca.fit_transform(x_scaled)

    # Create a DataFrame with PCA components and the corresponding words
    pca_df = pd.DataFrame(data=components, columns=[f'PC{i+1}' for i in range(n_components)])
    pca_df['Word'] = data['Word']

    # Static Plot using Matplotlib
    plt.figure(figsize=(10, 6))
    plt.scatter(pca_df['PC1'], pca_df['PC2'])
    for i, word in enumerate(pca_df['Word']):
        plt.text(pca_df['PC1'][i], pca_df['PC2'][i], word, fontsize=9)
    plt.title("Word Clustering using PCA (Static)")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.savefig("pca_clustering_static.png")
    plt.show()

    # Interactive Plot using Plotly
    fig = px.scatter(pca_df, x='PC1', y='PC2', text='Word', title="Word Clustering using PCA (Interactive)")
    fig.write_html("pca_clustering_interactive.html")
    fig.show()

# Main function to run all visualizations
def main():
    # 1. Correlation Heatmap
    correlation_heatmap(data)

    # 2. Bar Plot for High-Frequency Words
    bar_plot_high_freq_words(data)

    # 3. Box Plot for Selected Features (Pick a few interesting ones)
    selected_features = ['flap', 'flip', 'feel', 'fall']  # You can customize this list
    box_plot_distribution(data, selected_features)

    # 4. Word Clustering using PCA
    word_clustering_pca(data)

# Run the script
if __name__ == "__main__":
    main()
