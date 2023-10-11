# Extracting Symptom and Section

## Overview

This folder contains code to run summarization tasks using OpenAI's GPT. <br>

## Usage

### Experience Only

Meaning of each arguments:<br>
```exp``` Extracted Experience Data file with Excel format <br>
```apikey``` Your openai api key <br>
```gpt4summary``` Filename of GPT4 Summary <br>
```summary``` True Summary file <br>
```
python3 summarization_exp_only.py exp apikey gpt4summary summary
```

### Symptom Only

Meaning of each arguments:<br>
```symp``` Extracted Symptom Data file with Excel format <br>
```apikey``` Your openai api key <br>
```gpt4summary``` Filename of GPT4 Summary <br>
```summary``` True Summary file <br>
```
python3 summarization_symp_only.py symp apikey gpt4summary summary
```

### Experience and Symptom Both

Meaning of each arguments:<br>
```exp``` Extracted Expereinece Data file with Excel format <br>
```symp``` Extracted Symptom Data file with Excel format <br>
```apikey``` Your openai api key <br>
```gpt4summary``` Filename of GPT4 Summary <br>
```summary``` True Summary file <br>
```
python3 summarization_exp_symp.py exp symp apikey gpt4summary summary
```
