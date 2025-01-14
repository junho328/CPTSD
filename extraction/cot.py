iimport openai
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

            cot_df.at[index, 'CoT explanation'] = f"{{ {symptom} }} is defined as {{ {definition} }}and, accordingly {{ {section} }} In the section, {{ {symptom} }} appears to be symptomatic."

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
            {"role": "system", "content": "You'll be given a set of example Inputs and Outputs.\
            The Input is the interview transcript, and the Output describes the specific Depression and Bipolar symptoms found in that section based on the definition of Depression and Bipolar symptoms given in the previous Input.\
            When answering, please refer to the input and output forms given above. If there are multiple symptoms in a section, you can answer multiple times.\
            If you think there are multiple Depression and Bipolar symptoms in a given Input Query, you can answer multiple symptoms and sections.\
            If you don't have Depresion and Bipolar symptoms in a given interview, answer ‘Not applicable’."},
            {"role": "user", "content": "Based on the correspondence and content of the given input and output examples, if the patient in the last Input Query shows Depression and Bipolar symptoms, please tell the symptoms and the sections that suggest them."+full_prompt_CoT3}
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
