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
        prompt = f"다음 상담 내용을 보고 정신건강의학적으로 유의미한 증상이 있다고 생각되면 해당 증상과 이를 시사하는 구획을 알려줘. {row['Statement']}"
        completion = f"- 증상 : {row['Symptom']}\n- 구획 : {row['Section']}"

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

    # 병합된 데이터를 새로운 파일에 저장
    with open('./json_sumup/P_train_all.json', 'w', encoding='utf-8') as outfile:
        json.dump(merged_data, outfile,ensure_ascii=False)

# Remove 'None(해당없음)' data from jsonl files
def remove_none(origin,new):

    data = []
    with open(origin, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))

    # Filter out elements where completion contains '해당없음'
    filtered_data = [item for item in data if '해당없음' not in item['completion']]

    # Save the filtered data back to a jsonl file
    with open(new, 'w', encoding='utf-8') as f:
        for item in filtered_data:
            f.write(json.dumps(item, ensure_ascii=False) + '\n')