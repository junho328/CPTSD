import openai
import openpyxl
import pandas as pd
import re
import argparse
import json
import numpy as np
import ast
from itertools import chain
from ast import literal_eval
import os
import time


# zeroshot_symp
def extract_split_and_deduplicate_symptoms(df, source_column, target_column):
    """
    Extracts symptoms from a column containing JSON-like structures, splits comma-separated symptoms,
    deduplicates them, and adds them to a new column.

    :param df: DataFrame containing the data
    :param source_column: Column name from which to extract symptoms
    :param target_column: Column name to store the extracted, split, and deduplicated symptoms
    """
    extracted_symptoms = []

    # Iterate over each row in the dataframe
    for index, row in df.iterrows():
        # Parse the JSON-like string in the source column
        try:
            data = json.loads(row[source_column].replace("'", "\""))
        except json.JSONDecodeError:
            # In case of a decoding error, add a placeholder
            extracted_symptoms.append(["Error in data"])
            continue

        # Extract, split and deduplicate the symptoms
        symptoms = set()
        for item in data:
            if 'symptom' in item:
                for symptom in item['symptom'].split(','):
                    symptoms.add(symptom.strip())

        extracted_symptoms.append(list(symptoms))

    # Add the extracted symptoms to the dataframe in the target column
    df[target_column] = extracted_symptoms


# symp_ground-truth label
def extract_symp_from_df_label(df, source_column, target_column):
    """
    Extracts symptoms from a column containing JSON-like structures, splits comma-separated symptoms,
    deduplicates them, and adds them to a new column.

    :param df: DataFrame containing the data
    :param source_column: Column name from which to extract symptoms
    :param target_column: Column name to store the extracted, split, and deduplicated symptoms
    """
    extracted_symptoms = []

    # Iterate over each row in the dataframe
    for index, row in df.iterrows():
        # Parse the JSON-like string in the source column
        try:
            data = json.loads(row[source_column].replace("'", "\""))
        except json.JSONDecodeError:
            # In case of a decoding error, add a placeholder
            extracted_symptoms.append(["Error in data"])
            continue

        # Extract, split and deduplicate the symptoms
        symptoms = set()
        for item in data:
            if 'symptom' in item:
                for symptom in item['symptom'].split(','):
                    symptoms.add(symptom.strip())

        extracted_symptoms.append(list(symptoms))

    # Add the extracted symptoms to the dataframe in the target column
    df[target_column] = extracted_symptoms


# rag_symp_rag result
def extract_symp_from_df_rag(df, source_column, target_column):
    def extract_symptoms(data_string):
        if "증상 :" in data_string or "- 증상:" in data_string:
            # 증상 부분 추출
            parts = data_string.split("증상 :") if "증상 :" in data_string else data_string.split("- 증상:")
            if len(parts) > 1:
                symptoms_part = parts[1].split("\n")[0].split("-")[0].strip()
            else:
                return ['none']

            if symptoms_part.lower() == 'none':
                return ['none']

            symptoms = [symptom.strip() for symptom in symptoms_part.split(',')]
            return symptoms
        else:
            return ['none']

    extracted_symptoms_list = []

    for index, row in df.iterrows():
        symptoms_data = row[source_column]
        extracted_symptoms_list.append(extract_symptoms(symptoms_data))

    df[target_column] = extracted_symptoms_list


# icl_symp_icl results
def extract_symp_from_df_icl(df, source_column, target_column):
    """
    Extracts symptoms from the first list or non-list dictionary of a column containing JSON-like structures,
    regardless of the quotes used for keys and values. Splits comma-separated symptoms, deduplicates them,
    and adds them to a new column.

    :param df: DataFrame containing the data
    :param source_column: Column name from which to extract symptoms
    :param target_column: Column name to store the extracted, split, and deduplicated symptoms
    """
    extracted_symptoms = []

    # Iterate over each row in the dataframe
    for entry in df[source_column]:
        # Remove "Output: " and "Input: " prefixes if present
        entry = entry.replace('Output: ', '').replace('Input: ', '').strip()

        # Normalize single quotes to double quotes for JSON compatibility
        entry = entry.replace("'", "\"")

        # Handle non-list data formatted as a single dictionary
        if entry.startswith("{\"symptom\":"):
            entry = '[' + entry + ']'

        # Find the first list of symptoms in the entry
        try:
            # Attempt to find the first list or single dictionary directly
            first_list_start = entry.find("[{\"symptom\":")
            if first_list_start != -1:
                # Find the end of the list
                list_end = entry.find("}]", first_list_start) + 2
                data = json.loads(entry[first_list_start:list_end])
            else:
                # If no list or single dictionary is found, set data to an empty list
                data = []
        except json.JSONDecodeError:
            # In case of a decoding error, add a placeholder
            extracted_symptoms.append(["Error in data"])
            continue

        # Extract, split, and deduplicate the symptoms
        symptoms = set()
        for item in data:
            if 'symptom' in item:
                # Remove whitespace before splitting
                symptoms.update(symptom.strip() for symptom in item['symptom'].split(','))

        extracted_symptoms.append(list(symptoms))

    # Add the extracted symptoms to the dataframe in the target column
    df[target_column] = extracted_symptoms


