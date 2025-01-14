import pandas as pd
import argparse
import openai

from KoBERTScore_j.KoBERTScore.score import BERTScore, bert_score


parser = argparse.ArgumentParser(description='Summarization using symptom only') 
parser.add_argument('--symp',help='Extracted Symptom Data file with Excel format', required=True)   
parser.add_argument('--apikey', help='Your openai api key', required=True)   
parser.add_argument('--gpt4summary', help='Filename of GPT4 Summary',required=True)
parser.add_argument('--summary', help='True Summary file', required=True)

args = parser.parse_args()
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


def gpt4_summary(text):
    openai.api_key = api_key
        
    model = "gpt-4"

    query = "Summarise the Depression and Bipolar experience extract for this interview in 250 words. "+"\n"+text
        
    messages = [
        {"role": "system", "content": 
            "We have extracted the parts of the interview where the interviewee had a mental health experience of significance, organised them, and combined them into a string.\
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


def read_true_summary(true_summary_file_name):
    with open(f'{true_summary_file_name}.txt', "r",encoding='utf-8') as file:
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


combined_summaries = combine_summaries(symp_file)
gpt4_summary = gpt4_summary(combined_summaries)

save_gpt4_summary(gpt4_summary,gpt4_summary_filename) # summary_file_name : 'PatientNumber_Summarization_Symp_Only'

gpt4_summary = read_gpt4_summary(gpt4_summary_filename)
true_summary = read_true_summary(true_summary_filename)
bertscore_result = BertScore(gpt4_summary,true_summary)
save_bertscore(bertscore_result,gpt4_summary_filename)
