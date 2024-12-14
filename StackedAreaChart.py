import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the dataset
data_path = 'cleaned_dataset.csv'
dataset = pd.read_csv(data_path)




import plotly.express as px

# Ensure 'CRASH DATE' is in datetime format
dataset['CRASH DATE'] = pd.to_datetime(dataset['CRASH DATE'])

# Extract Year and Month
dataset['Year'] = dataset['CRASH DATE'].dt.year
dataset['Month'] = dataset['CRASH DATE'].dt.month

# Aggregate by Year and Month
monthly_crashes = dataset.groupby(['Year', 'Month']).size().reset_index(name='Crash Count')

# Create a stacked area chart
fig = px.area(monthly_crashes, x='Month', y='Crash Count', color='Year',
              title="Monthly Crash Trends (Stacked Area Chart)",
              labels={'Month': 'Month', 'Crash Count': 'Number of Crashes'})

fig.update_xaxes(tickmode='array', tickvals=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                 ticktext=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

fig.show()