# symp
def calculate_num_set(df1):
    # Combine the four DataFrames into one
    combined_df = df1

    combined_df['num_symptoms'] = 1
    combined_df['num_estimated_symptoms'] = 1
    combined_df['num_union'] = 1
    combined_df['num_intersection'] = 1

    def calculate_metrics(row):
        # The same function as before
        symptoms = eval(row['Symptom'])
        estimated_symptoms = eval(row['Estimated Symptom'])
        intersection = set(symptoms).intersection(set(estimated_symptoms))
        union = set(symptoms).union(set(estimated_symptoms))
        num_intersection = len(intersection)
        num_union = len(union)
        num_symptoms = len(symptoms)
        num_estimated_symptoms = len(estimated_symptoms)
        return num_symptoms, num_estimated_symptoms, num_union, num_intersection

    num_symptoms_list = []
    num_estimated_symptoms_list = []
    num_union_list = []
    num_intersection_list = []

    for i, row in combined_df.iterrows():
        num_symptoms, num_estimated_symptoms, num_union, num_intersection = calculate_metrics(row)

        num_symptoms_list.append(num_symptoms)
        num_estimated_symptoms_list.append(num_estimated_symptoms)
        num_union_list.append(num_union)
        num_intersection_list.append(num_intersection)

    combined_df['num_symptoms'] = num_symptoms_list
    combined_df['num_estimated_symptoms'] = num_estimated_symptoms_list
    combined_df['num_union'] = num_union_list
    combined_df['num_intersection'] = num_intersection_list

    return combined_df


# symp
def calculate_and_average_metrics(input_file, output_file):
    # Combine the four DataFrames into one

    combined_df_count = pd.read_excel(input_file)

    combined_df_count['accuracy'] = 1
    combined_df_count['precision'] = 1
    combined_df_count['recall'] = 1
    combined_df_count['f1_measure'] = 1

    def calculate_metrics(row):
        # The same function as before
        symptoms = eval(row['Symptom'])
        estimated_symptoms = eval(row['Estimated Symptom'])
        num_intersection = int(row['num_intersection'])
        num_union = int(row['num_union'])
        num_symptoms = int(row['num_symptoms'])
        num_estimated_symptoms = int(row['num_estimated_symptoms'])
        accuracy = num_intersection / num_union if num_union else 0
        precision = num_intersection / num_estimated_symptoms if num_symptoms else 0
        recall = num_intersection / num_symptoms if num_estimated_symptoms else 0
        f1_measure = (2 * num_intersection) / (num_symptoms + num_estimated_symptoms) if (num_symptoms + num_estimated_symptoms) else 0
        return accuracy, precision, recall, f1_measure

    accuracy_list = []
    precision_list = []
    recall_list = []
    f1_measure_list = []

    for i, row in combined_df_count.iterrows():
        accuracy, precision, recall, f1_measure = calculate_metrics(row)
        accuracy_list.append(accuracy)
        precision_list.append(precision)
        recall_list.append(recall)
        f1_measure_list.append(f1_measure)

    combined_df_count['accuracy'] = accuracy_list
    combined_df_count['precision'] = precision_list
    combined_df_count['recall'] = recall_list
    combined_df_count['f1_measure'] = f1_measure_list
    
    # Calculate the average of each metric
    avg_accuracy = combined_df_count['accuracy'].mean()
    avg_precision = combined_df_count['precision'].mean()
    avg_recall = combined_df_count['recall'].mean()
    avg_f1_measure = combined_df_count['f1_measure'].mean()

    combined_df_count.to_excel(output_file, index=False)
    return avg_accuracy, avg_precision, avg_recall, avg_f1_measure


