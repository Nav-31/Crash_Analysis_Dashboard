import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import requests

# Load the dataset
data_path = 'cleaned_dataset.csv'
dataset = pd.read_csv(data_path)




# Summing up the number of people killed and injured for each category
killed_pedestrians = dataset['NUMBER OF PEDESTRIANS KILLED'].sum()
killed_cyclists = dataset['NUMBER OF CYCLIST KILLED'].sum()
killed_motorists = dataset['NUMBER OF MOTORIST KILLED'].sum()

# Calculate the unknown killed (if any)
unknown_killed = dataset['NUMBER OF PERSONS KILLED'].sum() - (killed_pedestrians + killed_cyclists + killed_motorists)

# Summing up the number of people injured for each category
injured_pedestrians = dataset['NUMBER OF PEDESTRIANS INJURED'].sum()
injured_cyclists = dataset['NUMBER OF CYCLIST INJURED'].sum()
injured_motorists = dataset['NUMBER OF MOTORIST INJURED'].sum()

# Calculate the unknown injured (if any)
unknown_injured = dataset['NUMBER OF PERSONS INJURED'].sum() - (injured_pedestrians + injured_cyclists + injured_motorists)

# Data for the pie charts
killed_data = [killed_pedestrians, killed_cyclists, killed_motorists, unknown_killed]
injured_data = [injured_pedestrians, injured_cyclists, injured_motorists, unknown_injured]

# Labels for the pie charts
labels_killed = ['Pedestrians', 'Cyclists', 'Motorists', 'Unknown']
labels_injured = ['Pedestrians', 'Cyclists', 'Motorists', 'Unknown']

# Create the pie chart for Total People Killed
fig_killed = go.Figure(data=[go.Pie(labels=labels_killed, values=killed_data, hole=0.3)])

# Set the title for the pie chart
fig_killed.update_layout(
    title="People Killed in Traffic Crash",
    template="plotly_dark",
    title_font=dict(size=18, family="Arial", weight='bold'),
    title_x=0.5,  # Center the title horizontally
    title_y=0.99,  # Set the title to the top of the plot
    margin=dict(t=40, b=0, l=0, r=0)
)

# Create the pie chart for Total People Injured
fig_injured = go.Figure(data=[go.Pie(labels=labels_injured, values=injured_data, hole=0.3)])

# Set the title for the pie chart
fig_injured.update_layout(
    title="People Injured in Traffic Crash",
    title_font=dict(size=18, family="Trebuchet MS", weight='bold'),
    title_x=0.5,  # Center the title horizontally
    title_y=0.99,  # Set the title to the top of the plot
    template="plotly_dark",
    margin=dict(t=65, b=0, l=0, r=0)
)
# Save the pie chart HTML files for embedding
fig_killed.write_html('pie_chart_killed.html')
fig_injured.write_html('pie_chart_injured.html')

# Load the NYC Borough GeoJSON
geojson_url = "https://raw.githubusercontent.com/dwillis/nyc-maps/master/boroughs.geojson"
geojson_data = requests.get(geojson_url).json()

# Load the dataset again (as the first dataset loading is already done)
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

# # Create the animated choropleth map with enhanced color scale
# fig_map = go.Figure(go.Choropleth(
#     geojson=geojson_data,
#     locations=borough_crash_counts['BOROUGH'],
#     z=borough_crash_counts['Count'],
#     hoverinfo="location+z",
#     colorscale="Viridis"
# ))



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
    zoom=8.4,
    color_continuous_scale='Spectral',  # Enhanced color scale
    labels={'Count': 'Crash Intensity'},
)

# Add borough labels to the map
fig.add_scattermapbox(
    lat=borough_labels['Latitude'],
    lon=borough_labels['Longitude'],
    mode='text',
    text=borough_labels['BOROUGH'],
    textfont=dict(size=16, color='black', weight='bold'),
    textposition='middle center',
    name='Borough Names',
)

# Update layout to show numerical values on the color bar and apply black background
fig.update_layout(
    title_font=dict(size=18, family="Trebuchet MS", weight='bold'),
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
    margin={"r": 0, "t": 30, "l": 0, "b": 50},
    height=400,
    font=dict(color='white'),  # Set font color to white for better readability on dark background
    plot_bgcolor='black',  # Set background color of the plot area to black
    paper_bgcolor='black',  # Set the background color of the whole paper to black
    sliders=[{
        'currentvalue': {
            'visible': True, 
            'prefix': 'Year: ',
            'font': {'size': 14, 'color': 'white'}
        },
        'pad': {'t': 30}  # Add some padding between map and slider,
    }],
)

# Display the animated map
# fig.show()
# Save the bar chart as an HTML file for embedding
fig.write_html('choropleth_map.html')


# BAR GRAPH

# Convert the 'CRASH TIME' to datetime and extract the hour of the day
dataset['CRASH TIME'] = pd.to_datetime(dataset['CRASH TIME'], format='%H:%M')
dataset['Hour of Day'] = dataset['CRASH TIME'].dt.hour

