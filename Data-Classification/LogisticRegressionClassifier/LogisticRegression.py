import pandas as pd
from sklearn.linear_model import LogisticRegression
import os

# Load the training data
train_data_path = 'G:\\Test-Scenarios\Data-Classification-of-4-Classifiers\\Training-Data.xlsx'
train_df = pd.read_excel(train_data_path)

# Split the data into features and labels
X_train = train_df.drop('Label', axis=1)
y_train = train_df['Label']

# Train a Logistic Regression classifier
clf = LogisticRegression(random_state=42, max_iter=1000)
clf.fit(X_train, y_train)

# Load the test data
test_data_path = 'G:\\Test-Scenarios\\Data-Classification-of-4-Classifiers\\Test-Data.xlsx'
test_df = pd.read_excel(test_data_path)

# Predict the labels for the test data
predictions = clf.predict(test_df)

# Add the predictions as a new column in the test data DataFrame
test_df['Label'] = predictions

# Get the current working directory
current_directory = os.getcwd()

# Define the output file path within the current working directory
output_file_path = os.path.join(current_directory, 'Test_with_Predictions_LR.xlsx')

# Save the updated DataFrame to a new Excel file
test_df.to_excel(output_file_path, index=False)

print(f"Predictions have been saved to {output_file_path}")
