import pandas as pd
import json
import os
import argparse   

parser = argparse.ArgumentParser(description='xlsx to json for ft')   

parser.add_argument('--xlsx', help='excel file path')    
parser.add_argument('--json', help='json file name')

args = parser.parse_args()    



def convert_excel_to_json(excel_filepath, json_filename):
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

    return json_filepath


