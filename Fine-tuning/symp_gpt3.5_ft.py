import os
import openai
import csv
import pandas as pd
import re
import json
import argparse
from openai import OpenAI

parser = argparse.ArgumentParser(description='estimation to xlsx for ft')    

parser.add_argument('--xlsx', help='excel file path')   
parser.add_argument('--p', help='patient name')

args = parser.parse_args()   

def symp_estimate(input_file,api, model_name,patient_num,k):
    
    df = pd.read_excel(input_file)
    client = openai.Client(api_key=api)

    # Check if 'Statement' and 'Ground-truth label' columns exist in the data
    if 'Statement' in df.columns and 'Ground-truth label' in df.columns:
        # Initialize the columns for estimated symptom and section
        df['Estimation'] = ''
        
        for idx, row in df.iterrows():
            try:

                model = model_name
                
                query = f"다음 인터뷰를 보고 PTSD와 연관된 정신질환 증상이 있다고 생각하면 해당 증상(symptom) 및 이를 나타내는 구획(section)을 알려줘. {row['Statement']}"

                messages = [
                    {"role": "system", "content": "너에게 인터뷰가 주어질 거야. PTSD와 연관된 정신질환 증상(symptom) 및 이를 나타내는 구획(section)을 대답할 때, [{'symptom': '...', 'section': '...'}, {'symptom': '...', 'section': '...'}, ...] 형태로 반드시 대답해줘. \
                    특정 구획(section)에 여러 증상(symptom)이 있다고 생각하면, [{'symptom': '..., ...', 'section': '...'}, ...] 형태로 대답하면 돼. 만약 주어진 인터뷰에 PTSD와 연관된 정신질환 증상이 없다면 [{'symptom': 'none', 'section': 'none'}] 이라고 대답해줘.\
                    증상(symptom)을 대답할 때는 label로 대답해주고, 구획(section)을 대답할 때는 주어진 인터뷰 문구 그대로 가져와서 대답해줘."},
                    {"role": "user", "content": query}]
                
                response = client.chat.completions.create(
                    model = model,
                    messages = messages)
                
                df.loc[idx, 'Estimation'] = response.choices[0].message.content
            
                    
            except: #changed it to no-specification for error name
                df.loc[idx, 'Estimation'] = 'Error'
                
        # Save the dataframe to a new excel file
        if k != 1:
            df.to_excel(f'result_symp_estimation_{k}/symp_gpt3.5_{model_name}_{patient_num}.xlsx', index=False)
        else:
            df.to_excel(f'result_symp_estimation/symp_gpt3.5_{model_name}_{patient_num}.xlsx', index=False)
    else:
        print("No 'Statement' or 'Symptom' column found in the data.")


######################
        
#Final Fine-tuned Model
#epoch 5 lr default
#model : ur_model

symp_estimate(f'../label extract/{args.p}.xlsx',"ur_key", "ur_model", args.p,1)
symp_estimate(f'../label extract/{args.p}.xlsx',"ur_key", "ur_model", args.p,2)
symp_estimate(f'../label extract/{args.p}.xlsx',"ur_key", "ur_model", args.p,3)