# Group by the hour and count the number of crashes
crash_counts_by_hour = dataset.groupby('Hour of Day').size().reset_index(name='Crash Count')

# Calculate the total number of crashes
total_crashes = crash_counts_by_hour['Crash Count'].sum()

# Calculate the percentage for each hour
crash_counts_by_hour['Percentage'] = (crash_counts_by_hour['Crash Count'] / total_crashes) * 100
crash_counts_by_hour['Percentage'] = crash_counts_by_hour['Percentage'].round(2)

# Create the figure with the bar chart using Plotly
fig = go.Figure(data=[go.Bar(
    x=crash_counts_by_hour['Hour of Day'],
    y=crash_counts_by_hour['Crash Count'],
    marker=dict(color=crash_counts_by_hour['Crash Count'], colorscale='Viridis', showscale=True),
    hovertemplate="Hour: %{x}<br>Crashes: %{y}<br>% of Crashes at this hour: %{customdata}%<extra></extra>",  # Custom hover text
    customdata=crash_counts_by_hour['Percentage']  # Pass the percentage as custom data for hover
)])

# Add the title and axis labels
fig.update_layout(
    title="Number of Crashes by Hour of the Day",
    title_font=dict(size=18, family="Trebuchet MS", weight='bold'),
    title_x=0.5,  # Center the title horizontally
    title_y=0.99,  # Set the title to the top of the plot
    xaxis_title="Hour of Day",
    yaxis_title="Crash Count",
    xaxis=dict(tickmode='linear', tickvals=list(range(24))),  # Set x-axis from 0 to 23 hours
    template="plotly_dark",  # Optional: dark theme for better aesthetics
    margin=dict(t=20, b=50, l=0, r=0)
)

# Add annotations for the peak value
max_crash_hour = crash_counts_by_hour.loc[crash_counts_by_hour['Crash Count'].idxmax()]
fig.add_annotation(
    x=max_crash_hour['Hour of Day'],
    y=max_crash_hour['Crash Count'],
    text=f"Peak: {max_crash_hour['Crash Count']} crashes",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowcolor='red',
    font=dict(size=12, color="red"),
    ax=-40,
    ay=-10
)

# Add annotations for the lowest crash count hour
min_crash_hour = crash_counts_by_hour.loc[crash_counts_by_hour['Crash Count'].idxmin()]
fig.add_annotation(
    x=min_crash_hour['Hour of Day'],
    y=min_crash_hour['Crash Count'],
    text=f"Lowest: {min_crash_hour['Crash Count']} crashes",
    showarrow=True,
    arrowhead=2,
    arrowsize=1,
    arrowcolor='red',
    font=dict(size=12, color="red"),
    ax=0,
    ay=-60
)

# Save the bar chart as an HTML file for embedding
fig.write_html('bar_chart_by_hour.html')






#TREEMAP





# Replace 'Station Wagon/Sport Utility Vehicle' with 'SUV' in the 'VEHICLE TYPE CODE 3' column
dataset['VEHICLE TYPE CODE 3'] = dataset['VEHICLE TYPE CODE 3'].replace('Station Wagon/Sport Utility Vehicle', 'SUV')
dataset['VEHICLE TYPE CODE 3'] = dataset['VEHICLE TYPE CODE 3'].replace('Passenger Vehicle', 'Passenger Car')
dataset['CONTRIBUTING FACTOR VEHICLE 1'] = dataset['CONTRIBUTING FACTOR VEHICLE 1'].replace('Unsafe Speed', 'OverSpeed')
dataset['CONTRIBUTING FACTOR VEHICLE 1'] = dataset['CONTRIBUTING FACTOR VEHICLE 1'].replace('Alcohol Involvement', 'Alcohol')
dataset['CONTRIBUTING FACTOR VEHICLE 1'] = dataset['CONTRIBUTING FACTOR VEHICLE 1'].replace('Driver Inattention/Distraction', 'Driver Distracted')
dataset['CONTRIBUTING FACTOR VEHICLE 1'] = dataset['CONTRIBUTING FACTOR VEHICLE 1'].replace('Failure To Yield Right-Of-Way', 'Yield Violation')
dataset['CONTRIBUTING FACTOR VEHICLE 1'] = dataset['CONTRIBUTING FACTOR VEHICLE 1'].replace('Following Too Closely', 'Tailgating ')




# Filter out "Unspecified" from both contributing factors and vehicle types
filtered_dataset = dataset[
    (dataset['CONTRIBUTING FACTOR VEHICLE 1'] != 'Unspecified') &
    (dataset['VEHICLE TYPE CODE 3'] != 'Unspecified')
]

# Get the top 5 contributing factors and top 3 vehicle types
top_contributing_factors = filtered_dataset['CONTRIBUTING FACTOR VEHICLE 1'].value_counts().nlargest(5).index
top_vehicle_types = filtered_dataset['VEHICLE TYPE CODE 3'].value_counts().nlargest(3).index

