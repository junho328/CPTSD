import pandas as pd
import argparse
import openai
from KoBERTScore_j.KoBERTScore.score import BERTScore, bert_score


parser = argparse.ArgumentParser(description='Summarization using experience symptom both') 
parser.add_argument('--exp',help='Extracted Expereinece Data file with Excel format', required=True)   
parser.add_argument('--symp',help='Extracted Symptom Data file with Excel format',required=True)
parser.add_argument('--apikey', help='Your openai api key', required=True)   
parser.add_argument('--gpt4summary', help='Filename of GPT4 Summary',required=True)
parser.add_argument('--summary', help='True Summary file', required=True)

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
    
    # Load the Excel file
    data_file = pd.ExcelFile(filename)
    
    # Initialize an empty list to store formatted summaries
    formatted_summaries_list = []
    
    # Loop through each row in the DataFrame
    for idx, row in data_file.iterrows():
        # Extract the value from the target column
        symptom = row.get(target_col, None)
        
        # Skip the row if the value is '해당없음' or NaN
        if pd.isna(symptom) or symptom == 'Not applicable':
            continue
        
        # Create a formatted summary for this row using the simplified format
        formatted_summary = f"{symptom} appears."
        
        # Append the formatted summary to the list
        formatted_summaries_list.append(formatted_summary)
    
    # Combine the formatted summaries into a single string separated by new lines
    combined_formatted_summaries = '\n'.join(formatted_summaries_list)
    
    return combined_formatted_summaries


def gpt4_summary(text,text2):
    openai.api_key = api_key
        
    model = "gpt-4"
    
    query = "In 250 words, summarise the Depression and Bipolar experience and mental health symptom extraction information for this interview."+"\n Extracting experience : "+text + "\n Extracting symptoms : "+ text2
        
    messages = [
        {"role": "system", "content": 
            "The interviewer's mental health experiences were extracted, organised and combined into a single string.\
            You will be given that string and asked to summarise it.\
            The summaries are intended to help mental health practitioners get to know the patient before diagnosis.\
            Summarise for this purpose."},
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
    
    query = "Please summarise the Depression and Bipolar experience extraction information for this interview in 250 characters or less, including spaces."+"\n"+text
        
    messages = [
        {"role": "system", "content": 
            "We've extracted the parts of the interview where the interviewee had a mental health experience of significance, organised them, and combined them into a string.\
            You will be given that string and asked to summarise it.\
            The summaries are intended to help mental health practitioners get to know the patient before diagnosis.\
            Summarise for this purpose."},
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

