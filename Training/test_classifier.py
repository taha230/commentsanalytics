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


model_path = "outputs/model_args.json"

# model_state_dict = torch.load(model_path)
# model = CustomModel("other", "bert", use_cuda=False, args={"num_train_epochs": 1})
# model.load_state_dict(model_state_dict)

model = ClassificationModel(
        "roberta", "outputs", use_cuda=False
    )


# Make predictions on the test set
predictions, raw_outputs = model.predict(['what is the functionality of this video in marketing'])

print(colored('===========================================', 'blue'))
print(colored('model predicted', 'blue'))
print(colored('test result : ' + str(predictions), 'blue'))
print(colored('===========================================', 'blue'))
