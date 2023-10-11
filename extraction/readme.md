# Extracting Symptom and Section

## Overview

This folder contains code to run extraction tasks using OpenAI's GPT-4 with various methods Zero-Shot(zeroshot.py), In-Context Learning(icl.py), Chain-of-Thought(cot.py).

## Usage

### Zero-Shot

Meaning of each arguments:<br>
```data``` Data File After Label Extraction with Excel Format <br>
```apikey``` Your openai api key <br>
```result``` Filename of result data <br>
```
python3 zeroshot.py data apikey result
```

### In-Context Learning

Meaning of each arguments:<br>
```data``` Data File After Label Extraction with Excel Format <br>
```examplar``` Examplar File for In-Context Learning with Excel Format <br>
```apikey``` Your openai api key <br>
```result``` Filename of result data <br>
```
python3 icl.py data apikey examplar result
```

### Chain-of-Thought

Meaning of each arguments:<br>
```data``` ata File After Label Extraction with Excel Format <br>
```definition``` Symptom Definition File with Excel Forma <br>
```apikey``` Your openai api key <br>
```result``` Filename of result data <br>
```
python3 cot.py data definition apikey result
```

## Remind

The calculation of estimated section accuracy using mid-token distance, as presented in the paper, is not accompanied by specific code due to duplicate interview paragraphs and exceptional cases. <br> 
Please refer to the paper for the method of detailed procedure to calculate mid-token distance.
