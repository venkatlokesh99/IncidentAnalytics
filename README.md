# Incident Data Analytics
## Project Overview
This project provides a comprehensive solution for analyzing and visualizing incident data using various methods and technologies. It includes functionality for:

1. Uploading or fetching incident PDF files via URLs.
2. Extracting incident data (e.g., Date/Time, Location, Nature) from PDFs.
3. Visualizing the extracted data with multiple visualizations:
   - **Bar Chart**: Displays the frequency of different incident types.
   - **Time Series Line Graph**: Shows trends of incidents across different hours for each date.
   - **Clustering Map**: Visualizes incidents based on geographical location and their clusters.
   - **Nature and Time Clustering**: Groups incidents by their type and time.
   - **Location and Nature Clustering**: Groups incidents by their location and nature.

The application uses Flask for the backend, Plotly for visualizations, Leaflet for interactive maps, and Google Maps API for geocoding.

## Directory Structure
```bash
project/
├── README.md
├── main.py
├── src/
│   ├── utils.py
│   ├── templates/
│   │   └── index.html
├── tests/
│   ├── test_index_page.py
│   ├── test_upload_no_file.py
│   ├── test_upload_file.py
│   ├── test_fetch_no_urls.py
│   ├── test_visualize_empty_data.py
├── uploads/
├── setup.cfg
├── setup.py
```


---

## Installation and Setup

### Prerequisites
1. Python 3.10 or higher.
2. Virtual environment (optional but recommended).
3. API key for Google Maps Geocoding API.

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/venkatlokesh99/cis6930fa24-project3.git
   cd cis6930fa24-project3

2. Set up a virtual environment:
   ```bash
   pipenv install -e .
   pipenv shell
4. Update the Google Maps API key in main.py:
   ```bash
   GMAPS_API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"
