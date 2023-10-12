import openai
import openpyxl
import pandas as pd
import argparse

parser = argparse.ArgumentParser(description='Extract Symptom and Section with Chain-of-Thought method') 
parser.add_argument('--data',help='Data File After Label Extraction with Excel Format', required=True)  
parser.add_argument('--definition',help='Symptomt Definition File with Excel Format', required=True)
parser.add_argument('--apikey', help='Your openai api key', required=True)   
parser.add_argument('--result',help='Filename of result data', required=True)

args = parser.parse_args()
data_filename = args.data
symptom_definition_file = args.definition
api_key = args.apikey
result_filename = args.result

def add_CoT_explanation(cot_df, symptom_definition_df):
    
    # Add 'CoT explanation' column 
    cot_df['CoT explanation'] = ''

    for index, row in cot_df.iterrows():
        symptom = row['Symptom']
        section = row['Section']
        
        definition = symptom_definition_df[symptom_definition_df['symptom'] == symptom]['definition'].values
        if len(definition) > 0:
            definition = definition[0]

            cot_df.at[index, 'CoT explanation'] = f"{{ {symptom} }}의 정의는 {{ {definition} }}이고, 이에 따라 {{ {section} }} 구획에서 {{ {symptom} }} 증상이 나타나는 것으로 보입니다."

    return cot_df

def create_CoT_prompt(df):
    
    prompts = []

    for _, row in df.iterrows():
        statement = row['Statement']
        CoT_expl = row['CoT explanation']

        prompt = f"Input: {statement}\nOutput: {CoT_expl}"
        prompts.append(prompt)

    # Joining all the prompts together
    full_prompt = "\n\n".join(prompts)
    
    return full_prompt

def cot(df1, df2):

    # Initialize the columns for estimated symptom and section
    df2['GPT-4 Output'] = ''

    openai.api_key = api_key
    model = "gpt-4"

    for idx, statement in enumerate(df2['Statement']):

        # Construct the full prompt
        full_prompt_CoT3 = create_CoT_prompt(df1)
        full_prompt_CoT3 += f"\n\n Input Query: {statement}"


        messages = [
            {"role": "system", "content": "너에게 Input과 Output 예시 set들이 주어질 거야.\
            Input에는 상담 내용이 있고, Output에는 직전 Input에서 주어진 PTSD 증상의 정의를 기반으로 해당 구획에서 발견되는 특정 PTSD 증상을 설명하고 있어.\
            대답을 할 때 위에 주어진 Input과 Output 형태를 참고해서 대답해줘. 하나의 구획에 여러 증상이 존재한다면 증상을 여러번 대답해도 돼.\
            주어진 Input Query에 PTSD 증상이 여러개 존재한다고 생각하면 증상과 구획을 여러번 대답해줘도 돼.\
            만약 주어진 인터뷰에 PTSD 증상이 없다면 '해당없음'이라고 대답해줘."},
            {"role": "user", "content": "주어진 Input과 Output 예시들의 대응관계와 내용을 바탕으로 해서, 마지막 Input Query에 나타난 상담 내용을 보고 PTSD 증상이 나타나면 해당 증상과 이를 시사하는 구획을 알려줘."+full_prompt_CoT3}
        ]
        
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages)

        answer = response['choices'][0]['message']['content']
        df2['GPT-4 Output'].iloc[idx] = answer

    df2.to_excel(f'{result_filename}.xlsx', index=False)
    
data = pd.read_excel(f'{data_filename}.xlsx')
symptom_definition = pd.read_excel(f'{symptom_definition_file}.xlsx')
cot_data = add_CoT_explanation(data,symptom_definition)
cot(cot_data,data)
