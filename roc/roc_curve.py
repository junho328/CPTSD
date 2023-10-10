import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Draw ROC Curve with thresholds') 
parser.add_argument('data',help='Data File with Excel Format', required=True)  
parser.add_argument('name',help='Image Name', required=True)  

args = parser.parse_args()
data = args.data
img_name = args.name

def plot_roc(df, img_name, actual_col, predicted_col, confidence_col):
    # Filter out rows with 'Error'
    filtered_data = df[
        (df[predicted_col] != 'Error') & 
        (df[confidence_col] != 'error')
    ]
    # Convert 'confidence' column to float
    filtered_data[confidence_col] = pd.to_numeric(filtered_data[confidence_col], errors='coerce')

    # Create true binary labels
    true_labels = (filtered_data[actual_col] != '해당없음').astype(int)

    # Create predicted binary labels
    predicted_labels = (filtered_data[predicted_col] != '해당없음').astype(int)

    # Create new_confidence
    new_confidence = filtered_data[confidence_col].where(predicted_labels == 1, 1 - filtered_data[confidence_col])

    # Filter out rows with NaN values in new_confidence
    non_nan_indices = new_confidence.notna()
    filtered_true_labels = true_labels[non_nan_indices]
    filtered_new_confidence = new_confidence[non_nan_indices]

    # Compute ROC curve and ROC area
    fpr, tpr, thresholds = roc_curve(filtered_true_labels, filtered_new_confidence)
    roc_auc = auc(fpr, tpr)

    # Plot ROC curve
    plt.figure(figsize=(10, 7))
    plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'ROC curve (area = {roc_auc:.2f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label = "Random Classifier")
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('Receiver Operating Characteristic (ROC) Curve based on Logprob from GPT-3')
    plt.legend(loc="lower right")
    plt.savefig(f'{img_name}.png')

data = pd.read_excel(data) 
threshold_values = plot_roc(data, img_name, 'Symptom', 'Estimated symptom', 'confidence')