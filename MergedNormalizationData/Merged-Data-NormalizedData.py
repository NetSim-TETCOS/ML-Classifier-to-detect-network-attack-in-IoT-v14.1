import pandas as pd
import os

# Define the base path where the folders are located
base_path = 'G:\\Test-Scenarios'

# List of specific folders you want to process
folders_to_process = ['2', '4', '5', '6','8', '10', '12', '14']  # Add folder names as strings

# Initialize the start row for writing in Excel
start_row = 0

# Define the path for the output Excel file
excel_file_path = os.path.join(base_path, 'Merged_Sensor_Message_Counts.xlsx')

# Create an Excel writer object
with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
    # Iterate over each specified folder
    for folder in folders_to_process:
        folder_path = os.path.join(base_path, folder)

        # Check if the folder exists
        if not os.path.isdir(folder_path):
            print(f"Folder {folder} does not exist. Skipping...")
            continue

        # Iterate over each subfolder (e.g., 'seed1', 'seed2', ...)
        for subfolder in os.listdir(folder_path):
            subfolder_path = os.path.join(folder_path, subfolder)
            file_path = os.path.join(subfolder_path, 'Sensor_Message_Counts.csv')

            # Check if the file exists
            if not os.path.exists(file_path):
                print(f"File {file_path} does not exist. Skipping...")
                continue

            # Load the CSV file into a DataFrame with header
            try:
                df = pd.read_csv(file_path)

                # Add a 'Sensor' column with the sensor (subfolder) name repeated for all rows
                df.insert(0, 'Sensor', subfolder)
                
                # Write the DataFrame to the Excel file starting from the start_row
                df.to_excel(writer, index=False, startrow=start_row, sheet_name='All_Data')

                # Update the start_row for the next DataFrame to be written
                start_row += len(df) + 2  # Add 2 to create a space between each sensor's data

            except Exception as e:
                print(f"Error processing file {file_path}: {e}")

# Now process the merged Excel file to normalize data
merged_df = pd.read_excel(excel_file_path, sheet_name='All_Data')

# Convert non-numeric columns to numeric and handle errors
def to_numeric(df):
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

# Drop non-numeric columns and convert remaining data to numeric
numeric_df = merged_df.drop(columns=['Sensor'])
numeric_df = to_numeric(numeric_df)

# Normalize each row
try:
    max_values = numeric_df.max(axis=1)
    normalized_df = numeric_df.div(max_values, axis=0)
except Exception as e:
    print(f"Error during normalization: {e}")
    normalized_df = numeric_df  # Fallback to original data if normalization fails

# Add the 'Sensor' column back to the normalized DataFrame
normalized_df.insert(0, 'Sensor', merged_df['Sensor'])

# Define the path for the output Excel file
normalized_excel_file_path = os.path.join(base_path, 'Normalized_Sensor_Message_Counts.xlsx')

# Save the normalized DataFrame to a new Excel file
with pd.ExcelWriter(normalized_excel_file_path, engine='xlsxwriter') as writer:
    normalized_df.to_excel(writer, index=False, sheet_name='Normalized_Data')

print(f"Normalized data saved to {normalized_excel_file_path}")