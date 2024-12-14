import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

# Load the dataset
data_path = 'cleaned_dataset.csv'
dataset = pd.read_csv(data_path)

import pandas as pd
import plotly.graph_objects as go


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
    marker=dict(color=crash_counts_by_hour['Crash Count'], colorscale='Viridis', showscale=True ),
    hovertemplate="Hour: %{x}<br>Crashes: %{y}<br>% of Crashes at this hour: %{customdata}%<extra></extra>",  # Custom hover text
    customdata=crash_counts_by_hour['Percentage']  # Pass the percentage as custom data for hover

)])

# Add the title and axis labels
fig.update_layout(
    title="Number of Crashes by Hour of the Day (2012-2023)",
    title_font=dict(size=16,  weight='bold'),
    # , color="black", weight='bold')
    xaxis_title="Hour of Day",
    yaxis_title="Crash Count",
    xaxis=dict(tickmode='linear', tickvals=list(range(24))),  # Set x-axis from 0 to 23 hours
    template="plotly_dark",  # Optional: dark theme for better aesthetics
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
    ax=20,
    ay=-40
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
    ax=-20,
    ay=-60
)

# Display the figure
fig.show()
