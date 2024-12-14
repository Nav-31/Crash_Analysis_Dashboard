# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go

# # Load the dataset
# data_path = 'cleaned_dataset.csv'
# dataset = pd.read_csv(data_path)



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
#     margin={"r": 0, "t": 30, "l": 0, "b": 0},
#     height=600,

#     sliders=[{
#         'currentvalue': {
#             'visible': True, 
#             'prefix': 'Year: ',
#             'font': {'size': 18}
#         }
#     }],
# )

# # Display the animated map
# fig.show()



import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

# Load the dataset
data_path = 'cleaned_dataset.csv'
dataset = pd.read_csv(data_path)

# Load the NYC Borough GeoJSON
geojson_url = "https://raw.githubusercontent.com/dwillis/nyc-maps/master/boroughs.geojson"
geojson_data = requests.get(geojson_url).json()

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
    mapbox_style='carto-positron',  # Use light map style
    title='Crash Intensity by Borough Over Time',
    center={"lat": 40.7128, "lon": -74.0060},  # Centered on NYC
    zoom=9.3,
    color_continuous_scale='Spectral',  # Enhanced color scale
    labels={'Count': 'Crash Intensity'},
)

# Add borough labels to the map
fig.add_scattermapbox(
    lat=borough_labels['Latitude'],
    lon=borough_labels['Longitude'],
    mode='text',
    text=borough_labels['BOROUGH'],
    textfont=dict(size=14, color='white', weight='bold'),
    textposition='middle center',
    name='Borough Names',
)

# Update layout to show numerical values on the color bar and apply black background
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
    margin={"r": 0, "t": 30, "l": 0, "b": 0},
    height=600,
    font=dict(color='white'),  # Set font color to white for better readability on dark background
    plot_bgcolor='black',  # Set background color of the plot area to black
    paper_bgcolor='black',  # Set the background color of the whole paper to black
    sliders=[{
        'currentvalue': {
            'visible': True, 
            'prefix': 'Year: ',
            'font': {'size': 18, 'color': 'white'}
        }
    }],
)

# Display the animated map
fig.show()
