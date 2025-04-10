#!/bin/bash

python3 symp_gpt3.5_ft.py --p P1
python3 symp_gpt3.5_ft.py --p P2
python3 symp_gpt3.5_ft.py --p P3
python3 symp_gpt3.5_ft.py --p P4

python3 get_metric.py --model_name ur_model
