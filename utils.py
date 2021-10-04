from os import error
import json
import pandas as pd
import numpy as np
import os
from config import *

# Constants 

# Detect Extension and 
def read_json_data(file_path=TEST_PATH, data_name="Data"):
    
    # Read the JSON file 
    with open(file_path, "r") as fp:
        obj = json.load(fp)
    
    # Read the object for data and labels 
    data = np.array(obj["data"], dtype=np.int64)
    labels = np.array(obj["labels"], dtype=str)

    # Creating a pandas dataframe 
    df = pd.DataFrame(np.c_[data,labels], columns=[data_name, "labels"])
    df[data_name] = df[data_name].astype(np.int64)
    df["labels"] = df["labels"].astype(str)

    # Highlight Index 
    if obj["highlight_index"]: highlight_index = obj["highlight_index"]
    else: None

    return [df, highlight_index]
