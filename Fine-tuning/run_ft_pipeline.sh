#!/bin/bash

python3 symp_gpt3.5_ft.py --p P3
python3 symp_gpt3.5_ft.py --p P7
python3 symp_gpt3.5_ft.py --p P9
python3 symp_gpt3.5_ft.py --p P13

python3 get_metric.py --model_name ur_model
