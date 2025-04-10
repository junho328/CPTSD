## Fine-tuning Procedure

The fine-tuning process consists of the following steps:

1. **Hyperparameter Selection**  
   Use the notebook file `fine-tuning_validation.ipynb` to explore various hyperparameter configurations and identify the optimal setting.

2. **Model Fine-tuning**  
   Once the best hyperparameters are determined, use `fine-tuning_test.ipynb` to train the final fine-tuned model.

3. **Performance Evaluation**  
   Finally, run the shell script `run_ft_pipeline.sh` to evaluate the symptom estimation performance of the fine-tuned model.
