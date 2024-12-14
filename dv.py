import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the dataset
data_path = 'cleaned_dataset.csv'
dataset = pd.read_csv(data_path)



# import pandas as pd
# import plotly.express as px
# import requests

# # Load the NYC Borough GeoJSON
# geojson_url = "https://raw.githubusercontent.com/dwillis/nyc-maps/master/boroughs.geojson"
# geojson_data = requests.get(geojson_url).json()

# # Convert CRASH DATE to datetime
# dataset['CRASH DATE'] = pd.to_datetime(dataset['CRASH DATE'])

# # Extract year for grouping
# dataset['Year'] = dataset['CRASH DATE'].dt.year

# # Filter valid borough data and drop missing values
# borough_data = dataset[['Year', 'BOROUGH']].dropna()

# # Aggregate crash counts by borough and year
# borough_crash_counts = borough_data.groupby(['Year', 'BOROUGH']).size().reset_index(name='Count')

# # Standardize borough names to match GeoJSON
# borough_crash_counts['BOROUGH'] = borough_crash_counts['BOROUGH'].str.title()

# # Create a complete dataset with all years and boroughs to avoid animation issues
# all_years = pd.DataFrame({'Year': range(borough_crash_counts['Year'].min(), borough_crash_counts['Year'].max() + 1)})
# all_boroughs = pd.DataFrame({'BOROUGH': ['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island']})
# complete_index = all_years.merge(all_boroughs, how='cross')
# borough_crash_counts = complete_index.merge(borough_crash_counts, on=['Year', 'BOROUGH'], how='left').fillna(0)

# # Add a static location for borough labels (latitude and longitude)
# borough_labels = pd.DataFrame({
#     'BOROUGH': ['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island'],
#     'Latitude': [40.837048, 40.650002, 40.7831, 40.7282, 40.579021],
#     'Longitude': [-73.865433, -73.949997, -73.9712, -73.7949, -74.151535]
# })

# # Create the animated choropleth map with enhanced color scale
# fig = px.choropleth_mapbox(
#     borough_crash_counts,
#     geojson=geojson_data,
#     locations='BOROUGH',  # Column with borough names
#     featureidkey='properties.BoroName',  # Match GeoJSON field for borough names
#     color='Count',  # Color intensity based on crash count
#     animation_frame='Year',  # Animate across years
#     mapbox_style='carto-positron',
#     title='Crash Intensity by Borough Over Time',
#     center={"lat": 40.7128, "lon": -74.0060},  # Centered on NYC
#     zoom=9.3,
#     color_continuous_scale='Spectral',  # Enhanced color scale
#     labels={'Count': 'Crash Intensity'},
# )

# # Add borough labels to the map
# fig.add_scattermapbox(
#     lat=borough_labels['Latitude'],
#     lon=borough_labels['Longitude'],
#     mode='text',
#     text=borough_labels['BOROUGH'],
#     textfont=dict(size=14, color='black',  weight='bold'),
#     textposition='middle center',
#     name='Borough Names',

# )



# # Update layout to show numerical values on the color bar
# fig.update_layout(
#     coloraxis_colorbar=dict(
#         title="Crash Count",
#         tickvals=[
#             borough_crash_counts['Count'].min(),
#             borough_crash_counts['Count'].quantile(0.25),
#             borough_crash_counts['Count'].mean(),
#             borough_crash_counts['Count'].quantile(0.75),
#             borough_crash_counts['Count'].max()
#         ],
#         ticktext=[
#             int(borough_crash_counts['Count'].min()),
#             int(borough_crash_counts['Count'].quantile(0.25)),
#             int(borough_crash_counts['Count'].mean()),
#             int(borough_crash_counts['Count'].quantile(0.75)),
#             int(borough_crash_counts['Count'].max())
#         ]
#     ),
#     margin={"r": 0, "t": 50, "l": 0, "b": 0}
# )

# # Display the animated map
# fig.show()







import pandas as pd
import plotly.express as px
import requests

# Load the NYC Borough GeoJSON
geojson_url = "https://raw.githubusercontent.com/dwillis/nyc-maps/master/boroughs.geojson"
geojson_data = requests.get(geojson_url).json()

# Load the dataset (Replace 'cleaned_dataset.csv' with the correct path)
data_path = 'cleaned_dataset.csv'
dataset = pd.read_csv(data_path)

# Convert CRASH DATE to datetime
dataset['CRASH DATE'] = pd.to_datetime(dataset['CRASH DATE'])

# Extract year for grouping
dataset['Year'] = dataset['CRASH DATE'].dt.year

# Filter valid borough data and drop missing values
borough_data = dataset[['Year', 'BOROUGH']].dropna()

