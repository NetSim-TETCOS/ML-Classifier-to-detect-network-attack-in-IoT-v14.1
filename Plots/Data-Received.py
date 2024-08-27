import pandas as pd
import matplotlib.pyplot as plt
import os

# Base path where the 'Test-Scenarios' folder is located
base_path = 'G:\\Test-Scenarios'

# Define malicious nodes based on the scenario number
malicious_nodes_dict = {
    '2': ['S-5', 'S-9'],
    '3': ['S-5', 'S-9', 'S-10'],
    '4': ['S-5', 'S-9', 'S-10', 'S-16'],
    '5': ['S-5', 'S-9', 'S-10', 'S-16', 'S-18'],
    '6': ['S-5', 'S-9', 'S-10', 'S-16', 'S-18', 'S-19'],
    '7': ['S-5', 'S-9', 'S-10', 'S-16', 'S-18', 'S-19', 'S-22'],
    '8': ['S-5', 'S-9', 'S-10', 'S-16', 'S-18', 'S-19', 'S-22', 'S-24'],
    '9': ['S-5', 'S-9', 'S-10', 'S-16', 'S-18', 'S-19', 'S-22', 'S-24', 'S-27'],
    '10': ['S-5', 'S-9', 'S-10', 'S-16', 'S-18', 'S-19', 'S-22', 'S-24', 'S-27', 'S-30'],
    '11': ['S-5', 'S-9', 'S-10', 'S-16', 'S-18', 'S-19', 'S-22', 'S-24', 'S-27', 'S-30', 'S-33'],
    '12': ['S-5', 'S-9', 'S-10', 'S-16', 'S-18', 'S-19', 'S-22', 'S-24', 'S-27', 'S-30', 'S-33', 'S-36'],
    '13': ['S-5', 'S-9', 'S-10', 'S-16', 'S-18', 'S-19', 'S-22', 'S-24', 'S-27', 'S-30', 'S-33', 'S-36', 'S-38'],
    '14': ['S-5', 'S-9', 'S-10', 'S-16', 'S-18', 'S-19', 'S-22', 'S-24', 'S-27', 'S-30', 'S-33', 'S-36', 'S-38', 'S-41'],
    '15': ['S-5', 'S-9', 'S-10', 'S-16', 'S-18', 'S-19', 'S-22', 'S-24', 'S-27', 'S-30', 'S-33', 'S-36', 'S-38', 'S-41', 'S-43']
}

# Loop through each scenario folder
for scenario in os.listdir(base_path):
    scenario_path = os.path.join(base_path, scenario)
    if os.path.isdir(scenario_path):  # Ensure it's a directory
        malicious_sensors = malicious_nodes_dict.get(scenario, [])

        # Loop through each seed folder inside the scenario folder
        for seed_folder in os.listdir(scenario_path):
            seed_path = os.path.join(scenario_path, seed_folder)
            if os.path.isdir(seed_path):  # Ensure it's a directory
                file_path = os.path.join(seed_path, 'Packet Trace.csv')

                # Check if the Packet Trace.csv exists
                if os.path.exists(file_path):
                    try:
                        # Load the CSV file
                        df = pd.read_csv(file_path, encoding='latin1')

                        # Filter PACKET_TYPE to 'Sensing' and STATUS to 'Successful'
                        sensing_packets = df[(df['PACKET_TYPE'] == 'Sensing') & (df['PACKET_STATUS'] == 'Successful')]

                        # Abbreviate the sensor names
                        sensing_packets['SOURCE_ID'] = sensing_packets['SOURCE_ID'].str.replace('SENSOR-', 'S-')
                        sensing_packets['RECEIVER_ID'] = sensing_packets['RECEIVER_ID'].str.replace('SENSOR-', 'S-')

                        # Exclude non-sensor nodes like SinkNode, Router, and Node
                        excluded_nodes = ['SinkNode', 'Router', 'Node']
                        sensing_packets = sensing_packets[~sensing_packets['RECEIVER_ID'].isin(excluded_nodes)]

                        # Get the list of all sensors present in the data (excluding non-sensor nodes)
                        all_sensors_in_data = pd.concat([sensing_packets['SOURCE_ID'], sensing_packets['RECEIVER_ID']]).unique()
                        all_sensors_in_data = [sensor for sensor in all_sensors_in_data if sensor.startswith('S-')]

                        # Count the packets received by each sensor
                        sensor_receive_counts = sensing_packets[sensing_packets['RECEIVER_ID'].str.contains('S-', na=False)]['RECEIVER_ID'].value_counts()

                        # Reindex the DataFrame to include all sensors present in the data, filling missing ones with 0
                        sensor_receive_counts = sensor_receive_counts.reindex(all_sensors_in_data, fill_value=0)

                        # Create a DataFrame for plotting
                        combined_counts = pd.DataFrame({
                            'Data Packets Received': sensor_receive_counts
                        })

                        # Plotting the bar chart for packets received
                        fig, ax = plt.subplots(figsize=(20, 12))  # Maximize figure size for better spacing
                        bars = ax.bar(combined_counts.index, combined_counts['Data Packets Received'], color='lightgreen', width=0.8)  # Increased bar width

                        # Increase spacing between bars
                        plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels to prevent overlap

                        # Add count labels on top of the bars (vertical alignment to prevent merging)
                        for bar in bars:
                            height = bar.get_height()
                            ax.annotate(f'{int(height)}', 
                                        (bar.get_x() + bar.get_width() / 2., height),
                                        ha='center', va='bottom', fontsize=14)  # Increased fontsize for readability

                        plt.title('Number of Data Packets Received', fontsize=36)
                        plt.xlabel('Sensor ID', fontsize=36)
                        plt.ylabel('Data Packets', fontsize=36)

                        # Highlight specific sensor IDs in red based on malicious nodes
                        for label in ax.get_xticklabels():
                            if label.get_text() in malicious_sensors:
                                label.set_color('red')

                        plt.grid(False)  # Disable grid lines

                        # Adjust layout to prevent clipping of labels
                        plt.tight_layout()
                        plt.subplots_adjust(top=0.9, bottom=0.2, left=0.1, right=0.9)  # Adjust margins

                        # Save the plot as an image file with high resolution
                        output_path = os.path.join(seed_path, 'Data.png')
                        plt.savefig(output_path, dpi=300, bbox_inches='tight')  # Save with high resolution and tight bounding box

                        # Display the plot
                        plt.show()
                    except Exception as e:
                        print(f"Error processing file {file_path}: {e}")
                else:
                    print(f"File not found: {file_path}")