# Summarization 

## Overview

This folder contains code to run summarization tasks using OpenAI's GPT. <br>

## Usage

### Experience Only

Summarize the estimated traumatic experiences using OpenAI's GPT-4 and measure BERTScore F1 against the true summary.

Meaning of each arguments:<br>
```exp``` Extracted Experience Data file with Excel format <br>
```apikey``` Your openai api key <br>
```gpt4summary``` Filename of GPT4 Summary <br>
```summary``` True Summary file <br>
```
python3 summarization_exp_only.py exp apikey gpt4summary summary
```

### Symptom Only

Summarize the estimated traumatic symptoms using OpenAI's GPT-4 and measure BERTScore F1 against the true summary.

Meaning of each arguments:<br>
```symp``` Extracted Symptom Data file with Excel format <br>
```apikey``` Your openai api key <br>
```gpt4summary``` Filename of GPT4 Summary <br>
```summary``` True Summary file <br>
```
python3 summarization_symp_only.py symp apikey gpt4summary summary
```

### Experience and Symptom Both

Summarize the estimated traumatic experiences and symptoms using OpenAI's GPT-4 and measure BERTScore F1 against the true summary.

Meaning of each arguments:<br>
```exp``` Extracted Expereinece Data file with Excel format <br>
```symp``` Extracted Symptom Data file with Excel format <br>
```apikey``` Your openai api key <br>
```gpt4summary``` Filename of GPT4 Summary <br>
```summary``` True Summary file <br>
```
python3 summarization_exp_symp.py exp symp apikey gpt4summary summary
```
