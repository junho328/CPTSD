import openai
import openpyxl
import pandas as pd
import argparse
import time
import json
import re

from openai import OpenAI
from utils import extract_symp_from_df_label
from utils import extract_symp_from_df_icl
from utils import calculate_num_set
from utils import calculate_and_average_metrics
from utils import extract_sections
from utils import tokenize_numbering
from utils import mid_token_calc
from utils import mid_token_dist_calc

parser = argparse.ArgumentParser(description='Estimate Symptom and Section with In-Context Learning method') 
parser.add_argument('--data',help='Data File After Label Extraction with Excel Format', required=True)  
parser.add_argument('--examplar',help='Examplar File for In-Context Learning with Excel Format', required=True)
parser.add_argument('--apikey', help='Your openai api key', required=True)   
parser.add_argument('--result',help='Filename of gpt result data', required=True)

args = parser.parse_args()
data_filename = args.data
examplar_file = args.examplar
api_key = args.apikey
gpt_result_filename = args.result


def create_icl_ex(df):
    
    prompts = []

    for _, row in df.iterrows():
        statement = row['Statement']
        gt_label = row['Ground-truth label']

        prompt = f"Input: {statement}\nOutput: {gt_label}"
        prompts.append(prompt)

    # Joining all the prompts together
    full_prompt = "\n\n".join(prompts)
    
    return full_prompt


def icl(df1, df2):

    # Add 'Estimation' Column
    df2['Estimation'] = ''

    client = openai.Client(api_key = api_key)
    
    model = "gpt-4-1106-preview"
    
    ignore = 0

    # enumerate를 사용하여 인덱스(idx)와 값(statement)를 함께 얻음
    for idx, statement in enumerate(df2['Statement']):

        # Construct the full prompt
        full_prompt = create_icl_ex(df1)
        full_prompt += f"\n\nInput: {statement}"

        # 메시지 설정하기
        messages = [
            {"role": "system", "content": "너에게 여러 세트의 Input과 Output이 주어질 거야.\
                    Input에는 인터뷰 내용이 주어지고, Output에는 직전 Input에서 나타나는 PTSD와 연관된 정신질환 증상(symptom)과 증상(symptom)이 나타난 구획(section)이 쓰여있어.\
                    마지막에 주어지는 Input에 나타난 인터뷰 내용을 보고 PTSD와 연관된 정신질환 증상(symptom) 및 이를 나타내는 구획(section)을 대답할 때, [{'symptom': '...', 'section': '...'}, {'symptom': '...', 'section': '...'}, ...] 형태로 반드시 대답해줘. \
                    특정 구획(section)에 여러 증상(symptom)이 있다고 생각하면, [{'symptom': '..., ...', 'section': '...'}, ...] 형태로 대답하면 돼. 만약 주어진 인터뷰에 PTSD와 연관된 정신질환 증상이 없다면 [{'symptom': 'none', 'section': 'none'}] 이라고 대답해줘.\
                    이전의 Input, Output 세트들을 참고해서 in-context learning을 활용하여 대답해주면 돼.\
                    PTSD와 연관된 정신질환 증상(symptom)을 label(symptom)의 형태로 알려줄게. 다음과 같은 증상(symptom)들이 있어.\
                    reex(Reexperience), avoid(Avoidance), ncog(Negative change in cognition), nmood(Negative change in mood), arousal(Arousal), disso(Dissociation), demo(Difficulty in emotional regulation), nself(Negative self-image), \
                    drelat(Difficulty in relationship), depress(Depressed mood), dinter(Decreased interest), dapp(Decreased appetite), iapp(Increased appetite), insom(Insomnia), hsom(Hypersomnia), agit(Psychomotor agitation), retard(Psychomotor retardation), \
                    fati(Fatigue), worth(Worthlessness), guilty(Excessive guilt), dcon(Decreased concentration), dmemo(Decreased memory), ddeci(Decreased decision), suii(Suicidal ideation), suip(Suicide plan), suia(Suicide attempt), anxiety(Anxiety), \
                    palpi(Palpitation), sweat(Sweating), trembl(Trembling), breath(Shortness of breath), chok(Choking), chest(Chest pain), nausea(Nausea), dizzy(Dizziness), chhe(Chilling), pares(Paresthesia), control(Loss of control), dying(Fear of dying), \
                    adepen(Alcohol dependence), atoler(Alcohol tolerance), awithdr(Alcohol withdrawal) 와 같이 총 42개의 증상(symptom)이 있어.\
                    증상(symptom)을 대답할 때는 반드시 label로 대답해주고, 구획(section)을 대답할 때는 반드시 주어진 인터뷰 문구 그대로 가져와서 대답해줘."},
            {"role": "user", "content": "주어진 Input과 Output 예시들의 대응관계를 바탕으로, 마지막 Input에 나타난 인터뷰를 보고 PTSD와 연관된 정신질환 증상이 있다고 생각하면 해당 증상(symptom) 및 이를 나타내는 구획(section)을 알려줘.\n"+full_prompt}
        ]
        try:
            response = client.chat.completions.create(
                model = model,
                messages = messages)

            answer = response.choices[0].message.content
            
            df2['Estimation'].iloc[idx] = answer
            
            time.sleep(20)
        
        except Exception as e:
                print(e)
                if ("Limit" in str(e)):
                    time.sleep(10)
                
                else:
                    ignore += 1
                    print('ignored', ignore)
        

    df2.to_excel(f'{gpt_result_filename}.xlsx', index=False)


# in-context learning
data = pd.read_excel(f"{data_filename}.xlsx")
examplar = pd.read_excel(f"{examplar_file}.xlsx")
icl(examplar,data)

# extract ground-truth symptoms
gpt_result = pd.read_excel(f"{gpt_result_filename}.xlsx")
extract_symp1 = extract_symp_from_df_label(gpt_result, "Ground-truth label", "Symptom")

# extract estimated symptoms
extract_symp2 = extract_symp_from_df_icl(extract_symp1, "Estimation", "Estimated Symptom")

# calcuate metrics used for multi-label classification in estimating symptoms
num_set_extract_symp2 = calculate_num_set(extract_symp2) 
calculate_and_average_metrics(num_set_extract_symp2)

# extract ground-truth sections and estimated sections
extract_sec = extract_sections(gpt_result)

# tokenize the text of ground-truth sections and estimated sections and number tokens of the text
token_num_sec = tokenize_numbering(extract_sec)

# calculate the mid-token of the ground-truth sections and estimated sections
mid_token_calc_sec = mid_token_calc(token_num_sec)

# calculate the recall mid-token distance
mid_token_dist_calc(mid_token_calc_sec)
