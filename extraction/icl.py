import openai
import openpyxl
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Extract Symptom and Section with In-Context Learning method') 
parser.add_argument('--data',help='Data File After Label Extraction with Excel Format', required=True)  
parser.add_argument('--examplar',help='Examplar File for In-Context Learning with Excel Format', required=True)
parser.add_argument('--apikey', help='Your openai api key', required=True)   
parser.add_argument('--result',help='Filename of result data', required=True)

args = parser.parse_args()
data_filename = args.data
examplar_file = args.examplar
api_key = args.apikey
result_filename = args.result

def create_icl_prompt(df):
    
    prompts = []

    for _, row in df.iterrows():
        statement = row['Statement']
        section = row['Section']
        symptom = row['Symptom']

        prompt = f"Input: {statement}\nOutput: - Symptoms : {symptom} - Sections : {section}"
        prompts.append(prompt)

    # Joining all the prompts together
    full_prompt = "\n\n".join(prompts)
    
    return full_prompt

def icl(df1, df2):

    # Add 'GPT-4 Output' Column
    df2['GPT-4 Output'] = ''

    openai.api_key = api_key
    
    model = "gpt-4"

    # enumerate를 사용하여 인덱스(idx)와 값(statement)를 함께 얻음
    for idx, statement in enumerate(df2['Statement']):

        # Construct the full prompt
        full_prompt = create_icl_prompt(df1)
        full_prompt += f"\n\n Input Query: {statement}"

        # 메시지 설정하기
        messages = [
            {"role": "system", "content": "You'll have several sets of inputs and outputs.\
                    The input is a interview transcript, and the output is a list of Depression and Bipolar symptoms and the section in which they occurred in the previous input.\
                    If you think the patient has Depression and Bipolar symptoms in a given input query, please tell the symptoms and the sections that suggest them.\
                    When answering, please answer symptoms in the form ‘- Symptoms : ...’ and sections in the form ‘- Sections : ...’.\
                    If you don't have Depression and Bipolar symptoms in a given interview, pelase answer ‘Not applicable’. Do not arbitrarily assume you have Depression or Bipolar symptoms.\
                    Only if you're sure, tell us the symptoms and sections.\
                    The symptoms can be answered using in-context learning by referring to the previous set of inputs and outputs."},
            {"role": "user", "content": "Based on the correspondence and content of the given input and output examples, identify the symptoms of Psychiatric disorders and the sections that suggest them, if any, in the interview shown in the last Input Query. If there are no Depression or Bipolar symptoms in the given interview, answer ‘Not applicable’."+full_prompt}
        ]

        response = openai.ChatCompletion.create(
            model=model,
            messages=messages)
        
        answer = response['choices'][0]['message']['content']
        df2['GPT-4 Output'].iloc[idx] = answer

    df2.to_excel(f'{result_filename}.xlsx', index=False)
    
data = pd.read_excel(f"{data_filename}.xlsx")
examplar = pd.read_excel(f"{examplar_file}.xlsx")
icl(examplar,data)
