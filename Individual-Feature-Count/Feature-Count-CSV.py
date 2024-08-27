import pandas as pd
import os

# Define the base path for test scenarios
base_path = 'G:\\Test-Scenarios'

# Function to count sent and received messages for a given packet type
def count_messages(df, packet_type, control_packet_name):
    # Filter for the specified packet type and status
    control_packets = df[(df['PACKET_TYPE'] == packet_type) & (df['PACKET_STATUS'] == 'Successful')]

    # Filter specific control packet messages
    specific_packets = control_packets[control_packets['CONTROL_PACKET_TYPE/APP_NAME'] == control_packet_name]

    # Count messages sent by each sensor
    sent_count = specific_packets[~specific_packets['SOURCE_ID'].str.contains('SINKNODE|ROUTER', case=False)]['SOURCE_ID'].str.replace('SENSOR-', 'S-').value_counts()

    # Count messages received by each sensor
    received_count = specific_packets[~specific_packets['RECEIVER_ID'].str.contains('SINKNODE|ROUTER', case=False)]['RECEIVER_ID'].str.replace('SENSOR-', 'S-').value_counts()

    # Combine the data
    combined_counts = pd.DataFrame({
        f'{control_packet_name}_Sent': sent_count,
        f'{control_packet_name}_Received': received_count
    }).fillna(0).astype(int)  # Fill NaNs with 0 and ensure the counts are integers

    return combined_counts

# Iterate over each main folder (e.g., '2', '3', ...)
for folder in range(2, 16):
    folder_name = str(folder)
    folder_path = os.path.join(base_path, folder_name)
    
    # Check if the folder exists
    if not os.path.isdir(folder_path):
        continue
    
    # Iterate over each subfolder (e.g., 'seed1', 'seed2', ...)
    for subfolder in os.listdir(folder_path):
        subfolder_path = os.path.join(folder_path, subfolder)
        file_path = os.path.join(subfolder_path, 'Packet Trace.csv')
        
        # Check if the file exists
        if not os.path.exists(file_path):
            continue
        
        # Load the packet trace CSV file
        df = pd.read_csv(file_path, encoding='latin1')

        # Verify the required columns exist
        if not {'PACKET_TYPE', 'CONTROL_PACKET_TYPE/APP_NAME', 'SOURCE_ID', 'RECEIVER_ID', 'PACKET_STATUS'}.issubset(df.columns):
            print(f"Required columns are missing from the DataFrame in folder {folder_name}, subfolder {subfolder}.")
            continue

        # Count DAO and DIO messages
        dao_counts = count_messages(df, 'Control_Packet', 'DAO')
        dio_counts = count_messages(df, 'Control_Packet', 'DIO')

        # Merge both counts
        all_counts = pd.concat([dao_counts, dio_counts], axis=1).fillna(0).astype(int)

        # Filter Sensing packets
        sensing_packets = df[(df['PACKET_TYPE'] == 'Sensing') & (df['PACKET_STATUS'] == 'Successful')]

        # Abbreviate the sensor names
        sensing_packets['SOURCE_ID'] = sensing_packets['SOURCE_ID'].str.replace('SENSOR-', 'S-')
        sensing_packets['RECEIVER_ID'] = sensing_packets['RECEIVER_ID'].str.replace('SENSOR-', 'S-')

        # Count the packets received by each sensor
        sensor_receive_counts = sensing_packets[sensing_packets['RECEIVER_ID'].str.contains('S-', na=False)]['RECEIVER_ID'].value_counts()

        # Add a total packets received column
        all_counts['Packet_Received'] = sensor_receive_counts.reindex(all_counts.index, fill_value=0).astype(int)

        # Sort by sensor IDs
        def extract_sensor_number(name):
            # If 'Sensor' is found in the column name, extract the number
            if 'Sensor' in name:
                return int(name.split('Sensor')[1])
            return float('inf')

        # Reindex based on sensor numbers
        all_counts = all_counts.reindex(sorted(all_counts.columns, key=extract_sensor_number), axis=1)

        # Add a prefix 'Sensor' to each index
        all_counts.index = ['Sensor' + idx.split('-')[1] for idx in all_counts.index]

        # Transpose the DataFrame
        all_counts = all_counts.T

        # Generate output file path in the same directory as input file
        output_file_path = os.path.join(subfolder_path, 'Sensor_Message_Counts.csv')

        # Save the transposed data to a CSV file
        all_counts.to_csv(output_file_path)

        print(f'Successfully saved the transposed counts to {output_file_path}')
