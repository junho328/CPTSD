import openai
import openpyxl
import pandas as pd
import re
import argparse
import json
from utils import calculate_metrics


parser = argparse.ArgumentParser(description='Extract Symptom and Section with Zero-shot Inference') 
parser.add_argument('--data',help='Data File After Label Extraction with Excel Format', required=True)  
parser.add_argument('--apikey', help='Your openai api key', required=True)   
parser.add_argument('--result',help='Filename of result data', required=True)

args = parser.parse_args()
data_filename = args.data
api_key = args.apikey
result_filename = args.result

def zeroshot(df):
    
    openai.api_key = api_key

    # Check if 'Statement' and 'Symptom' columns exist in the data
    if 'Statement' in df.columns and 'Symptom' in df.columns:
        # Initialize the columns for estimated symptom and section
        df['Estimated Symptom'] = ''
        df['Estimated Section'] = ''
        df['Correct'] = 0
        
        for idx, row in df.iterrows():
            try:

                model = "gpt-4"
                
                query = f"If you think the following consultation has psychiatrically significant symptoms, please tell what they are and the sections in the text where you find these symptoms. {row['Statement']}"

                messages = [
                    {"role": "system", "content": "
                    You will be given the following interview between a psychiatrist and a patient. If you think there are any psychiatrically significant symptoms in the following interview, please tell what they are and the sections that suggest them.\
                    Please answer symptoms in the form '- Symptoms : ...' and sections in the form '- Sections : ...'. If there are no psychiatrically significant symptoms in a given interview, please answer 'N/A'.\
                    Psychiatrically significant symptoms include alcohol dependence, anxiety, avoidance, chest pain, insomnia, negative cognitive changes, feelings of self-worthlessness, reexperiencing, suicidal ideation, psychomotor agitation, hyperarousal, choking, and loss of interest.\
                    "},
                    {"role": "user", "content": query}]
                
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages)
                
            
                # Extract the symptom and the section from the response
                symptom_match = re.search(r'- Symptoms : (.*)', response['choices'][0]['message']['content'])
                section_match = re.search(r'- Sections : (.*)', response['choices'][0]['message']['content'])
                
                if response['choices'][0]['message']['content'] == 'N/A':
                    df.loc[idx, 'Estimated Symptom'] = 'Not applicable'
                    df.loc[idx, 'Estimated Section'] = 'Not applicable'
                    
                    # Check if the estimated symptom matches the actual symptom
                    if symptom == row['Symptom']:
                        df.loc[idx, 'Correct'] = 1
            
                elif symptom_match:
                    # Strip the leading ':' and whitespace
                    symptom = symptom_match.group(1).lstrip(': ').strip()
                    df.loc[idx, 'Estimated symptom'] = symptom
                
                    # Check if the estimated symptom matches the actual symptom
                    if symptom == row['Symptom']:
                        df.loc[idx, 'Correct'] = 1
            
                if section_match:
                    # Strip the leading ':' and whitespace
                    section = section_match.group(1).lstrip(': ').strip()
                    df.loc[idx, 'Estimated Section'] = section
                    
            except openai.error.InvalidRequestError:
                df.loc[idx, 'Estimated Symptom'] = 'Error'
                df.loc[idx, 'Estimated Section'] = 'Error'
                df.loc[idx, 'Correct'] = 'Error'
        
        # Save the dataframe to a new excel file
        df.to_excel(f'{result_filename}.xlsx', index=False)
    else:
        print("No 'Statement' or 'Symptom' column found in the data.")
    
data = pd.read_excel(f"{data_filename}.xlsx")
zeroshot(data)
calculate_metrics(result_filename)

