#pip3 install simpletransformers pandas
#pip3 install transformers==4.26.1


import pandas as pd
from sklearn.model_selection import train_test_split
from simpletransformers.classification import ClassificationModel
from termcolor import colored
import torch
import logging
# from simpletransformers.model import CustomModel
from transformers import AutoModel


logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)



model_youtube = None

def youtube_category_extraction(text):
    try:

        cl_model = get_model()
        predictions_youtube, raw_outputs_youtube = cl_model.predict([text])
        return [list(youtube_categories_json)[predictions_youtube[0]]]

    except Exception as e:
        print(e)
        return ['Others']

def get_model():
    global model_youtube
    if model_youtube is None:
        model_args = args={'reprocess_input_data': True,
                                  'overwrite_output_dir': True,
                                  "use_multiprocessing": False, "use_multiprocessing_for_evaluation": False, "process_count": 1,
                                  'num_train_epochs': 10,
                                  'learning_rate': 3e-5,
                                  'train_batch_size': 4,
                                  'eval_batch_size': 1,
                                  'gradient_accumulation_steps': 1,
                                  'save_steps': 1000,
                                  'fp16': False}
        model_youtube = ClassificationModel('roberta', "outputs", use_cuda=False, args=model_args)
    return model_youtube

model_path = "outputs/model_args.json"

# model_state_dict = torch.load(model_path)
# model = CustomModel("other", "bert", use_cuda=False, args={"num_train_epochs": 1})
# model.load_state_dict(model_state_dict)

model = get_model()

youtube_categories_json = {
    'Feedback' : 0,
    'Functionality' : 1,
    'Personal Experience' : 2,
    'Pricing' : 3,
    'Question' : 4,
    'Suggestion' : 5,
    'Others' : 6
}

# Make predictions on the test set
predictions= youtube_category_extraction('what is the functionality of this video in marketing')

print(colored('===========================================', 'blue'))
print(colored('model predicted', 'blue'))
print(colored('test result : ' + str(predictions), 'blue'))
print(colored('===========================================', 'blue'))