# Aggregate crash counts by borough and year
borough_crash_counts = borough_data.groupby(['Year', 'BOROUGH']).size().reset_index(name='Count')

# Standardize borough names to match GeoJSON
borough_crash_counts['BOROUGH'] = borough_crash_counts['BOROUGH'].str.title()

# Create a complete dataset with all years and boroughs to avoid animation issues
all_years = pd.DataFrame({'Year': range(borough_crash_counts['Year'].min(), borough_crash_counts['Year'].max() + 1)})
all_boroughs = pd.DataFrame({'BOROUGH': ['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island']})
complete_index = all_years.merge(all_boroughs, how='cross')
borough_crash_counts = complete_index.merge(borough_crash_counts, on=['Year', 'BOROUGH'], how='left').fillna(0)

# Add a static location for borough labels (latitude and longitude)
borough_labels = pd.DataFrame({
    'BOROUGH': ['Bronx', 'Brooklyn', 'Manhattan', 'Queens', 'Staten Island'],
    'Latitude': [40.837048, 40.650002, 40.7831, 40.7282, 40.579021],
    'Longitude': [-73.865433, -73.949997, -73.9712, -73.7949, -74.151535]
})

# Create the animated choropleth map with enhanced color scale
fig = px.choropleth_mapbox(
    borough_crash_counts,
    geojson=geojson_data,
    locations='BOROUGH',  # Column with borough names
    featureidkey='properties.BoroName',  # Match GeoJSON field for borough names
    color='Count',  # Color intensity based on crash count
    animation_frame='Year',  # Animate across years
    mapbox_style='carto-positron',
    title='Crash Intensity by Borough Over Time',
    center={"lat": 40.7128, "lon": -74.0060},  # Centered on NYC
    zoom=8.3,
    color_continuous_scale='Spectral',  # Enhanced color scale
    labels={'Count': 'Crash Intensity'},
)

# Add borough labels to the map
fig.add_scattermapbox(
    lat=borough_labels['Latitude'],
    lon=borough_labels['Longitude'],
    mode='text',
    text=borough_labels['BOROUGH'],
    textfont=dict(size=14, color='black', weight='bold'),
    textposition='middle center',
    name='Borough Names'
)

# Update layout to show numerical values on the color bar
fig.update_layout(
    coloraxis_colorbar=dict(
        title="Crash Count",
        tickvals=[
            borough_crash_counts['Count'].min(),
            borough_crash_counts['Count'].quantile(0.25),
            borough_crash_counts['Count'].mean(),
            borough_crash_counts['Count'].quantile(0.75),
            borough_crash_counts['Count'].max()
        ],
        ticktext=[
            int(borough_crash_counts['Count'].min()),
            int(borough_crash_counts['Count'].quantile(0.25)),
            int(borough_crash_counts['Count'].mean()),
            int(borough_crash_counts['Count'].quantile(0.75)),
            int(borough_crash_counts['Count'].max())
        ]
    ),
    margin={"r": 0, "t": 30, "l": 0, "b": 0}
)

# Save the Plotly figure as an HTML file
fig.write_html('choropleth_map.html')

# HTML layout to create a 4-quadrant grid with Plotly figure in the top-left quadrant
html_layout = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crash Intensity Map</title>
    <style>
        /* Set up the grid layout with 4 quadrants */
        .grid-container {
            display: grid;
            grid-template-columns: 40% 50%;
            grid-template-rows: 60% 50%;
            height: 100vh;
            gap: 10px;
        }

        /* Top-left quadrant for the map */
        .top-left {
            grid-column: 1;
            grid-row: 1;
        }

        /* The other quadrants */
        .top-right, .bottom-left, .bottom-right {
            background-color: #f0f0f0; /* Light grey background for other quadrants */
        }

        /* Ensure the iframe fits properly in the grid */
        iframe {
            width: 100%;
            height: 100%;
            border: none;
        }
    </style>
</head>
<body>

    <div class="grid-container">
        <!-- Top Left: Place the Plotly map here -->
        <div class="top-left">

            <iframe src="choropleth_map.html" title="Crash Intensity Map"></iframe>
        </div>
        
        <!-- Placeholder for other quadrants (you can add other content here if needed) -->
        <div class="top-right">
            <p>Top Right Quadrant</p>
        </div>
        <div class="bottom-left">
            <p>Bottom Left Quadrant</p>
        </div>
        <div class="bottom-right">
            <p>Bottom Right Quadrant</p>
        </div>
    </div>

</body>
</html>
"""

# Save the HTML layout to a file
with open('quad_layout.html', 'w') as f:
    f.write(html_layout)

print("HTML layout saved as 'quad_layout.html'. Open this file in a browser to view the result.")
