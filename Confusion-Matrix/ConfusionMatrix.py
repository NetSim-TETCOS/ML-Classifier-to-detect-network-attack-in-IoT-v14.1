import pandas as pd
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score, f1_score
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Load data from Excel files
predicted_df = pd.read_excel('E:\\Test-Training-Data\\Confusion-Matrix\\NaiveBayes.xlsx')
actual_df = pd.read_excel('E:\\Test-Training-Data\\Confusion-Matrix\\Test-Data-With-Label.xlsx')

# Extract labels (assuming the columns are named 'Label' or adjust as necessary)
predicted_labels = predicted_df['Label']
actual_labels = actual_df['Label']

# Calculate the confusion matrix
cm = confusion_matrix(actual_labels, predicted_labels)

# Extract TP, TN, FP, FN
TN, FP, FN, TP = cm.ravel()

# Calculate additional metrics
accuracy = accuracy_score(actual_labels, predicted_labels)
precision = precision_score(actual_labels, predicted_labels)
recall = recall_score(actual_labels, predicted_labels)
f1 = f1_score(actual_labels, predicted_labels)

# Display the confusion matrix with metrics
fig, ax = plt.subplots(figsize=(12, 8))  # Increase figure size

# Create a mask for the confusion matrix to differentiate positives and negatives
positive_mask = np.array([[False, True], [True, False]])  # Positions for TP and FP
negative_mask = np.array([[True, False], [False, True]])  # Positions for TN and FN

# Define a custom color map with light green for positives and light sky blue for negatives
cmap_pos = sns.color_palette(["#a1d99b"])  # Light green for positives
cmap_neg = sns.color_palette(["#9ecae1"])  # Light sky blue for negatives

# Plot confusion matrix with seaborn heatmap for positives
sns.heatmap(cm, annot=True, fmt='d', cbar=False, ax=ax,
            mask=~positive_mask, cmap=cmap_pos, linewidths=1, linecolor='black', 
            annot_kws={"size": 30, "ha": "left"})

# Plot confusion matrix with seaborn heatmap for negatives
sns.heatmap(cm, annot=True, fmt='d', cbar=False, ax=ax,
            mask=~negative_mask, cmap=cmap_neg, linewidths=1, linecolor='black', 
            annot_kws={"size": 30, "ha": "left"})

# Set the size for the x and y tick labels
ax.tick_params(axis='both', which='major', labelsize=25)

# Centering the title
plt.title('Confusion Matrix for Naive Bayes Classifier', fontsize=30, x=0.5, y=1.1)

# Adjust the metrics text and its position below the plot
metrics_text = (f"True Positives (TP): {TP}\n"
                f"True Negatives (TN): {TN}\n"
                f"False Positives (FP): {FP}\n"
                f"False Negatives (FN): {FN}\n\n"
                f"Accuracy: {accuracy:.4f}\n"
                f"Precision: {precision:.4f}\n"
                f"Recall: {recall:.4f}\n"
                f"F1 Score: {f1:.4f}")

# Adding the metrics below the plot
plt.figtext(0.5, -0.08, metrics_text, ha='center', va='center', fontsize=25, bbox=dict(facecolor='white', alpha=0.8))

plt.tight_layout(rect=[0, 0.1, 1, 0.9])  # Adjust layout to make space for text below

# Save the figure in the same directory as the script
output_file = os.path.join(os.getcwd(), 'Confusion_Matrix_with_bayes.png')
plt.savefig(output_file, bbox_inches='tight')

plt.show()

print(f"Confusion matrix plot saved as {output_file}")
