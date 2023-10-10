import openai
import openpyxl
import pandas as pd
import re
import argparse
import json
from utils import calculate_metrics


parser = argparse.ArgumentParser(description='Extract Symptom and Section with Zero-shot Inference') 
parser.add_argument('data',help='Data File After Label Extraction with Excel Format', required=True)  
parser.add_argument('apikey', help='Your openai api key', required=True)   
parser.add_argument('result',help='Filename of result data', required=True)

args = parser.parse_args()
data_filename = args.data
api_key = args.apikey
result_filename = args.result

def zeroshot(df):
    
    openai.api_key = api_key

    # Check if 'Statement' and 'Symptom' columns exist in the data
    if 'Statement' in df.columns and 'Symptom' in df.columns:
        # Initialize the columns for estimated symptom and section
        df['Estimated symptom'] = ''
        df['Estimated Section'] = ''
        df['Correct'] = 0
        
        for idx, row in df.iterrows():
            try:

                model = "gpt-4"
                
                query = f"다음 상담 내용을 보고 정신건강의학적으로 유의미한 증상이 있다고 생각되면 해당 증상과 이를 시사하는 구획을 알려줘. {row['Statement']}"

                messages = [
                    {"role": "system", "content": "너에게 I와 P7의 인터뷰가 주어질 거야. 다음 상담 내용을 보고 정신건강의학적으로 유의미한 증상이 있다고 생각되면 해당 증상과 이를 시사하는 구획을 알려줘.\
                    증상은 '- 증상 : ...' 형태로 대답하고 구획은 '- 구획 : ...' 형태로 대답해줘. 만약 주어진 인터뷰에 정신건강의학적으로 유의미한 증상이 없다면 '해당없음'이라고 대답해줘.\
                    정신건강의학적으로 유의미한 증상에는 알코올 의존, 불안, 회피, 흉통, 불면, 인지의 부정적 변화, 자기 무가치감, 재경험, 자살사고, 정신운동초조, 과각성, 질식, 흥미상실 이 있어."},
                    {"role": "user", "content": query}]
                
                response = openai.ChatCompletion.create(
                    model=model,
                    messages=messages)
                
            
                # Extract the symptom and the section from the response
                symptom_match = re.search(r'- 증상 : (.*)', response['choices'][0]['message']['content'])
                section_match = re.search(r'- 구획 : (.*)', response['choices'][0]['message']['content'])
                
                if response['choices'][0]['message']['content'] == '해당없음':
                    df.loc[idx, 'Estimated symptom'] = '해당없음'
                    df.loc[idx, 'Estimated Section'] = '해당없음'
                    
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
                df.loc[idx, 'Estimated symptom'] = 'Error'
                df.loc[idx, 'Estimated Section'] = 'Error'
                df.loc[idx, 'Correct'] = 'Error'
        
        # Save the dataframe to a new excel file
        df.to_excel(f'{result_filename}.xlsx', index=False)
    else:
        print("No 'Statement' or 'Symptom' column found in the data.")
    
data = pd.read_excel(f"{data_filename}.xlsx")
zeroshot(data)
calculate_metrics(result_filename)

