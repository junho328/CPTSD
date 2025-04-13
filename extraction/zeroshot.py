import openai
import os
import openpyxl
import pandas as pd
import numpy as np
import re
import argparse
import json

from openai import OpenAI
from utils import extract_split_and_deduplicate_symptoms
from utils import calculate_num_set
from utils import calculate_and_average_metrics
from utils import extract_sections
from utils import tokenize_numbering
from utils import mid_token_calc
from utils import mid_token_dist_calc


parser = argparse.ArgumentParser(description='Estimate Symptom and Section with Zero-shot Inference') 
parser.add_argument('--data', help='Data File After Label Extraction with Excel Format', required=True)  
parser.add_argument('--apikey', help='Your openai api key', required=True)   
parser.add_argument('--result', help='Filename of gpt result data', required=True)

args = parser.parse_args()
data_filename = args.data
api_key = args.apikey
gpt_result_filename = args.result


def zeroshot(df):
    
    client = OpenAI(api_key = api_key)

    # Check if 'Statement' and 'Ground-truth label' columns exist in the data
    if 'Statement' in df.columns and 'Ground-truth label' in df.columns:
        # Initialize the columns for estimated symptom and section
        df['Estimation'] = ''
        
        for idx, row in df.iterrows():
            try:

                model = "gpt-4-1106-preview"
                
                query = f"다음 인터뷰를 보고 PTSD와 연관된 정신질환 증상이 있다고 생각하면 해당 증상(symptom) 및 이를 나타내는 구획(section)을 알려줘. {row['Statement']}"

                messages = [
                    {"role": "system", "content": "너에게 인터뷰가 주어질 거야. PTSD와 연관된 정신질환 증상(symptom) 및 이를 나타내는 구획(section)을 대답할 때, [{'symptom': '...', 'section': '...'}, {'symptom': '...', 'section': '...'}, ...] 형태로 반드시 대답해줘. \
                    특정 구획(section)에 여러 증상(symptom)이 있다고 생각하면, [{'symptom': '..., ...', 'section': '...'}, ...] 형태로 대답하면 돼. 만약 주어진 인터뷰에 PTSD와 연관된 정신질환 증상이 없다면 [{'symptom': 'none', 'section': 'none'}] 이라고 대답해줘.\
                    PTSD와 연관된 정신질환 증상(symptom)을 label(symptom)의 형태로 알려줄게. 다음과 같은 증상(symptom)들이 있어.\
                    reex(Reexperience), avoid(Avoidance), ncog(Negative change in cognition), nmood(Negative change in mood), arousal(Arousal), disso(Dissociation), demo(Difficulty in emotional regulation), nself(Negative self-image), \
                    drelat(Difficulty in relationship), depress(Depressed mood), dinter(Decreased interest), dapp(Decreased appetite), iapp(Increased appetite), insom(Insomnia), hsom(Hypersomnia), agit(Psychomotor agitation), retard(Psychomotor retardation), \
                    fati(Fatigue), worth(Worthlessness), guilty(Excessive guilt), dcon(Decreased concentration), dmemo(Decreased memory), ddeci(Decreased decision), suii(Suicidal ideation), suip(Suicide plan), suia(Suicide attempt), anxiety(Anxiety), \
                    palpi(Palpitation), sweat(Sweating), trembl(Trembling), breath(Shortness of breath), chok(Choking), chest(Chest pain), nausea(Nausea), dizzy(Dizziness), chhe(Chilling), pares(Paresthesia), control(Loss of control), dying(Fear of dying), \
                    adepen(Alcohol dependence), atoler(Alcohol tolerance), awithdr(Alcohol withdrawal) 와 같이 총 42개의 증상(symptom)이 있어. \
                    증상(symptom)을 대답할 때는 반드시 label로 대답해주고, 구획(section)을 대답할 때는 반드시 주어진 인터뷰 문구 그대로 가져와서 대답해줘."},
                    {"role": "user", "content": query}]
                
                response = client.chat.completions.create(
                    model = model,
                    messages = messages)
                
                df.loc[idx, 'Estimation'] = response.choices[0].message.content
            
                    
            except openai.error.InvalidRequestError:
                df.loc[idx, 'Estimation'] = 'Error'
                
        # Save the dataframe to a new excel file
        df.to_excel(f'{result_filename}.xlsx', index=False)
    else:
        print("No 'Statement' or 'Symptom' column found in the data.")

# zero-shot inference        
data = pd.read_excel(f"{data_filename}.xlsx")
zeroshot(data)

# extract ground-truth symptoms and estimated symptoms
gpt_result = pd.read_excel(f"{gpt_result_filename}.xlsx")
extract_symp1 = extract_split_and_deduplicate_symptoms(gpt_result, "Ground-truth label", "Symptom")
extract_symp2 = extract_split_and_deduplicate_symptoms(extract_symp1, "Estimation", "Estimated Symptom")

# calcuate metrics used for multi-label classification in estimating symptoms
num_set_extract_symp2 = calculate_num_set(extract_symp2) 
calculate_and_average_metrics(num_set_extract_symp2, zeroshot_metric)

# extract ground-truth sections and estimated sections
extract_sec = extract_sections(gpt_result)

# tokenize the text of ground-truth sections and estimated sections and number tokens of the text
token_num_sec = tokenize_numbering(extract_sec, token_num_sec)

# calculate the mid-token of the ground-truth sections and estimated sections
mid_token_calc_sec = mid_token_calc(token_num_sec, mid_token_calc_sec)

# calculate the recall mid-token distance
mid_token_dist_calc(mid_token_calc_sec, zeroshot_midtoken_dist)
