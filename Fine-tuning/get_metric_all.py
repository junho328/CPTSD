import argparse
import json
import pandas as pd


parser = argparse.ArgumentParser(description='estimation to xlsx for ft')    


parser.add_argument('--xlsx', help='excel file path')   
parser.add_argument('--p', help='patient name')
parser.add_argument('--model_name', help='model name')

args = parser.parse_args()  


# input: gpt로부터 얻은 test data df 2개
 
def calculate_and_average_metrics(df1,k):
    # Combine the four DataFrames into one
    df = df1
    
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
        
    extract_split_and_deduplicate_symptoms(df, "Ground-truth label", "Symptom")
    extract_split_and_deduplicate_symptoms(df, "Estimation", "Estimated Symptom")
    
    df.to_excel(f'symp_estimation_score_simulated_{k}/symp_extract_{args.model_name}_{args.p}.xlsx', index=False)

    combined_df = pd.read_excel(f'symp_estimation_score_simulated_{k}/symp_extract_{args.model_name}_{args.p}.xlsx')

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
        accuracy = num_intersection / num_union if num_union else 0
        precision = num_intersection / num_symptoms if num_symptoms else 0
        recall = num_intersection / num_estimated_symptoms if num_estimated_symptoms else 0
        f1_measure = (2 * num_intersection) / (num_symptoms + num_estimated_symptoms) if (num_symptoms + num_estimated_symptoms) else 0
        return num_symptoms, num_estimated_symptoms, num_union, num_intersection, accuracy, precision, recall, f1_measure

   
    num_symptoms_list = []
    num_estimated_symptoms_list = []
    num_union_list = []
    num_intersection_list = []


   
    for i, row in combined_df.iterrows():
        num_symptoms, num_estimated_symptoms, num_union, num_intersection, accuracy, precision, recall, f1_measure = calculate_metrics(row)

        
        num_symptoms_list.append(num_symptoms)
        num_estimated_symptoms_list.append(num_estimated_symptoms)
        num_union_list.append(num_union)
        num_intersection_list.append(num_intersection)


   
    combined_df['num_symptoms'] = num_symptoms_list
    combined_df['num_estimated_symptoms'] = num_estimated_symptoms_list
    combined_df['num_union'] = num_union_list
    combined_df['num_intersection'] = num_intersection_list


    combined_df.to_excel(f'symp_estimation_score_simulated_{k}/count_symp_extract_gpt3.5_ft_{args.model_name}_{args.p}.xlsx', index=False)
    return True


def calculate_and_average_metrics_final(xlsx: str, k: int):
    # Combine the four DataFrames into one

    combined_df_count = pd.read_excel(xlsx)

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
        precision = num_intersection / num_symptoms if num_symptoms else 0
        recall = num_intersection / num_estimated_symptoms if num_estimated_symptoms else 0
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
    
    
    avg_accuracy = combined_df_count['accuracy'].mean()
    avg_precision = combined_df_count['precision'].mean()
    avg_recall = combined_df_count['recall'].mean()
    avg_f1_measure = combined_df_count['f1_measure'].mean()

    combined_df_count.to_excel(f'symp_estimation_score_simulated_{k}/final_score_symp_extract_gpt3.5_ft_{args.model_name}_{args.p}.xlsx', index=False)
    return avg_accuracy, avg_precision, avg_recall, avg_f1_measure




df1 = pd.read_excel(f"./result_symp_estimation/symp_gpt3.5_{args.model_name}_{args.p}.xlsx")
calculate_and_average_metrics(df1,1)

df2 = pd.read_excel(f"./result_symp_estimation_2/symp_gpt3.5_{args.model_name}_{args.p}.xlsx")
calculate_and_average_metrics(df2,2)

df3 = pd.read_excel(f"./result_symp_estimation_3/symp_gpt3.5_{args.model_name}_{args.p}.xlsx")
calculate_and_average_metrics(df3,3)



xlsx1 = f'symp_estimation_score_simulated_1/count_symp_extract_gpt3.5_ft_{args.model_name}_{args.p}.xlsx'
avg_accuracy, avg_precision, avg_recall, avg_f1_measure = calculate_and_average_metrics_final(xlsx1, 1)
print("SAMPLE 1")
print(args.model_name, "\n")
print("Acc:", avg_accuracy, "\n", "Precision:", avg_precision,"\n","Recall:", avg_recall,"\n","F1:", avg_f1_measure)
print("------"*6)


xlsx2 = f'symp_estimation_score_simulated_2/count_symp_extract_gpt3.5_ft_{args.model_name}_{args.p}.xlsx'
avg_accuracy, avg_precision, avg_recall, avg_f1_measure = calculate_and_average_metrics_final(xlsx2, 2)
print("SAMPLE 2")
print(args.model_name, "\n")
print("Acc:", avg_accuracy, "\n", "Precision:", avg_precision,"\n","Recall:", avg_recall,"\n","F1:", avg_f1_measure)
print("------"*6)

xlsx3 = f'symp_estimation_score_simulated_3/count_symp_extract_gpt3.5_ft_{args.model_name}_{args.p}.xlsx'
avg_accuracy, avg_precision, avg_recall, avg_f1_measure = calculate_and_average_metrics_final(xlsx3, 3)
print("SAMPLE 3")
print(args.model_name, "\n")
print("Acc:", avg_accuracy, "\n", "Precision:", avg_precision,"\n","Recall:", avg_recall,"\n","F1:", avg_f1_measure)


######################
#Final Fine-tuned Model
#epoch 5 lr default
#model : ur_model
#python3 get_metric_all.py --model_name ur_model --p ur_p