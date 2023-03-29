# General Idea: Take in data from a CSV file filter the data according to some conditions, write the results to another CSV file.
    # Making this object oriented: 
    # a class 'File', is instantiated with every new file that needs to be filtered. We take in a name, then prompt questions to determine columns values etc.

# First iteration: Hard Code the file name, the columns and conditions to filter by and the file name for the output file

# Second iteration, create CLI for interaction with program
import csv
import pandas

class File:
    def __init__(self, name, finalName):
        self.name = name # The file name that we are reading from
        self.final = finalName # What we are going to name the file once we've completed the filter

    def description(self):
        print(f"We are reading from {self.name}, and turning it into {self.final}")

    def readFile(self):
        df = pandas.read_csv(self.name)
        nullDf = df.dropna() # All rows with a Nan value are being dropped
        nullDf.to_csv(self.final, index = False) # create and write a new file with the updated files.


newFile = File('/Users/jacobhein/Documents/MLBData/test.csv', 'newText.csv')
newFile.description()
newFile.readFile()