# extracting sections
def extract_sections(df):
    """
    Processes the dataframe by removing rows where 'Ground-truth label' contains 'none',
    extracting the 'section' part from both 'Ground-truth label' and 'Estimation' columns, 
    and adding these as new columns 'Section' and 'Estimated Section'.
    """
    # Remove rows where 'Ground-truth label' contains 'none'
    df = df[df['Ground-truth label'].apply(lambda x: 'none' not in x)]

    # Function to extract section values
    def extract_section(column):
        sections = []
        for item in eval(column):
            # Add an empty string if 'section' is 'none', otherwise add the 'section' value
            if item.get('section', '') == 'none':
                sections.append('')
            else:
                sections.append(item.get('section', ''))
        return sections

    # Create new columns for 'Section' and 'Estimated Section'
    df['Section'] = df['Ground-truth label'].apply(extract_section)
    df['Estimated Section'] = df['Estimation'].apply(extract_section)

    return df


def tokenize_numbering(input_file_path, output_file_path):
    """
    Process the given Excel file by tokenizing and assigning token numbers to 'Statement', 
    'Section', and 'Estimated Section' columns, and export the processed data to a new Excel file.

    :param input_file_path: Path to the input Excel file.
    :param output_file_path: Path to the output Excel file.
    """
    import pandas as pd
    import re
    from itertools import chain
    from ast import literal_eval

    def tokenize(text):
        # Tokenize the text into 3-word phrases, ignoring punctuation and sentence boundaries.
        # Replace all punctuation marks with spaces to effectively remove them.
        text = re.sub(r'[.?!]', ' ', text)
        words = text.split()
        tokens = []
        for i in range(len(words) - 2):
            tokens.append(' '.join(words[i:i+3]))
        return tokens

    def tokenize_and_assign_numbers(statement):
        """Tokenize the statement and assign token numbers starting from 0."""
        tokens = tokenize(statement)
        token_number_pairs = [(token, i) for i, token in enumerate(tokens)]
        return token_number_pairs

    def extract_tokens_with_numbers(df_column):
        """Extract all unique tokens with their corresponding numbers from a dataframe column."""
        token_number_dict = {}
        for row in df_column:
            for token, number in row:
                if token not in token_number_dict:
                    token_number_dict[token] = number
        return token_number_dict

    def tokenize_list_column_and_assign_numbers(column, reference_tokens):
        """Tokenize each string in a list within a dataframe column and assign token numbers based on a reference."""
        tokenized_column = []
        max_existing_number = max(reference_tokens.values(), default=-1)

        for item in column:
            item_list = literal_eval(item)
            tokenized_items = []
            for text in item_list:
                tokens = tokenize(text)
                token_number_pairs = []
                for token in tokens:
                    if token in reference_tokens:
                        token_number_pairs.append((token, reference_tokens[token]))
                    else:
                        max_existing_number += 1
                        reference_tokens[token] = max_existing_number
                        token_number_pairs.append((token, max_existing_number))
                tokenized_items.append(token_number_pairs)
            tokenized_column.append(tokenized_items)

        return tokenized_column

    # Load the Excel file
    df = pd.read_excel(input_file_path)

    # Tokenize 'Statement' and assign token numbers
    df['Tokenized Statement with Numbers'] = df['Statement'].apply(tokenize_and_assign_numbers)

    # Extract tokens with numbers from the tokenized Statement column
    statement_tokens_with_numbers = extract_tokens_with_numbers(df['Tokenized Statement with Numbers'])

    # Tokenize 'Section' and 'Estimated Section' and assign token numbers
    df['Tokenized Section with Numbers'] = tokenize_list_column_and_assign_numbers(df['Section'], statement_tokens_with_numbers.copy())
    df['Tokenized Estimated Section with Numbers'] = tokenize_list_column_and_assign_numbers(df['Estimated Section'], statement_tokens_with_numbers.copy())

    # Export to a new Excel file
    df.to_excel(output_file_path, index=False)

    return "Processing and export completed."


