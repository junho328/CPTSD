import openai
import openpyxl
import pandas as pd
import argparse
from prompts_icl import icl_short_en_1

parser = argparse.ArgumentParser(
    description="Extract Symptom and Section with In-Context Learning method"
)
parser.add_argument(
    "--data", help="Data File After Label Extraction with Excel Format", required=True
)
parser.add_argument(
    "--examplar",
    help="Examplar File for In-Context Learning with Excel Format",
    required=True,
)
parser.add_argument("--apikey", help="Your openai api key", required=True)
parser.add_argument("--result", help="Filename of result data", required=True)

args = parser.parse_args()
data_filename = args.data
examplar_file = args.examplar
api_key = args.apikey
result_filename = args.result


def create_icl_prompt(df):

    prompts = []

    for _, row in df.iterrows():
        statement = row["Statement"]
        section = row["Section"]
        symptom = row["Symptom"]

        prompt = (
            f"Input: {statement}\nOutput: - Symptoms : {symptom} - Sections : {section}"
        )
        prompts.append(prompt)

    # Joining all the prompts together
    full_prompt = "\n\n".join(prompts)

    return full_prompt


def icl(df1, df2):

    # Add 'GPT-4 Output' Column
    df2["GPT-4 Output"] = ""

    openai.api_key = api_key

    model = "gpt-4"

    # Using enumerate to get an index (idx) and a value (statement) together
    for idx, statement in enumerate(df2["Statement"]):

        # Construct the full prompt
        full_prompt = create_icl_prompt(df1)
        full_prompt += f"\n\n Input Query: {statement}"

        # Set up messages
        messages = icl_short_en_1
        messages[-1]["content"] += full_prompt

        response = openai.ChatCompletion.create(model=model, messages=messages)

        answer = response["choices"][0]["message"]["content"]
        df2["GPT-4 Output"].iloc[idx] = answer

    df2.to_excel(f"{result_filename}.xlsx", index=False)


data = pd.read_excel(f"{data_filename}.xlsx")
examplar = pd.read_excel(f"{examplar_file}.xlsx")
icl(examplar, data)
