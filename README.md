# Aligning Large Language Models for Enhancing Psychiatric Interviews through Symptom Delineation and Summarization

Jae-hee So, Joonhwan Chang, Eunji Kim, Junho Na, JiYeon Choi, Jy-yong Sohn, Byung-Hoon Kim, Sang Hui Chu

This repository is the code implementation of paper *[Aligning Large Language Models for Enhancing Psychiatric Interviews through Symptom Delineation and Summarization]()* 

## Abstract

Recent advancements in Large Language Models (LLMs) have accelerated their usage in various domains. Given the fact that psychiatric interviews are goal-oriented and structured dialogues between the professional interviewer and the interviewee, it is one of the most underexplored areas where LLMs can contribute substantial value. Here, we explore the use of LLMs for enhancing psychiatric interviews, by analyzing counseling data from North Korean defectors with traumatic events and mental health issues. Specifically, we investigate whether LLMs can (1) delineate the part of the conversation that suggests psychiatric symptoms and name the symptoms, and (2) summarize stressors and symptoms, based on the interview dialogue transcript. Here, the transcript data was labeled by mental health experts for training and evaluation of LLMs. 
Our experimental results show that appropriately prompted LLMs can achieve high performance on both the symptom delineation task and the summarization task. This research contributes to the nascent field of applying LLMs to psychiatric interview and demonstrates their potential effectiveness in aiding mental health practitioners.

<p align="center">
  <img src="imgs/Extraction.png">
  <b>Procedure for Extracting traumatic expereiences of patient interview transcriptions</b>
<br><br>
  <img src="imgs/Summarization.png">
  <b>Procedure for Summary using the traumatic experiences and symptoms</b>
<br><br>
  <img src="imgs/ROC.png">
  <b>ROC curve of GPT-4 zero-shot symptom prediction</b>
</p>

## Setting up an environment

We recommend that you run experiments in a virtual environment where you have installed all the necessary packages.
You may install the requirements using the requirements.txt file:
```
pip install -r requirements.txt
```
Please read the detailed manuals in each subfolder

## Data Format

We saved our initial training data in Excel file(.xlsx). The initial data consisted of 'Statement,' 'Symptom,' and 'Section.'<br>
```Statement``` One segment from the interview with the patient <br>
```Symptom```  Psychiatric symptoms related to PTSD labeled by mental health specialists. symptoms <br>
```Section```  Section with symptoms labeled by mental health specialists <br>
The table below is an example of that. Please use this example to create the data structure for conducting experiments in code.

| Statement | Symptom | Section |
| --------- | --------- | --------- |
| I:... Q:...  | re-experience  | ...coming out in my dreams... |

## Remind

### Estimated Section Accuracy

The calculation of estimated section accuracy using mid-token distance, as presented in the paper, is not accompanied by specific code due to duplicate interview paragraphs and exceptional cases. <br> 
Please refer to the paper for the method of detailed procedure to calculate mid-token distance.

### Fine-tuning

As mentioned in the paper, we fine-tuned GPT-3.5 to compare the performance of zero-shot and fine-tuned one. The data for fine-tuning was created using the 'merge_json' function from 'summarization/json_utils.py,' and the fine-tuning process was conducted with reference to *[OpenAI's Fine-tuning documentation](https://platform.openai.com/docs/guides/fine-tuning)*
