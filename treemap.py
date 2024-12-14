import plotly.express as px
import pandas as pd

import requests

# Load the dataset
data_path = 'cleaned_dataset.csv'
dataset = pd.read_csv(data_path)




# Replace 'Station Wagon/Sport Utility Vehicle' with 'SUV' in the 'VEHICLE TYPE CODE 3' column
dataset['VEHICLE TYPE CODE 3'] = dataset['VEHICLE TYPE CODE 3'].replace('Station Wagon/Sport Utility Vehicle', 'SUV')

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

# Create the Treemap using Plotly with dark theme and apply discrete color scale
fig3 = px.sunburst(treemap_data, 
                   path=['CONTRIBUTING FACTOR VEHICLE 1', 'VEHICLE TYPE CODE 3'], 
                   values='Count',
                   title='Treemap of Top 5 Contributing Factors and Top 3 Vehicle Types (Excluding Unspecified)',
                   template="plotly_dark",  # Apply dark mode theme
                #    color='Count',  # Apply color based on the count of each combinatio
                #    color_continuous_scale='Plasma')
                   color_discrete_sequence=px.colors.qualitative.Light24)  # Choose a discrete color scale (e.g., 'Set1', 'Set2', 'Set3')

# Adjust the size of the Treemap
fig3.update_layout(
    height=600,  # Increase the height to fit the content better
    width=800,   # Adjust the width for better proportions
)

# Show the Treemap
fig3.show()
