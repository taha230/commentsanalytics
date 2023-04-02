#pip3 install simpletransformers pandas
#pip3 install transformers==4.26.1


import pandas as pd
from sklearn.model_selection import train_test_split
from simpletransformers.classification import ClassificationModel,  ClassificationArgs
from termcolor import colored
import torch
import logging
import faulthandler

faulthandler.enable()


logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)



# Load data into Pandas DataFrame

usecols = ["text"]
feedback_df = pd.read_csv("Feedback.csv", index_col="index")
functionality_df = pd.read_csv("Functionality.csv", index_col="index")
personal_exp_df = pd.read_csv("Personal Experience.csv", index_col="index")
pricing_df = pd.read_csv("Pricing.csv", index_col="index")
question_df = pd.read_csv("Question.csv", index_col="index")
suggestion_df = pd.read_csv("Suggestion.csv", index_col="index")
others_df = pd.read_csv("Others.csv", index_col="index")

# Add labels to each DataFrame
feedback_df["label"] = 0
functionality_df["label"] = 1
personal_exp_df["label"] = 2
pricing_df["label"] = 3
question_df["label"] = 4
suggestion_df["label"] = 5
others_df["label"] = 6

# print(feedback_df.head())


# Concatenate all DataFrames into one
data_df = pd.concat([feedback_df, functionality_df, personal_exp_df,
                     pricing_df, question_df, suggestion_df, others_df], axis=0, ignore_index=True)


print(colored(data_df.head(), 'green'))

# Split Train, Test, Eval
train_df, test_df = train_test_split(data_df, test_size=0.1, random_state=42)
train_df, eval_df = train_test_split(train_df, test_size=0.1, random_state=42)

print(colored('split data to train, test, eval', 'blue'))


print(colored(train_df.head(), 'cyan'))
print(colored(eval_df.head(), 'magenta'))
print(colored(test_df.head(), 'yellow'))


cuda_available = torch.cuda.is_available()
print(colored('cuda_available : ' + str(cuda_available), 'cyan'))

# Initialize the RoBERTa-based classification model

# Optional model configuration

model = ClassificationModel("roberta", "roberta-base",
                            use_cuda=cuda_available, cuda_device=0,
                            num_labels=len(data_df.label.unique()),
                            args={'reprocess_input_data': True,
                                  'overwrite_output_dir': True,
                                  'use_multiprocessing': False,
                                #   'use_multiprocessing': False, 'use_multiprocessing_for_evaluation': False, 'process_count': 1,
                                  'num_train_epochs': 10,
                                  'learning_rate': 3e-5,
                                  'train_batch_size': 4,
                                  'eval_batch_size': 1,
                                  'gradient_accumulation_steps': 1,
                                  'save_steps': 1000,
                                  'fp16': False})

print(colored('===========================================', 'blue'))
print(colored('model created', 'blue'))
print(colored('===========================================', 'blue'))

# Train the model
model.train_model(train_df, show_running_loss = True)

print(colored('===========================================', 'blue'))
print(colored('model trained', 'blue'))
print(colored('===========================================', 'blue'))

# Evaluate the model on the validation set
# result, model_outputs, wrong_predictions = model.eval_model(eval_df)

# print(colored('===========================================', 'blue'))
# print(colored('model evaluated', 'blue'))
# print(colored('evaluation result : ' + str(result), 'blue'))
# print(colored('===========================================', 'blue'))

# Make predictions on the test set
predictions, raw_outputs = model.predict(['what is the functionality of this video in marketing'])

# print(colored('===========================================', 'blue'))
# print(colored('model predicted', 'blue'))
# print(colored('test result : ' + str(predictions), 'blue'))
# print(colored('===========================================', 'blue'))
