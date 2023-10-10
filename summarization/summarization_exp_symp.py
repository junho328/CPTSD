import pandas as pd
import argparse
import openai
from KoBERTScore_j.KoBERTScore.score import BERTScore, bert_score


parser = argparse.ArgumentParser(description='Summarization using experience symptom both') 
parser.add_argument('exp',help='Extracted Expereinece Data file with Excel format', required=True)   
parser.add_argument('symp',help='Extracted Symptom Data file with Excel format',required=True)
parser.add_argument('apikey', help='Your openai api key', required=True)   
parser.add_argument('gpt4summary', help='Filename of GPT4 Summary',required=True)
parser.add_argument('summary', help='True Summary file', required=True)

args = parser.parse_args()
exp_file = args.exp
symp_file = args.symp
api_key = args.apikey
gpt4_summary_filename = args.gpt4summary
true_summary_filename = args.truesummary

def combine_summaries(filename):

    # Load the Excel file
    data_file = pd.ExcelFile(filename)
    
    # Extract the summaries from the second column and convert to a list
    summaries_list = data_file.iloc[:, 1].tolist()
    
    # Remove potential NaN values
    summaries_list = [summary for summary in summaries_list if pd.notna(summary)]
    
    # Combine the summaries into a single string
    combined_summaries = ' '.join(summaries_list)
    
    return combined_summaries

# Define the function to be provided to the user
def generate_simplified_combined_summary(filename, target_col='Estimated symptom'):
    
    # Function to determine if a Korean noun has a final consonant (받침)
    def has_final_consonant(word):
        if not word:
            return False
        last_char = word[-1]
        # Unicode offset for Korean characters
        offset = ord('가')
        # Unicode code for the last character
        last_char_code = ord(last_char) - offset
        # Check if the last character has a final consonant (받침)
        return (last_char_code % 28) != 0
    
    # Load the Excel file
    data_file = pd.ExcelFile(filename)
    
    # Initialize an empty list to store formatted summaries
    formatted_summaries_list = []
    
    # Loop through each row in the DataFrame
    for idx, row in data_file.iterrows():
        # Extract the value from the target column
        symptom = row.get(target_col, None)
        
        # Skip the row if the value is '해당없음' or NaN
        if pd.isna(symptom) or symptom == '해당없음':
            continue
        
        # Determine whether the noun has a 받침 (final consonant) to correctly use '이' or '가'
        particle = '이' if has_final_consonant(symptom) else '가'
        
        # Create a formatted summary for this row using the simplified format
        formatted_summary = f"{symptom}{particle} 나타났다."
        
        # Append the formatted summary to the list
        formatted_summaries_list.append(formatted_summary)
    
    # Combine the formatted summaries into a single string separated by new lines
    combined_formatted_summaries = '\n'.join(formatted_summaries_list)
    
    return combined_formatted_summaries


def gpt4_summary(text,text2):
    openai.api_key = api_key
        
    model = "gpt-4"
    
    query = "해당 인터뷰에 대한 PTSD 경험과 정신건강학적 증상 추출 정보를 250단어로 요약해줘."+"\n 경험 추출 : "+text + "\n 증상 추출 : "+ text2
        
    messages = [
        {"role": "system", "content": 
            "인터뷰를 통해서 해당 인터뷰 대상자가 정신건강학적으로 유의미한 경험을 한 부분을 추출하여 정리하여 하나의 문자열로 합쳤어.\
            추가로 인터뷰를 통해서 인터뷰 대상자가 정신건강학적 증상을 보인 부분을 추출하여 정리하여 하나의 문자열로 합쳤어.\
            너에게 해당 문자열들이 제공되고 이를 합쳐서 요약해달라고 요청을 할거야.\
            해당 요약문은 정신건강의학 의사가 진단 전에 미리 환자를 파악하는데 도움을 주기 위해서 작성되는 것이야.\
            목적에 맡게 요약을 해줘."},
        {"role": "user", "content": query}
        ]
    
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages
    )

    answer = response['choices'][0]['message']['content']

    return answer

def gpt4_true_text_summary(text):
    openai.api_key = api_key
        
    model = "gpt-4"
    
    query = "해당 인터뷰에 대한 PTSD 경험 추출 정보를 공백 포함 650자 내외로 요약해줘."+"\n"+text
        
    messages = [
        {"role": "system", "content": 
            "인터뷰를 통해서 해당 인터뷰 대상자가 정신건강학적으로 유의미한 경험을 한 부분을 추출하여 정리하여 하나의 문자열로 합쳤어.\
            너에게 해당 문자열이 제공되고 이를 요약해달라고 요청을 할거야.\
            해당 요약문은 정신건강의학 의사가 진단 전에 미리 환자를 파악하는데 도움을 주기 위해서 작성되는 것이야.\
            목적에 맡게 요약을 해줘."},
        {"role": "user", "content": query}
        ]
    
    response = openai.ChatCompletion.create(
    model=model,
    messages=messages
    )

    answer = response['choices'][0]['message']['content']

    return answer

def save_gpt4_summary(content,filename):
    with open(f'{filename}.txt', 'w', encoding='utf-8') as file:
        file.write(content)


def read_gpt4_summary(filename):
    with open(f'{filename}.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    return gpt4_summary


def read_true_summary(filename):
    with open(f'{filename}.txt', "r",encoding='utf-8') as file:
        true_summary = file.read()
        
    return true_summary

def save_bertscore(bertscore,filename):
    with open(f'{filename}_BERTScore.txt','w',encoding='utf-8') as file:
        file.write("BERTScore F1: ",bertscore)

def BertScore(gpt4_summary, true_summary):

    model_name = "beomi/kcbert-base"
    bertscore = BERTScore(model_name, best_layer=4)

    references = [
        true_summary
    ]

    candidates = [
        gpt4_summary
    ]

    #R, P, F = bert_score(references, candidates, batch_size=128)
    F = bertscore(references, candidates, batch_size=128)
    
    return F


exp_combined_summaries = combine_summaries(exp_file)
symp_combined_summaries = generate_simplified_combined_summary(symp_file)
gpt4_summary = gpt4_summary(exp_combined_summaries, symp_combined_summaries) # summary_file_name : 'PatientNumber_Summarization_Exp_Symp'

save_gpt4_summary(gpt4_summary,gpt4_summary_filename) 

gpt4_summary = read_gpt4_summary(gpt4_summary_filename)
true_summary = read_true_summary(true_summary_filename)
bertscore_result = BertScore(gpt4_summary,true_summary)
save_bertscore(bertscore_result,gpt4_summary_filename)

