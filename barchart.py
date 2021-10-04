# Imports 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib as mpl
import json 

import os
import sys
import argparse 

from utils import read_json_data
from config import *


# Bar Chart Settings

# BarChart class 
class BarChart():

    def __init__(self):
        self.arg_parser = argparse.ArgumentParser(description="Build a Bar Chart Visualization")
        pass

    def get_args(self):
        # Add the arguments
        parser = self.arg_parser
        parser.add_argument('datapath', metavar='datapath', type=str, help='path to data file')
        parser.add_argument('--cmap', metavar='cmap', type=str, help='the color map to use while creating visualizations')
        parser.add_argument('--colorpath', metavar='color-scheme', type=str, help='the cmap(value) that should be used')
        parser.add_argument('-o', metavar='output', type=str, help='the name of the output file')
        parser.add_argument('--dataname', type=str, metavar='dataname', help='the name of the data')
        parser.add_argument('--title', type=str, metavar='title', help='title of the vizualization')
        parser.add_argument('--horizontal', action="store_true", help="this produces a horizontal bar chart")
        parser.add_argument('--xgrid', action="store_true", help="stores x-grid option")
        parser.add_argument('--ygrid', action="store_true", help="stores xy-grid option")
        parser.add_argument('--fontsize', type=str, metavar='fontsize', help='font size of all the labels and titles')
        parser.add_argument('--xlabel', type=str, metavar="xlabel", help="the label appearing on the xaxis")
        parser.add_argument('--ylabel', type=str, metavar="ylabel", help="the label appearing on the xaxis")
        parser.add_argument('--xfigsize', type=int, metavar="horizontal figure size")
        parser.add_argument('--yfigsize', type=int, metavar="vertical figure size")
        parser.add_argument('--highlight', action="store_true", help="uses basic colorscheme - if you want a customized scheme, use the colorpath method to target the required file")
        parser.add_argument('--alpha', type=float, metavar='alpha transperance', help='the alpha value of colors')
        parser.add_argument('--xticksrot', type=int, metavar="xticks-rotation", help="rotation of xticks")
        parser.add_argument('--yticksrot', type=int, metavar="yticks-rotation", help="rotation of yticks")


        # Parse arguments
        args = self.arg_parser.parse_args()


        # Setting Options
        self.datapath = args.datapath
        self.cmap = args.cmap or CMAP
        self.colorpath = args.colorpath or COLORSCHEME_PATH
        if args.o: self.o = args.o
        else: self.o = input("Enter the output path: ")

        # Read until a valid Path is defined
        path_exists = os.path.exists(self.datapath)

        while not path_exists:
            print()
            print("You've entered an incorrect path")
            self.datapath = input("Enter a valid Path: ") 
            path_exists = os.path.exists(self.datapath)
            print()
        
        # Set Title and Dataname
        self.dataname = args.dataname or DATANAME
        self.title = args.title or TITLE
        
        # Set Horizontal setting 
        if args.horizontal: self.horizontal = HORIZONTAL
        else: self.horizontal = VERTICAL

        # Grid options 
        if (args.xgrid and args.ygrid): self.grid = "both"
        elif (args.xgrid): self.grid = "x"
        elif (args.ygrid): self.grid = "y"
        else:self.grid = None

        # Font size 
        self.fontsize= args.fontsize or FONTSIZE

        # X and Y Axis labels
        self.xlabel = args.xlabel or XLABEL
        self.ylabel = args.ylabel or YLABEL

        # Figure Size 
        if args.xfigsize and args.yfigsize: self.figsize = (args.xfigsize, args.yfigsize)
        elif args.xfigsize: self.figsize = (args.xfigsize, YFIGSIZE)
        elif args.yfigsize: self.figsize = (XFIGSIZE, args.yfigsize)
        else: self.figsize = (XFIGSIZE, YFIGSIZE)

        # Highlight 
        self.highlight = args.highlight

        # Alpha 
        self.alpha = args.alpha or ALPHA

        # Rotation 
        self.xticksrot = args.xticksrot or XTICKSROT
        self.yticksrot = args.yticksrot or YTICKSROT

    def get_df(self, path):
        # Detecting the extension
        filename, extension = os.path.split(path)

        # Importing the data into pandas
        if extension == ".csv":
            df = pd.read_csv(path)
        elif extension == ".xlsx":
            df = pd.read_excel(path)
        else:
            [df, highlight_index] = read_json_data(path)
        
        

        return [df, filename, extension, highlight_index]

    def get_colorscheme(self, path):
        # Opening the color scheme
        with open(path, "r") as fp:
            obj = json.load(fp)
        
        # Highlight color value 
        highlight_color_value = obj["highlight"]
        other_color_value = obj["other"]

        return [highlight_color_value, other_color_value]

    def make_bar_chart(self):
        
        # Get the DataFrame 
        df, filename, extension, highlight_index = self.get_df(self.datapath)
        labels = df["labels"].tolist()        

        # Highlight 
        if self.highlight:
            # Data Length
            datalength = len(df[self.dataname])

            # Get Highlight and other color
            highlight_val, other_val = self.get_colorscheme(self.colorpath)
            cmap = mpl.cm.get_cmap(self.cmap)
            highlight_color, other_color = cmap(highlight_val), cmap(other_val)

            # Create Colors array
            colors = [list(other_color) for x in range(datalength)]
            colors = np.array(colors)

            # Highlighting the required one
            colors[highlight_index] = list(highlight_color) # Highlighted
            self.colors = np.array(colors) 

        else: 
            self.colors = None


        # Make Visualization 
        if self.highlight:

            ax = df.plot(kind=self.horizontal, y=self.dataname, color=colors, sort_columns=True, 
                    fontsize=self.fontsize, figsize=self.figsize, alpha=self.alpha)

            

        else: 
            ax = df.plot(kind=self.horizontal, y=self.dataname, cmap=self.cmap , sort_columns=True, 
                    fontsize=self.fontsize, figsize=self.figsize, alpha=self.alpha)
            
        # Labels
        if self.xlabel: ax.set_xlabel(self.xlabel)
        if self.ylabel: ax.set_ylabel(self.ylabel)

        # XTick Labels 
        if self.horizontal == HORIZONTAL: ax.set_yticklabels(labels, rotation=self.yticksrot)
        else: ax.set_xticklabels(labels, rotation=self.xticksrot)

        # Grid Setting 
        if self.grid: ax.grid(axis = self.grid)

        # Title 
        ax.set_title(self.title)
        
        # PLT save fig
        plt.savefig(self.o)

        plt.show()




# Creating the class
if __name__ == '__main__':
    print("Making your visualization ...")
    barchart = BarChart()
    barchart.get_args()
    barchart.make_bar_chart()