# Filter the dataset to include only the top 5 contributing factors and top 3 vehicle types
filtered_data = filtered_dataset[
    filtered_dataset['CONTRIBUTING FACTOR VEHICLE 1'].isin(top_contributing_factors) & 
    filtered_dataset['VEHICLE TYPE CODE 3'].isin(top_vehicle_types)
]

# Prepare the data for the Treemap visualization
treemap_data = filtered_data.groupby(['CONTRIBUTING FACTOR VEHICLE 1', 'VEHICLE TYPE CODE 3']).size().reset_index(name='Count')

# Create the Treemap using Plotly with dark theme
fig3 = px.sunburst(treemap_data, 
                   path=['CONTRIBUTING FACTOR VEHICLE 1', 'VEHICLE TYPE CODE 3'], 
                   values='Count',
                   template="plotly_dark", 
                   title='Treemap: Top 5 Crash Contributing Factors and Top 3 Vehicle Types',
                   color_discrete_sequence=px.colors.qualitative.Light24)
                #                    color='Count',  # Apply color based on the count of each combinatio
                #    color_continuous_scale='Plasma')
                   
                   
# Update layout to make text bold
fig3.update_traces(textfont=dict(family='Arial', size=12, color='black', weight='bold'))



# Adjust the size of the Treemap
fig3.update_layout(
    height=410,  # Increase the height to fit the content better
    # width=800,   # Adjust the width for better proportions
    title_x=0.5,  # Center the title horizontally
    title_y=0.95,  # Set the title to the top of the plot
    title_font=dict(size=18, family="Trebuchet MS", weight='bold'),
    margin=dict(t=50, b=0, l=0, r=0),
)

# Show the Treemap
# fig3.show()

# Save the Treemap as an HTML file for embedding
fig3.write_html('treemap.html')


# Define layout for the HTML grid with pie charts in the bottom-right quadrant
html_layout = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@700&display=swap" rel="stylesheet">

    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Crash Intensity Map</title>
    <style>
     html, body {{
            margin: 0;
            padding: 0;
            height: 100%;  /* Ensure the body and html take the full height */
            background-color: black;  /* Set background color to black */
            overflow: hidden;
        }}
        /* Set up the grid layout with 4 quadrants */
        .grid-container {{
            display: grid;
            grid-template-columns: 50% 50%;
            grid-template-rows: 60% 40%;
            height: calc(100vh - 20px);

        }}

         /* Common title styling */
        .common-title {{
            text-align: center;
            color: white;
            font-family: 'Trebuchet MS', sans-serif; 
            font-size: 24px;
            letter-spacing: 1px; 
            font-weight: bold;
           
            margin-top: 8px;  /* Space between title and grid */
        }}

        /* Top-left quadrant for the map */
        .top-left {{
            grid-column: 1;
            grid-row: 1;
            background-color: black;
        }}

        /* Top-right quadrant for the bar graph */
        .top-right {{
            grid-column: 2;
            grid-row: 1;
            background-color: black;
        }}

        /* Bottom-right quadrant for pie charts side by side */
        .bottom-right {{
            grid-column: 2;
            grid-row: 2;
            background-color: black;

            display: flex;
            
        }}

        /* Bottom-left quadrant for the bar graph */
        .bottom-left {{
            grid-column: 1;
            grid-row: 2;
            background-color: black;
        }}

        iframe {{
            width: 100%;
            height: 100%;
            border: none;
        }}
    </style>
</head>
<body>

 <!-- Common title for the entire visualization -->
    <div class="common-title">
TRAFFIC CRASH INTENSITY AND ANALYSIS DASHBOARD: 2012-23

</div>



    <div class="grid-container">
        <!-- Top Left: Place the Plotly map here -->
        <div class="top-left">
            <iframe src="choropleth_map.html" title="Crash Intensity Map"></iframe>
        </div>

        
        <!-- Top Right: Place the bar graph here -->
        <div class="bottom-left">
            <iframe src="bar_chart_by_hour.html" title="Crashes by Hour of Day"></iframe>
        </div>

        <div class="top-right">
        <iframe src="treemap.html" title="Treemap of Contributing Factors and Vehicle Types"></iframe>
        </div>



        <!-- Bottom Right: Pie charts for killed and injured side by side -->
        <div class="bottom-right">
            <div style="width: 50%;">
                
                <iframe src="pie_chart_killed.html"></iframe>
            </div>
            <div style="width: 50%;">
             
                <iframe src="pie_chart_injured.html"></iframe>
            </div>
        </div>




    </div>
</body>
</html>
"""

# Save the final HTML layout to a file
with open('quad_layout_with_pie_chart_headings.html', 'w') as f:
    f.write(html_layout)

print("HTML layout with pie chart headings saved as 'quad_layout_with_pie_chart_headings.html'. Open this file in a browser to view the result.")
