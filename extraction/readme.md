# Extracting Symptom and Section

## Overview

This folder contains code to run extraction tasks using OpenAI's GPT-4 with various methods Zero-Shot(zeroshot.py), In-Context Learning(icl.py), Chain-of-Thought(cot.py).

## Usage

### Zero-Shot

Extract traumatic symptom and section from patient interview transcripts without further training

Meaning of each arguments:<br>
```data``` Data File After Label Extraction with Excel Format <br>
```apikey``` Your openai api key <br>
```result``` Filename of result data <br>
```
python3 zeroshot.py --data=data --apikey=apikey --result=result
```

### In-Context Learning

Extract traumatic symptom and section from patient interview transcripts with Few-shot In-Context Learning method.
Please refer to *[the respective paper](https://arxiv.org/abs/2301.00234)* for detailed information on In-Context Learning method.

Meaning of each arguments:<br>
```data``` Data File After Label Extraction with Excel Format <br>
```examplar``` Examplar File for In-Context Learning with Excel Format <br>
```apikey``` Your openai api key <br>
```result``` Filename of result data <br>
```
python3 icl.py --data=data --apikey=apikey --examplar=examplar --result=result
```

### Chain-of-Thought

Extract traumatic symptom and section from patient interview transcripts with Chain-of-Thought method.
Please refer to *[the respective paper](https://arxiv.org/abs/2201.11903)* for detailed information on Chain-of-Thought method.

Meaning of each arguments:<br>
```data``` ata File After Label Extraction with Excel Format <br>
```definition``` Symptom Definition File with Excel Forma <br>
```apikey``` Your openai api key <br>
```result``` Filename of result data <br>
```
python3 cot.py --data=data --definition=definition --apikey=apikey --result=result
```