6. Run the application:
   ```bash
   pipenv run python main.py
8. Access the application in your browser at:
   ```bash
   http://127.0.0.1:5000
   ```
## Video
[https://youtu.be/LPbzhbLv-ig](https://youtu.be/1HbkLU7mCUs)

## Usage

### Upload PDFs
- Navigate to the upload section on the homepage.
- Select multiple PDF files for upload and click Upload and Visualize.

### Fetch PDFs from URLs
- Enter URLs for PDF files in the provided textarea seperated by comma(,).
- Click the "Fetch and Visualize" button to process data.

### View Visualizations
- Access bar charts, time series graphs, and clustering maps.
- Interactive map visualizations provide popups with incident details.

## Files

### `utils.py`
- **Purpose**: Contains helper functions for PDF extraction, fetching files, and data preprocessing.
- **Functions**:
  1. **`fetch_pdf_from_url`**: Downloads PDF files from given URLs and saves them locally.
  2. **`extract_incidents_from_pdf`**: Extracts incident data (Date/Time, Location, Nature, etc.) from uploaded PDF files.
  3. **`process_incident_line`**: Cleans and processes raw lines of text extracted from PDFs.
  4. **`extract_fields`**: Splits lines into structured fields for further processing.

### `index.html`
- **Purpose**: Frontend of the application.
- **Features**:
  1. Provides forms for uploading multiple files or fetching PDFs via URLs.
  2. Dynamically displays visualizations using Plotly (bar charts, line graphs) and Leaflet (maps).
  3. Includes interactive elements like hover popups on clustering maps to show incident details.
  4. Built with Bootstrap for responsiveness and ease of use.

## Visualizations

### `1. Bar Chart`

- **Purpose**: Provides an overview of the most common incident types.

- **Details**: Displays the frequency of different incident types ("Nature") in a bar chart. This visualization helps identify which types of incidents are most frequent.

- **Interactivity**: Hover over each bar to see the exact count of incidents.

### `2. Time Series Graph`

- **Purpose**: Shows trends of incidents over time.

- **Details**: Plots incidents by hour for each date. Each date generates its own graph, allowing for a clear view of daily trends and variations in incident occurrences.

- **Interactivity**: Hover over points on the line graph to see the number of incidents for a specific hour.

### `3. Clustering Map`

- **Purpose**: Geographically clusters incidents to identify spatial patterns.

- **Details**: Uses Google Maps API for geocoding and Leaflet for interactive mapping. Displays clusters with markers that provide details such as the type of incident, date/time, and cluster number.

- **Interactivity**: Click on or hover over a marker to see detailed information about the incident.

### `4. Nature and Time Clustering`

- **Purpose**: Groups incidents based on their type and time of occurrence.

- **Details**: Uses clustering algorithms like KMeans to cluster incidents by encoded "Nature" and their occurrence time. The graph visualizes clusters to show relationships between types and times of incidents.

- **Interactivity**: Hover over data points to view details about the incident's nature, time, and cluster group.

### `5. Location and Nature Clustering`

- **Purpose**: Clusters incidents by their geographical location and type.

- **Details**: Geocoded locations are combined with incident types to generate clusters. This visualization shows patterns in how specific types of incidents occur in certain locations.

- **Interactivity**: Interactive maps allow users to explore incident clusters with detailed hover information, including the type of incident and its location.

## Tests

### Running Tests
Use `pytest` to run the test suite:
```bash
pipenv run python -m pytest -v
```
### Test Coverage

- **test_index_page.py**: Tests if the homepage loads successfully.

- **test_upload_no_file.py**: Tests the upload endpoint with no file provided.

- **test_upload_file.py**: Tests the upload endpoint with a valid PDF file.

- **test_fetch_no_urls.py**: Tests the fetch endpoint with no URLs provided.

- **test_visualize_empty_data.py**: Tests the visualization endpoint with no data.

# Approach

## Data Ingestion

### File Upload:
- Users can upload multiple PDF files through the web interface.

### URL Input:
- Users can also provide multiple URLs pointing to PDF files for incident data extraction.

---

## Data Fetching and Extraction

### Fetch Incidents:
- If URLs are provided, the system fetches PDF data from these URLs.

### Extract Incidents:
- Incident data is extracted from the uploaded/fetched PDF files. The extraction includes:
  - Parsing PDF text to identify incident records.
  - Splitting lines correctly based on date-time patterns.
  - Constructing a structured DataFrame containing relevant columns like `incident_time`, `incident_number`, `incident_location`, `nature`, and `incident_ori`.

---

## Data Processing

### Datetime Conversion:
- Converts `incident_time` from string format to a datetime object.

### Data Cleaning:
- Removes records with invalid/missing datetime entries.

### Geocoding:
- Uses Google Maps API to get latitude and longitude coordinates for incident locations.

---

## Data Visualization

### Bar Chart:
- **Purpose**: Creates a bar chart showing the frequency of different incident natures.
- **Details**: Displays how often each type of incident occurs, helping to identify common patterns.

### Time Series Graphs:
- **Purpose**: Generates individual time series graphs for each uploaded/fetched PDF, displaying incident counts over time.
- **Details**: Shows the trend of incidents across different hours in a day.

### KMeans Clustering Visualization:
- **Purpose**: Clusters incidents based on geocoded incident locations.
- **Details**:
  - Performs KMeans clustering using incident locations and nature.
  - Generates a scatter plot of incident clusters, with hover tools to display incident details (e.g., nature and time).

### DBScan Visualization:
- **Purpose**: Clusters incidents based on incident nature and time.
- **Details**:
  - Encodes the nature of incidents into numeric values for clustering.
  - Groups incidents by date and clusters them based on `nature` (encoded) and hour of the day.
  - Generates a scatter plot for each date with clusters, showing detailed hover information.

---

## Result Display

- Combines all visualizations—bar charts, time series graphs, and clustering plots.
- Renders these visualizations on the results page in the web interface, providing interactive insights into incident data.

## Error Handling and User Feedback

### Error Handling:
- Catches and logs errors during data fetching, extraction, and geocoding.

### User Notifications:
- Uses flash messages to inform users about issues like failed URL fetches or upload errors.

## Bugs and Assumptions

### Bugs:
1. **Inconsistent PDF Formatting**: If the structure of the PDF file changes, the extraction logic may fail.
2. **Multiple Incidents on the Same Line**: Errors may occur if the data isn't cleanly separated.
3. **Date Format**: Assumes dates in the incident PDF files follow the `%m/%d/%Y %H:%M` format.
4. **Internet Connection**: Requires a stable internet connection to fetch external URLs and use the Google Maps API.
5. **Google Maps API Key**: Assumes the key has the necessary permissions and is not restricted.

### Assumptions:
1. **Consistent PDFs**: The PDFs provided by Norman PD are consistently formatted.
2. **Complete Data**: Only incidents with complete information (i.e., all required fields present) are considered.
3. **Accurate Data**: The data is assumed to be accurate as provided by Norman PD.
4. **URL Handling**: Invalid URLs or restricted access (e.g., 404, 403 errors) will result in failed URL processing.
5. **Date Parsing**: Incorrect formats will lead to parsing failures.
6. **Geocoding Errors**: Some locations may not return coordinates, leading to incomplete clustering data.
7. **Large Datasets**: Processing large datasets may result in performance issues.
8. **Visualization Gaps**: Margins or layout gaps may require adjustments in Plotly settings.
9. **Multiple Submissions**: Handling simultaneous file uploads and URL fetches may increase runtime significantly.
