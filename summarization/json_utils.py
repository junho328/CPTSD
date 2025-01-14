import pandas as pd
import json

# Convert excel file to json 
def convert_excel_json(excel_filepath, json_filename):
    
    # Load the Excel file
    df = pd.read_excel(excel_filepath)

    # Initialize an empty list to store the converted data
    data = []

    # Loop over each row in the dataframe
    for idx, row in df.iterrows():
        # Construct the prompt and completion strings
        prompt = f"If you think the following interview has psychiatrically significant symptoms, please tell what they are and the secions that suggest them. {row['Statement']}"
        completion = f"- Symptoms : {row['Symptom']}\n- Sections : {row['Section']}"

        # Add the row to the data list as a dictionary
        data.append({
            "prompt": prompt,
            "completion": completion
        })

    # Specify the JSON filename
    json_filepath = f"json/{json_filename}.json"

    # Write the data to a JSON file
    with open(json_filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Merge json files for fine-tuning
def merge_json(json_files:list):
    
    merged_data = []

    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            merged_data += data

    # Save the merged data to a new file 
    with open('./json_sumup/P_train_all.json', 'w', encoding='utf-8') as outfile:
        json.dump(merged_data, outfile,ensure_ascii=False)

# Remove 'None(Not applicable)' data from jsonl files
def remove_none(origin,new):

    data = []
    with open(origin, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))

    # Filter out elements where completion contains 'Not applicable'
    filtered_data = [item for item in data if 'Not applicable' not in item['completion']]

    # Save the filtered data back to a jsonl file
    with open(new, 'w', encoding='utf-8') as f:
        for item in filtered_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')
