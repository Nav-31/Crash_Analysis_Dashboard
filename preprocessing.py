import pandas as pd

# Load the dataset
file_path = 'Original_dataset.csv'  
data = pd.read_csv(file_path)

# Step 1: Drop columns with excessive missing values (threshold > 90% missing)
columns_to_drop = [
    'VEHICLE TYPE CODE 1',
    'VEHICLE TYPE CODE 2',
    'VEHICLE TYPE CODE 4',
    'VEHICLE TYPE CODE 5',
    'CONTRIBUTING FACTOR VEHICLE 2',
    'CONTRIBUTING FACTOR VEHICLE 3',
    'CONTRIBUTING FACTOR VEHICLE 4',
    'CONTRIBUTING FACTOR VEHICLE 5',
    'COLLISION_ID',
    'LOCATION',
    'ON STREET NAME',
    'CROSS STREET NAME',
    'OFF STREET NAME',
    'ZIP CODE',
] 
data_cleaned = data.drop(columns=columns_to_drop)

# Step 2: Impute missing values
# Impute LATITUDE and LONGITUDE with their respective means
data_cleaned['LATITUDE'].fillna(data_cleaned['LATITUDE'].mean(), inplace=True)
data_cleaned['LONGITUDE'].fillna(data_cleaned['LONGITUDE'].mean(), inplace=True)

# Step 3: Standardize datetime columns
# Combine CRASH DATE and CRASH TIME into a single datetime column

data_cleaned['CRASH DATETIME'] = pd.to_datetime(data_cleaned['CRASH DATE'] + ' ' + data_cleaned['CRASH TIME'])

data_cleaned['CRASH DATE'] = pd.to_datetime(data_cleaned['CRASH DATE']).dt.to_period('M').astype(str)



# Step 4: Drop rows with missing values in critical columns
data_cleaned.dropna(subset=['VEHICLE TYPE CODE 3', 'CONTRIBUTING FACTOR VEHICLE 1', 'BOROUGH'], inplace=True)

# Step 5: Normalize string columns
string_columns = ['BOROUGH', 'CONTRIBUTING FACTOR VEHICLE 1', 'VEHICLE TYPE CODE 3']
for col in string_columns:
    data_cleaned[col] = data_cleaned[col].str.strip().str.title()

# Step 6: Save the cleaned dataset
output_path = 'cleaned_dataset.csv'  
data_cleaned.to_csv(output_path, index=False)

print(f"Cleaned dataset saved to {output_path}")
