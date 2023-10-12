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

        prompt = f"Input: {statement}\nOutput: - 증상: {symptom} - 구획: {section}"
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
            {"role": "system", "content": "너에게 여러 세트의 Input과 Output이 주어질 거야.\
                    Input에는 상담 내용이 주어지고, Output에는 바로 앞 Input에서 나타나는 PTSD 증상과 증상이 나타난 구획이 쓰여있어.\
                    마지막에 주어지는 Input Query에 나타난 상담 내용을 보고 PTSD 증상이 있다고 생각하면 해당 증상과 이를 시사하는 구획을 알려주면 돼.\
                    대답을 할 때 증상은 '- 증상: ...' 형태로 대답하고 구획은 '- 구획: ...' 형태로 대답해줘.\
                    만약 주어진 인터뷰에 PTSD 증상이 없다면 반드시 '해당없음'이라고 대답해줘야 해. 마음대로 PTSD 증상이 있다고 판단하지 않았으면 좋겠어.\
                    확신이 있는 경우에만, 증상과 구획을 알려줘.\
                    증상은 in-context learning을 활용하여 앞선 Input과 Output 세트들을 참고해서 대답해주면 돼."},
            {"role": "user", "content": "주어진 Input과 Output 예시들의 대응관계와 내용을 바탕으로 해서, 마지막 Input Query에 나타난 상담 내용을 보고 PTSD 증상이 나타나면 해당 증상과 이를 시사하는 구획을 알려줘. 만약 주어진 인터뷰에 PTSD 증상이 없다면 '해당없음'이라고 대답해줘."+full_prompt}
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