def mid_token_calc(input_file_path, output_file_path):
    """
    Process the Excel file to calculate mid-tokens for the specified columns.
    Input and output are both Excel files.

    Args:
    input_file_path (str): Path to the input Excel file.
    output_file_path (str): Path to save the output Excel file.
    """
    def calculate_mid_tokens(column):
        """
        Calculate the mid-token for each list of tokens in the given column.
        This function first converts the string representation of the list of tuples into an actual list of tuples.
        """
        mid_tokens = []
        for token_list_str in column:
            # Convert the string representation to a list of tuples
            token_list = ast.literal_eval(token_list_str)
            mid_tokens_list = []
            for sublist in token_list:
                # Extract the numbers from the sublist
                numbers = [token[1] for token in sublist]
                # Calculate the mid-token
                if numbers:
                    mid_token = (numbers[0] + numbers[-1]) / 2
                    mid_tokens_list.append(mid_token)
            mid_tokens.append(mid_tokens_list)
        return mid_tokens

    # Load the Excel file
    df = pd.read_excel(input_file_path)

    # Calculate mid-tokens for the specified columns
    df['Mid-Token Section'] = calculate_mid_tokens(df['Tokenized Section with Numbers'])
    df['Mid-Token Estimated Section'] = calculate_mid_tokens(df['Tokenized Estimated Section with Numbers'])

    # Save the updated dataframe to a new Excel file
    df.to_excel(output_file_path, index=False)
    

def mid_token_dist_calc(input_file_path, output_file_path):
    """
    Process the Excel file to find the closest values in 'Mid-Token Estimated Section' for each element
    in 'Mid-Token Section', calculate the average difference, and compute the recall mid-token distance.
    Save the results to new columns in the Excel file.

    Args:
    input_file_path (str): Path to the input Excel file.
    output_file_path (str): Path to save the output Excel file.
    """
    import pandas as pd
    import ast

    def find_closest_values(section_column, estimated_column):
        """
        For each value in the section_column list, find the closest value in the estimated_column list.
        """
        closest_values = []
        for section_list, estimated_list in zip(section_column, estimated_column):
            closest_for_section = []
            for section_value in section_list:
                # Calculate the absolute differences between the section value and all estimated values
                differences = [abs(section_value - est_value) for est_value in estimated_list]
                # Find the estimated value with the smallest difference
                closest_value = estimated_list[differences.index(min(differences))] if differences else None
                closest_for_section.append(closest_value)
            closest_values.append(closest_for_section)
        return closest_values

    def find_avg_difference(section_column, closest_estimated_column):
        avg_differences = []
        for section_list, closest_estimated_list in zip(section_column, closest_estimated_column):
            # Check if 'Closest Mid-Token Estimated Section' is an empty list or contains None
            if not closest_estimated_list or all(value is None for value in closest_estimated_list):
                # Skip calculating average difference if the list is empty or all None
                avg_difference = None
            else:
                # Calculate the absolute differences and average them
                differences = [abs(section_value - est_value) for section_value, est_value in zip(section_list, closest_estimated_list) if est_value is not None]
                avg_difference = sum(differences) / len(differences) if differences else None
            avg_differences.append(avg_difference)
        return avg_differences


    def calculate_recall_mid_token_distance(df):
        """
        Calculate the recall mid-token distance using the tokenized statement column.
        """
        def calculate_distance(row):
            tokenized_statement = ast.literal_eval(row['Tokenized Statement with Numbers'])
            closest_estimated_section = row['Closest Mid-Token Estimated Section']

            # Check if 'Closest Mid-Token Estimated Section' is a list containing 'None'
            if None in closest_estimated_section:
                # If the list contains None, set recall_mid_token_distance to 1
                return 1

            # Counting the number of elements (pairs) in the tokenized statement
            token_count = len(tokenized_statement)

            # Handle cases where token count is zero to avoid division by zero
            if token_count == 0:
                return None

            avg_difference = row['Average Difference']
            # Calculate the recall mid-token distance
            recall_mid_token_distance = avg_difference / token_count if avg_difference is not None else None
            return recall_mid_token_distance

        # Apply the calculate_distance function to each row
        df['Recall Mid-Token Distance'] = df.apply(calculate_distance, axis=1)
        return df

    # Load the Excel file
    df = pd.read_excel(input_file_path)

    # Add new columns for the closest mid-token and average differences
    df['Closest Mid-Token Estimated Section'] = find_closest_values(
        df['Mid-Token Section'].apply(ast.literal_eval),
        df['Mid-Token Estimated Section'].apply(ast.literal_eval)
    )
    
    df['Average Difference'] = find_avg_difference(
        df['Mid-Token Section'].apply(ast.literal_eval),
        df['Closest Mid-Token Estimated Section']
    )

    # Calculate and add the recall mid-token distance column
    df = calculate_recall_mid_token_distance(df)

    # Save the updated dataframe to a new Excel file
    df.to_excel(output_file_path, index=False)
