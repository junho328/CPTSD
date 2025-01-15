import pandas as pd
import json

def calculate_metrics(filename):
    # Loading the Excel file
    data = pd.read_excel(filename)

    # Removing rows where 'Estimated symptom' is 'Error'
    data_filtered = data[data['Estimated symptom'] != 'Error']

    # Calculating Accuracy1
    accuracy = (data_filtered['Correct'] == 1).sum() / len(data_filtered)
    
    # Calculating Accuracy2
    accuracy_plus = (data_filtered['Correct2'] == 1).sum() / len(data_filtered)

    # Calculating Sensitivity
    sensitivity_rows = data_filtered[(data_filtered['Symptom'] != 'Not applicable') & (data_filtered['Estimated symptom'] != 'Not applicable')]
    sensitivity = len(sensitivity_rows) / len(data_filtered[data_filtered['Symptom'] != 'Not applicable'])

    # Calculating Specificity
    specificity_rows = data_filtered[(data_filtered['Symptom'] == 'Not applicable') & (data_filtered['Estimated symptom'] == 'Not applicable')]
    specificity = len(specificity_rows) / len(data_filtered[data_filtered['Symptom'] == 'Not applicable'])

    result = {}
    result['Accuracy'] = accuracy
    result['Accuracy_plus'] = accuracy_plus
    result['Sensitivity'] = sensitivity
    result['Specificity'] = specificity
    
    with open(f'{filename}_metrics.json', 'w', encoding='utf-8') as f:
        json.dump(result, f)
    
    
    
