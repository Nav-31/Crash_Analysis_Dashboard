import plotly.express as px
import pandas as pd

# Load the dataset
data_path = 'cleaned_dataset.csv'
dataset = pd.read_csv(data_path)

import pandas as pd
import plotly.graph_objects as go



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
fig_killed = go.Figure(data=[go.Pie(labels=labels_killed, values=killed_data, hole=0.3, title="Total People Killed - Breakdown by Category")])

# Create the pie chart for Total People Injured
fig_injured = go.Figure(data=[go.Pie(labels=labels_injured, values=injured_data, hole=0.3, title="Total People Injured - Breakdown by Category")])

# Show both pie charts
fig_killed.show()
fig_injured.show()
