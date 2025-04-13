import openai
import openpyxl
import pandas as pd
import argparse
import time
import json
import re
import os
import pickle

from openai import OpenAI
from utils import extract_symp_from_df_label
from utils import extract_symp_from_df_rag
from utils import calculate_num_set
from utils import calculate_and_average_metrics
from utils import tokenize_numbering
from utils import mid_token_calc
from utils import mid_token_dist_calc

from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain.vectorstores import FAISS
from langchain.storage import LocalFileStore
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.callbacks import StdOutCallbackHandler

parser = argparse.ArgumentParser(description='Estimate Symptom and Section with Zero-shot Inference with RAG')
parser.add_argument('--trauma', help='Trauma and Stressor-Related Disorders chapter of the DSM-5 with PDF Format', required=True)  
parser.add_argument('--data', help='Data File After Label Extraction with Excel Format', required=True)  
parser.add_argument('--apikey', help='Your openai api key', required=True)   
parser.add_argument('--result', help='Filename of gpt result data', required=True)

args = parser.parse_args()
data_filename = args.data
api_key = args.apikey
gpt_result_filename = args.result
DSM_5_trauma = args.trauma

api_key = os.environ.get(api_key)
api_key = api_key

trauma_loader = PyMuPDFLoader(f"{DSM_5_trauma}.pdf")
trauma_documents = trauma_loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50,
    length_function = len
)
documnet_chunks = text_splitter.transform_documents(trauma_documents)

store = LocalFileStore('./DSM5_cache/')

# create an embedder
core_embeddings_model = OpenAIEmbeddings(openai_api_key = api_key) #text-embedding-ada

embedder = CacheBackedEmbeddings.from_bytes_store(
    core_embeddings_model,
    store,
    namespace = core_embeddings_model.model
)
# store embeddings in vector store
vectorstore = FAISS.from_documents(documnet_chunks, embedder)

# instantiate a retriever
retriever = vectorstore.as_retriever()

# template for zero-shot with RAG
open_ai_model = "gpt-4-1106-preview"
llm = ChatOpenAI(api_key = api_key, model_name = open_ai_model)
handler =  StdOutCallbackHandler()

template = """아래의 내용에 기반하여 질문에 답하여라:
{context}

질문: PTSD와 연관된 정신질환 증상(symptom)을 label(symptom)의 형태로 알려줄 것인데, 다음과 같다.
reex(Reexperience), avoid(Avoidance), ncog(Negative change in cognition), nmood(Negative change in mood), arousal(Arousal), disso(Dissociation), demo(Difficulty in emotional regulation), nself(Negative self-image),
drelat(Difficulty in relationship), depress(Depressed mood), dinter(Decreased interest), dapp(Decreased appetite), iapp(Increased appetite), insom(Insomnia), hsom(Hypersomnia), agit(Psychomotor agitation), retard(Psychomotor retardation),
fati(Fatigue), worth(Worthlessness), guilty(Excessive guilt), dcon(Decreased concentration), dmemo(Decreased memory), ddeci(Decreased decision), suii(Suicidal ideation), suip(Suicide plan), suia(Suicide attempt), anxiety(Anxiety),
palpi(Palpitation), sweat(Sweating), trembl(Trembling), breath(Shortness of breath), chok(Choking), chest(Chest pain), nausea(Nausea), dizzy(Dizziness), chhe(Chilling), pares(Paresthesia), control(Loss of control), dying(Fear of dying),
adepen(Alcohol dependence), atoler(Alcohol tolerance), awithdr(Alcohol withdrawal) 와 같이 총 42개의 증상(symptom)이 있다.
다음 인터뷰 내용을 보고 PTSD와 연관된 정신질환 증상(symptom) 및 이를 나타내는 구획(section)을 추출하라. 인터뷰 내용에서 증상(symptom)을 추출할 때는 반드시 label(symptom) 형태에서 (symptom)을 제외한 label만을 사용해서 대답하고, 인터뷰 내용에서 구획(section)을 추출할 때는 반드시 주어진 인터뷰 내용만을 활용해서 대답해야 한다.
또한 인터뷰 내용에서 구획(section)을 여러 번 추출할 때, 반드시 "...", "...", "..." 의 형태로 대답하라.
만약 주어진 인터뷰에 PTSD와 연관된 정신질환 증상이 없다면 'none'이라고 대답하라.
- 인터뷰 내용 : {question}

답변:
- 증상 : 
- 구획 :
"""
prompt = ChatPromptTemplate.from_template(template)

chain_type_kwargs = {"prompt":prompt}

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    callbacks=[handler],
    return_source_documents=True,
    chain_type_kwargs=chain_type_kwargs
)

def zeroshot_rag(df, output_file):
    
    df['Estimation'] = ''
    ignore = 0
    for idx, row in df.iterrows():
        
        question = row['Statement']
        
        try:
            response = qa_chain({'query':question})
        
            df.loc[idx, 'Estimation'] = response['result']
            
            time.sleep(20)
        
        except Exception as e:
                print(e)
                if ("Limit" in str(e)):
                    time.sleep(10)
                
                else:
                    ignore += 1
                    print('ignored', ignore)
    
    # Save the dataframe to a new excel file
    df.to_excel(f'{gpt_result_filename}.xlsx', index=False)

    
# zero-shot with RAG
data = pd.read_excel(f"{data_filename}.xlsx")
zeroshot_rag(data)

# extract ground-truth symptoms
gpt_result = pd.read_excel(f"{gpt_result_filename}.xlsx")
extract_symp1 = extract_symp_from_df_label(gpt_result, "Ground-truth label", "Symptom")

# extract estimated symptoms
extract_symp2 = extract_symp_from_df_rag(extract_symp1, "Estimation", "Estimated Symptom")

# calcuate metrics used for multi-label classification in estimating symptoms
num_set_extract_symp2 = calculate_num_set(extract_symp2) 
calculate_and_average_metrics(num_set_extract_symp2, rag_metric_symp)

# extract ground-truth sections and estimated sections
extract_sec = extract_sections(gpt_result)

# tokenize the text of ground-truth sections and estimated sections and number tokens of the text
tokenize_numbering(extract_sec, token_num_sec)

# calculate the mid-token of the ground-truth sections and estimated sections
mid_token_calc(token_num_sec, mid_token_calc_sec)

# calculate the recall mid-token distance
mid_token_dist_calc(mid_token_calc_sec, rag_midtoken)
