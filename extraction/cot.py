import openai
import openpyxl
import pandas as pd
import argparse
from prompts_cot import cot_short_en_1

parser = argparse.ArgumentParser(
    description="Extract Symptom and Section with Chain-of-Thought method"
)
parser.add_argument(
    "--data", help="Data File After Label Extraction with Excel Format", required=True
)
parser.add_argument(
    "--definition", help="Symptom Definition File with Excel Format", required=True
)
parser.add_argument("--apikey", help="Your openai api key", required=True)
parser.add_argument("--result", help="Filename of result data", required=True)

args = parser.parse_args()
data_filename = args.data
symptom_definition_file = args.definition
api_key = args.apikey
result_filename = args.result


def add_CoT_explanation(cot_df, symptom_definition_df):

    # Add 'CoT explanation' column
    cot_df["CoT explanation"] = ""

    for index, row in cot_df.iterrows():
        symptom = row["Symptom"]
        section = row["Section"]

        definition = symptom_definition_df[symptom_definition_df["symptom"] == symptom][
            "definition"
        ].values
        if len(definition) > 0:
            definition = definition[0]

            cot_df.at[index, "CoT explanation"] = (
                f"{{ {symptom} }} is defined as {{ {definition} }}and, accordingly {{ {section} }} In the section, {{ {symptom} }} appears to be symptomatic."
            )

    return cot_df


def create_CoT_prompt(df):

    prompts = []

    for _, row in df.iterrows():
        statement = row["Statement"]
        CoT_expl = row["CoT explanation"]

        prompt = f"Input: {statement}\nOutput: {CoT_expl}"
        prompts.append(prompt)

    # Joining all the prompts together
    full_prompt = "\n\n".join(prompts)

    return full_prompt


def cot(df1, df2):

    # Initialize the columns for estimated symptom and section
    df2["GPT-4 Output"] = ""

    openai.api_key = api_key
    model = "gpt-4"

    for idx, statement in enumerate(df2["Statement"]):

        # Construct the full prompt
        full_prompt_CoT3 = create_CoT_prompt(df1)
        full_prompt_CoT3 += f"\n\n Input Query: {statement}"

        messages = cot_short_en_1
        messages[-1]["content"] += full_prompt_CoT3

        response = openai.ChatCompletion.create(model=model, messages=messages)

        answer = response["choices"][0]["message"]["content"]
        df2["GPT-4 Output"].iloc[idx] = answer

    df2.to_excel(f"{result_filename}.xlsx", index=False)


data = pd.read_excel(f"{data_filename}.xlsx")
symptom_definition = pd.read_excel(f"{symptom_definition_file}.xlsx")
cot_data = add_CoT_explanation(data, symptom_definition)
cot(cot_data, data)
