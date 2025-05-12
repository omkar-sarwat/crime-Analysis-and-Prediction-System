import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import folium
from folium.plugins import HeatMap
import geopandas as gpd

def perform_clustering(data, n_clusters=10):
    """
    Perform K-Means clustering on the crime locations.
    """
    # Standardize the data
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(data)
    
    # Perform K-Means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    clusters = kmeans.fit_predict(scaled_data)
    
    # Get cluster centers
    cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
    
    return clusters, cluster_centers

def create_heatmap(df, cluster_centers):
    """
    Create an interactive heatmap using Folium.
    """
    # Create a base map centered on Chicago
    m = folium.Map(location=[41.8781, -87.6298], zoom_start=11)
    
    # Add heatmap layer
    heat_data = [[row['Latitude'], row['Longitude']] for index, row in df.iterrows()]
    HeatMap(heat_data).add_to(m)
    
    # Add cluster centers as markers
    for i, center in enumerate(cluster_centers):
        folium.CircleMarker(
            location=[center[0], center[1]],
            radius=10,
            color='red',
            fill=True,
            popup=f'Hotspot {i+1}'
        ).add_to(m)
    
    return m

def analyze_hotspot_patterns(df, clusters):
    """
    Analyze patterns within each hotspot.
    """
    df['Cluster'] = clusters
    
    hotspot_patterns = {}
    for cluster in range(len(np.unique(clusters))):
        cluster_data = df[df['Cluster'] == cluster]
        
        patterns = {
            'total_crimes': len(cluster_data),
            'most_common_crime': cluster_data['Primary Type'].mode()[0],
            'peak_hour': cluster_data['Hour'].mode()[0],
            'peak_day': cluster_data['DayOfWeek'].mode()[0]
        }
        
        hotspot_patterns[f'Hotspot_{cluster+1}'] = patterns
    
    return hotspot_patterns 