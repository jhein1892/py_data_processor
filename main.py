# General Idea: Take in data from a CSV file filter the data according to some conditions, write the results to another CSV file.
    # Making this object oriented: 
    # a class 'File', is instantiated with every new file that needs to be filtered. We take in a name, then prompt questions to determine columns values etc.

# First iteration: Hard Code the file name, the columns and conditions to filter by and the file name for the output file

# Second iteration, create CLI for interaction with program
import csv
import pandas
import click
import curses


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



add = True
baseDirectory = ''
options = ["1", "2", "3", "4"]

def select_options():
    selected_options = []
    index = 0
    
    # Initialize the curses library
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    
    # Print the initial list of options
    for i, option in enumerate(options):
        if i == index:
            stdscr.addstr(f"> {option}\n")
        else:
            stdscr.addstr(f"  {option}\n")
    
    # Wait for user input
    while len(selected_options) < 3:
        key = stdscr.getch()
        
        # Move the selected option up or down
        if key == curses.KEY_UP:
            index = (index - 1) % len(options)
        elif key == curses.KEY_DOWN:
            index = (index + 1) % len(options)
        elif key == curses.KEY_ENTER or key == 10 or key == 13:
            selected_options.append(options[index])
        
        # Print the updated list of options
        stdscr.clear()
        for i, option in enumerate(options):
            if i == index:
                stdscr.addstr(f"> {option}\n")
            else:
                stdscr.addstr(f"  {option}\n")
    
    # Clean up the curses library
    curses.nocbreak()
    stdscr.keypad(False)
    curses.echo()
    curses.endwin()
    
    return selected_options

# Call the select_options function and print the selected options
selected = select_options()
print(f"Selected options: {selected}")


# while add is True:





#     # print(baseDirectory)
#     # if len(baseDirectory) < 1:
#     #     baseDirectory = input("What is the absolute path to the base directory for your data files? ")
#     # else:
#     #     newDirectory = input(f"Is this file also found in: {baseDirectory}? (y/n) ")
#     #     if newDirectory != 'y':
#     #         baseDirectory = input("What is the absolute path to the base directory for your data files? ")

#     # name = input("What is the name of file you'd like to filter? ")
#     # finalName = input("What would you like to name the file containing the filtered data? ")
#     # fileName = baseDirectory + '/' + name

#     # newFile = File(fileName, finalName)
#     # newFile.description()
#     # # newFile.readFile()
#     # userContinue = input("Would you like to filter another file? (y/n) ")
#     # if userContinue !='y':
#     #     add = False


# print("Thank you for using our data processor!")





    
# /Users/jacobhein/Documents/MLBData/test.csv