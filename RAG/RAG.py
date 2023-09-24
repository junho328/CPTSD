import pandas as pd
import argparse
import re
import pickle
from langchain.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import CacheBackedEmbeddings
from langchain.vectorstores import FAISS
from langchain.storage import LocalFileStore
from langchain.prompts import ChatPromptTemplate
from langchain.llms.openai import OpenAIChat
from langchain.chains import RetrievalQA
from langchain.callbacks import StdOutCallbackHandler

parser = argparse.ArgumentParser(description="RAG with Langchain command")

parser.add_argument('apikey', help="Your openai api key", required=True)
parser.add_argument('data', help="Excel Data with column [Statement, Symptom, Section]",required=True)
parser.add_argument('document', help='PDF Doucment for RAG',requried=True)
parser.add_argument('output_file', help="Output Excel data name", required=True)

args = parser.parse_args()

# YOUR OWN API KEY
api_key = args.apikey

# Load Excel Data & PDF Document for RAG
data = args.data
document = args.document

df = pd.read_excel(data)

# Langchain
document_loader = PyMuPDFLoader(document)
document = document_loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 50,
    length_function = len
)

documnet_chunks = text_splitter.transform_documents(document)

store = LocalFileStore('./document_cache/')

# create an embedder
#text-embedding-ada
core_embeddings_model = OpenAIEmbeddings(openai_api_key=api_key) 

embedder = CacheBackedEmbeddings.from_bytes_store(
    core_embeddings_model,
    store,
    namespace = core_embeddings_model.model
)
# store embeddings in vector store
vectorstore = FAISS.from_documents(documnet_chunks, embedder)

# instantiate a retriever
retriever = vectorstore.as_retriever()

# OpenAI GPT-4 8k 
llm = OpenAIChat(openai_api_key=api_key,model_name="gpt-4")
handler =  StdOutCallbackHandler()

template = """아래의 내용에 기반하여 질문에 답하여라:
{context}

질문: 정신건강의학적으로 유의미한 증상에는 [각 환자의 증상 목록]가 있다. 다음 상담 내용을 보고 정신건강의학적으로 유의미한 증상이 있다면 해당 증상과 이를 시사하는 구획을 추출하라. 만약 유의미한 증상이 없다면 '해당없음'이라고 대답하라. 
- 상담 내용 : {question}

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

# RAG with Langchain 
def RAG(df):
    
    df['Estimated_Symptom'] = ''
    df['Estimated_Section'] = ''
    
    for idx,row in df.iterrows():
        
        question = row['Statement']
        
        response = qa_chain({'query':question})
        
        with open(f'rag_dsm5_results_p7/result_{idx}.pkl','wb') as f:
            pickle.dump(response,f)
        
        symptom = re.search(r'- 증상 : (.*)', response['result'])
        section = re.search(r'- 구획 : (.*)', response['result'])
        
        documents = [i for i in response['source_documents']]
        
        if symptom == None:
        
            df.at[idx,'Estimated_Symptom'] = '해당없음'
            df.at[idx,'Estimated_Section'] = '해당없음'
            
        if symptom != None:
            
            try:
                df.at[idx,'Estimated_Symptom'] = symptom.group(1).lstrip(': ').strip()
                
            except:
                df.at[idx,'Estimated_Symptom'] = '해당없음'
            
            try:
                df.at[idx,'Estimated_Section'] = section.group(1).lstrip(': ').strip()
            
            except:
                df.at[idx,'Estimated_section'] = '해당없음'
            
    return df
        
result = RAG(df)
file_name = args.output_file
result.to_excel(f"{file_name}.xslx",index=False)