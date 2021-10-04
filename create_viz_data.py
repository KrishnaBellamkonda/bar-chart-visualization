# This allows you to create a data file for your visualization 
import argparse 
import os 
import json
import numpy as np

from config import DATA_SAVE_PATH 


class VisualizationDataCreator():
    def __init__(self):
        pass

    def get_args(self):

        # Init Arg Parser
        arg_parser = argparse.ArgumentParser(description="This program allows you to create your own data json file from command line")

        # Adding Args
        arg_parser.add_argument('o', type=str, help="the name of the output file")
        arg_parser.add_argument('-d', action='append', nargs='+', type=int, help='the datapoints that you want to enter')
        arg_parser.add_argument('-l',action='append', nargs='+',  type=str, help='these are labels of the data')
        arg_parser.add_argument('-hindex',action='append', nargs='+',  type=int, help='these are the highlighted indices')
        arg_parser.add_argument('--desc', type=str, help="contains the description of the data - optional flag")


        # Parsing the input 
        args = arg_parser.parse_args()

        # Adding arguments
        self.data = args.d
        self.labels = args.l
        self.outputname = args.o
        self.desc = args.desc
        self.highlighted = args.hindex

    def make_data_file(self):
        # Make a dictionary 
        viz_data = {}

        # Flatening the data 
        data_array = np.squeeze(self.data).tolist()
        self.data = data_array

        # Flatening the labels 
        labels_array = self.labels[0]
        self.labels = labels_array

        # Flattening hindex
        if self.highlighted:
            hindex_array = self.highlighted[0]
            self.highlighted = hindex_array

        # Adding data 
        viz_data["data"] = self.data
        viz_data["labels"] = self.labels
        viz_data["highlight_index"] = self.highlighted

        # Dumping the JSON file 
        name, extension = os.path.splitext(self.outputname)
        if extension != ".json": self.outputname = name + ".json"
        output_path = os.path.join(DATA_SAVE_PATH, self.outputname)
        with open(output_path, "w") as fp:
            json.dump(viz_data, fp)
            print(f"Created a file here - {output_path}")


if __name__ == '__main__':
    viz_data_creator = VisualizationDataCreator()
    viz_data_creator.get_args()
    viz_data_creator.make_data_file()