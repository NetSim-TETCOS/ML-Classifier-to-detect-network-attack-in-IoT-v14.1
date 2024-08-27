import pandas as pd
import matplotlib.pyplot as plt
import os

# Define the path to the "test scenarios" folder
base_folder = 'G:\\Test-Scenarios'

# Define the malicious sensors for each scenario based on the main folder name
malicious_sensors_map = {
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

# Iterate over each main folder (e.g., '2', '3', ...)
for folder in range(2, 16):
    folder_name = str(folder)
    folder_path = os.path.join(base_folder, folder_name)
    
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
            raise ValueError(f"Required columns are missing from the DataFrame in folder {folder_name}, subfolder {subfolder}.")

        # Filter for 'Control_Packet' packet type and 'Successful' status
        control_packets = df[(df['PACKET_TYPE'] == 'Control_Packet') & (df['PACKET_STATUS'] == 'Successful')]

        # Filter DAO messages
        dao_packets = control_packets[control_packets['CONTROL_PACKET_TYPE/APP_NAME'] == 'DAO']

        # Count DAO messages sent by each sensor
        sent_dao = dao_packets[~dao_packets['SOURCE_ID'].str.contains('SINKNODE|ROUTER', case=False)]['SOURCE_ID'].value_counts()

        # Count DAO messages received by each sensor
        received_dao = dao_packets[~dao_packets['RECEIVER_ID'].str.contains('SINKNODE|ROUTER', case=False)]['RECEIVER_ID'].value_counts()

        # Abbreviate sensor names
        sent_dao.index = sent_dao.index.str.replace('SENSOR-', 'S-')
        received_dao.index = received_dao.index.str.replace('SENSOR-', 'S-')

        # Combine the data for plotting
        combined_counts = pd.DataFrame({
            'Sent': sent_dao,
            'Received': received_dao.reindex(sent_dao.index, fill_value=0)
        }).fillna(0)

        # Plotting
        fig, ax = plt.subplots(figsize=(15, 8))
        bar_width = 0.3
        index = range(len(combined_counts))

        # Increase spacing between bars to avoid overlap
        bar_spacing = bar_width * 1.5
        
        # Plot bars for sent (Sent) and received (Received) messages
        bars_sent = ax.bar(index, combined_counts['Sent'], bar_width, label='DAO Sent', color='skyblue', edgecolor='none')
        bars_received = ax.bar([i + bar_spacing for i in index], combined_counts['Received'], bar_width, label='DAO Received', color='lightgreen', edgecolor='none')

        # Add count labels on top of the bars with vertical orientation and slight offset
        for bar in bars_sent + bars_received:
            height = bar.get_height()
            ax.annotate(f'{int(height)}', 
                        (bar.get_x() + bar.get_width() / 2., height),
                        ha='center', va='bottom', fontsize=12, rotation=90, xytext=(0, 5), textcoords='offset points')

        # Customize the plot
        ax.set_title('Number of DAO Messages Sent and Received', fontsize=32)
        ax.set_xlabel('Sensor ID', fontsize=32)
        ax.set_ylabel('DAO Messages', fontsize=32)
        ax.set_xticks([i + bar_spacing / 2 for i in index])
        ax.set_xticklabels(combined_counts.index, rotation=45, ha='center', va='top', fontsize=14)

        # Highlight specific sensor IDs in red based on malicious nodes
        malicious_sensors = malicious_sensors_map.get(folder_name, [])
        for label in ax.get_xticklabels():
            if label.get_text() in malicious_sensors:
                label.set_color('red')

        # Add legend to indicate colors
        ax.legend(title="Message Type", title_fontsize='20', fontsize='16')

        plt.tight_layout()

        # Save the plot as an image file in the same directory as the packet trace
        output_path = os.path.join(subfolder_path, 'DAO.png')
        plt.savefig(output_path)

        # Display the plot
        plt.show()
