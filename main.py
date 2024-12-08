from flask import Flask, request, render_template, jsonify
import os
from src.utils import fetch_pdf_from_url, extract_incidents_from_pdf
import pandas as pd
import plotly.express as px
from sklearn.cluster import DBSCAN,KMeans
from sklearn.preprocessing import StandardScaler,LabelEncoder
import numpy as np
import googlemaps

app = Flask(__name__, template_folder="src/templates")

UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize Google Maps API client
GMAPS_API_KEY = "AIzaSyBW8jFyrA7pc3NfKdZMMvnaDhWKRrLrEJY"
gmaps = googlemaps.Client(key=GMAPS_API_KEY)

# Initialize global dataframe
df = pd.DataFrame()

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    """Handle PDF uploads and process them."""
    global df

    files = request.files.getlist('files')
    if not files:
        return jsonify({'error': 'No files provided.'}), 400

    for file in files:
        save_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(save_path)

        # Extract data and append to global dataframe
        incidents = extract_incidents_from_pdf(save_path)
        df = pd.concat([df, pd.DataFrame(incidents)], ignore_index=True)

    return jsonify({'message': 'Files uploaded and processed successfully.'})

@app.route('/fetch', methods=['POST'])
def fetch():
    """Handle fetching PDFs from multiple URLs and process them."""
    global df

    urls = request.json.get('urls')
    if not urls:
        return jsonify({'error': 'No URLs provided.'}), 400

    for url in urls:
        save_path = os.path.join(UPLOAD_FOLDER, os.path.basename(url))
        fetch_pdf_from_url(url, save_path)

        # Extract data and append to global dataframe
        incidents = extract_incidents_from_pdf(save_path)
        df = pd.concat([df, pd.DataFrame(incidents)], ignore_index=True)

    return jsonify({'message': 'Files fetched and processed successfully.'})

@app.route('/visualize', methods=['GET'])
def visualize():
    """Generate visualizations from incident data."""
    if df.empty:
        return jsonify({'error': 'No data available for visualization.'}), 400

    # Visualization 1: Bar Chart of Nature vs Frequency
    if 'Nature' in df.columns:
        nature_counts = df['Nature'].value_counts().reset_index()
        nature_counts.columns = ['Incident Type', 'Frequency']
        bar_chart = px.bar(
            nature_counts,
            x='Incident Type',
            y='Frequency',
            labels={'Incident Type': 'Incident Type', 'Frequency': 'Frequency'},
            title="Incident Frequency Comparison"
        )
    else:
        bar_chart = None

    # Visualization 2: Time Series Line Graph (one per date)
    time_series_graphs = []
    if 'DateTime' in df.columns:
        df['DateTime'] = pd.to_datetime(df['DateTime'], errors='coerce')
        grouped = df.groupby(df['DateTime'].dt.date)

        for date, group in grouped:
            daily_data = group.groupby(group['DateTime'].dt.hour)['Nature'].count()
            time_series = px.line(
                daily_data.reset_index(),
                x='DateTime',
                y='Nature',
                labels={'DateTime': 'Hour of Day', 'Nature': 'Incident Count'},
                title=f"Incident Trends for {date}"
            )
            time_series_graphs.append(time_series.to_json())

    # Visualization 3: Improved Clustering of Location and Nature
    clustering_map_data = []

    if 'Location' in df.columns:
        location_coords = []

        for _, row in df.iterrows():
            location = f"{row['Location']}, Norman, OK"
            geocode_result = gmaps.geocode(location)
            if geocode_result:
                lat = geocode_result[0]['geometry']['location']['lat']
                lon = geocode_result[0]['geometry']['location']['lng']
                location_coords.append({
                    'lat': lat,
                    'lon': lon,
                    'nature': row['Nature'],
                    'datetime': row['DateTime'],
                    'location': location
                })

        location_df = pd.DataFrame(location_coords)

        if not location_df.empty and len(location_df) >= 2:
            coords = location_df

            # Standardize coordinates to improve clustering
            scaler = StandardScaler()
            standardized_coords = scaler.fit_transform(coords[['lat', 'lon']])

            # Apply DBSCAN clustering with adjusted parameters
            clustering_model = DBSCAN(eps=0.5, min_samples=5)
            clusters = clustering_model.fit_predict(standardized_coords)
            coords['cluster'] = clusters

            for _, row in coords.iterrows():
                clustering_map_data.append({
                    'lat': row['lat'],
                    'lon': row['lon'],
                    'cluster': int(row['cluster']) if row['cluster'] != -1 else 'Noise',
                    'popup_info': f"Nature: {row['nature']}<br>Date/Time: {row['datetime']}<br>Cluster: {row['cluster']}"
                })

    # Visualization 4: Clustering Based on Nature and Time
    nature_time_clusters = []
    if 'Nature' in df.columns and 'DateTime' in df.columns:
        df['DateTime'] = pd.to_datetime(df['DateTime'], errors='coerce')
        df['Hour'] = df['DateTime'].dt.hour

        # Encode Nature as numeric values for clustering
        le = LabelEncoder()
        df['NatureEncoded'] = le.fit_transform(df['Nature'])

        grouped = df.groupby(df['DateTime'].dt.date)
        for date, group in grouped:
            if len(group) >= 5:  # Ensure enough samples for clustering
                kmeans = KMeans(n_clusters=min(5, len(group)), random_state=42)
                group['Cluster'] = kmeans.fit_predict(group[['NatureEncoded', 'Hour']])

                cluster_fig = px.scatter(
                    group,
                    x='Hour',
                    y='NatureEncoded',
                    color='Cluster',
                    hover_data=['Nature', 'DateTime'],
                    labels={'Hour': 'Hour of Day', 'NatureEncoded': 'Incident Type (Encoded)'},
                    title=f"Clustering of Incidents for {date}"
                )
                nature_time_clusters.append(cluster_fig.to_json())

    # Visualization 5: Clustering Based on Location and Nature
    location_nature_cluster = None
    if 'Location' in df.columns and 'Nature' in df.columns:
        df['Location'] = df['Location'] + ", Norman, OK"  # Append "Norman, OK" to each location
        location_coords = []

        for location in df['Location'].unique():
            try:
                geocode_result = gmaps.geocode(location)
                if geocode_result:
                    latlng = geocode_result[0]['geometry']['location']
                    location_coords.append((location, latlng['lat'], latlng['lng']))
            except Exception as e:
                print(f"Geocoding error: {e}")

        location_df = pd.DataFrame(location_coords, columns=['location', 'lat', 'lng'])

        if not location_df.empty:
            cluster_df = df.merge(location_df, left_on='Location', right_on='location')
            if len(cluster_df) >= 5:
                kmeans = KMeans(n_clusters=3, random_state=42)
                cluster_df['Cluster'] = kmeans.fit_predict(cluster_df[['lat', 'lng']])

                fig_cluster = px.scatter(
                    cluster_df,
                    x='lng',
                    y='lat',
                    color='Cluster',
                    hover_data=['Nature', 'DateTime'],
                    title='Clustering of Incidents Based on Location and Nature',
                    labels={'lng': 'Longitude', 'lat': 'Latitude'}
                )
                location_nature_cluster = fig_cluster.to_json()

    return jsonify({
        'bar_chart': bar_chart.to_json() if bar_chart else None,
        'time_series': time_series_graphs if time_series_graphs else None,
        'clustering_map': clustering_map_data,
        'nature_time_clusters': nature_time_clusters if nature_time_clusters else None,
        'location_nature_clusters': location_nature_cluster if location_nature_cluster else None
    })

if __name__ == '__main__':
    app.run(debug=True)
