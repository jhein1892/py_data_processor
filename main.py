# General Idea: Take in data from a CSV file filter the data according to some conditions, write the results to another CSV file.
    # Making this object oriented: 
    # a class 'File', is instantiated with every new file that needs to be filtered. We take in a name, then prompt questions to determine columns values etc.

# First iteration: Hard Code the file name, the columns and conditions to filter by and the file name for the output file

# Second iteration, create CLI for interaction with program
import csv
import pandas
import curses


class File:

    def __init__(self, name, finalName):
        self.name = name # The file name that we are reading from
        self.final = finalName # What we are going to name the file once we've completed the filter
        self.readFile()

    def description(self):
        print(f"We are reading from {self.name}, and turning it into {self.final}")

    def readFile(self):
        df = pandas.read_csv(self.name)
        self.df = df
        self.getColumns()
    
        # nullDf = df.dropna() # All rows with a Nan value are being dropped
        # nullDf.to_csv(self.final, index = False) # create and write a new file with the updated files.

    # Get the columns for this file
    def getColumns(self): #
        self.column_names = self.df.columns
        self.setFilterParams()
        
    
    def setColumnFilter(self):
        print('setColumnFilter')
        index = 0 # So we know where we are in the list
        chosen = False

        # Initialize the curses library
        stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        stdscr.keypad(True)
        
        
        # Print the initial list of options
        stdscr.addstr(f"What Column would you like to filter by?\n")
        for i, option in enumerate(self.column_names):
            if i == index:
                stdscr.addstr(f"> {option}\n", curses.A_STANDOUT)
            else:
                stdscr.addstr(f"  {option}\n")
        

        while chosen is False:
            key = stdscr.getch()
            
            # Move the selected option up or down
            if key == curses.KEY_UP:
                index = (index - 1) % len(self.column_names)
            elif key == curses.KEY_DOWN:
                index = (index + 1) % len(self.column_names)
            elif key == curses.KEY_ENTER or key == 10 or key == 13:
                self.filterColumn = self.column_names[index]
                stdscr.clear()
                self.setOperatorFilter(stdscr)

                chosen = True
            
            stdscr.clear()
            stdscr.addstr(f"What Column would you like to filter by?\n")
            # Print the updated list of options
            for i, option in enumerate(self.column_names):
                if i == index:
                    stdscr.addstr(f"> {option}\n", curses.A_STANDOUT)
                else:
                    stdscr.addstr(f"  {option}\n")
        
        # Clean up the curses library
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()
    
    def setOperatorFilter(self, stdscr):
        index = 0 # So we know where we are in the list
        chosen = False
        options = ['<', '>', '=', '<=', '>=']

        stdscr.addstr(f"{self.filterColumn} is ____\n")
        # Print the initial list of options
        for i, option in enumerate(options):
            print(option)
            if i == index:
                stdscr.addstr(f"> {option}\n", curses.A_STANDOUT)
            else:
                stdscr.addstr(f"  {option}\n")
        

        while chosen is False:
            key = stdscr.getch()
            # Move the selected option up or down
            if key == curses.KEY_UP:
                index = (index - 1) % len(options)
            elif key == curses.KEY_DOWN:
                index = (index + 1) % len(options)
            elif key == curses.KEY_ENTER or key == 10 or key == 13:
                self.operator = options[index]
                stdscr.clear()
                self.setValueFilter(stdscr)
                chosen = True
            
            # Print the updated list of options
            stdscr.clear()
            stdscr.addstr(f"{self.filterColumn} is ____\n")
            for i, option in enumerate(options):
                if i == index:
                    stdscr.addstr(f"> {option}\n", curses.A_STANDOUT)
                else:
                    stdscr.addstr(f"  {option}\n")

    def setValueFilter(self, stdscr):
        index = 0 # So we know where we are in the list
        chosen = False
        options = ['0', '1', '5', '25', '100']
        valueStr = ''

        stdscr.addstr(f"{self.filterColumn} is {self.operator} ____\n")
        stdscr.addstr(f"> {valueStr}\n", curses.A_STANDOUT)

        while chosen is False:
            key = stdscr.getch()
            if key == curses.KEY_ENTER or key == 10 or key == 13:
                self.value = valueStr
                stdscr.clear()
                chosen = True
            elif key == curses.KEY_BACKSPACE or key == 127 or key == 263:
                valueStr = valueStr[:-1]
            else:
                valueStr += curses.keyname(key).decode('utf-8')
            
            # Print the updated list of options
            stdscr.clear()
            stdscr.addstr(f"{self.filterColumn} is {self.operator} ____\n")
            stdscr.addstr(f"> {valueStr}\n", curses.A_STANDOUT)

    def setFilterParams(self):
        print('In FilterParams')
        moreFilters = True
        # So this is going to start to build us our filtering parameters
        # We want to first display all of our column names as options.
        # I want this to be like building a query for sql, but we are going to build a pandas function.
        while moreFilters:
            self.setColumnFilter()
            print(f"Your chosen Column is: {self.filterColumn}")
            print(f"Your chosen Operator is: {self.operator}")
            print(f"Your chosen Operator is: {self.value}")
            # if self.filterColumn:
            #     self.setOperatorFilter()

            moreFilters = False

        # Third Pick value (string or number)
        




add = True
baseDirectory = ''





while add is True:

    if len(baseDirectory) < 1:
        baseDirectory = input("What is the absolute path to the base directory for your data files? ")
    else:
        newDirectory = input(f"Is this file also found in: {baseDirectory}? (y/n) ")
        if newDirectory != 'y':
            baseDirectory = input("What is the absolute path to the base directory for your data files? ")

    name = input("What is the name of file you'd like to filter? ")
    finalName = input("What would you like to name the file containing the filtered data? ")
    fileName = baseDirectory + '/' + name

    newFile = File(fileName, finalName) # Create new File

    userContinue = input("Would you like to filter another file? (y/n) ")
    if userContinue !='y':
        add = False


print("Thank you for using our data processor!")





    
# /Users/jacobhein/Documents/MLBData/test.csv





#### THIS IS FOR THE COMMAND LINE INTEREACTION ####
# options = ["1", "2", "3", "4"]

# def select_options():
#     selected_options = []
#     index = 0
    
#     # Initialize the curses library
#     stdscr = curses.initscr()
#     curses.noecho()
#     curses.cbreak()
#     stdscr.keypad(True)
    
#     # Print the initial list of options
#     for i, option in enumerate(options):
#         if i == index:
#             stdscr.addstr(f"> {option}\n")
#         else:
#             stdscr.addstr(f"  {option}\n")
    
#     # Wait for user input
#     while len(selected_options) < 3:
#         key = stdscr.getch()
        
#         # Move the selected option up or down
#         if key == curses.KEY_UP:
#             index = (index - 1) % len(options)
#         elif key == curses.KEY_DOWN:
#             index = (index + 1) % len(options)
#         elif key == curses.KEY_ENTER or key == 10 or key == 13:
#             selected_options.append(options[index])
        
#         # Print the updated list of options
#         stdscr.clear()
#         for i, option in enumerate(options):
#             if i == index:
#                 stdscr.addstr(f"> {option}\n")
#             else:
#                 stdscr.addstr(f"  {option}\n")
    
#     # Clean up the curses library
#     curses.nocbreak()
#     stdscr.keypad(False)
#     curses.echo()
#     curses.endwin()
    
#     return selected_options

# # Call the select_options function and print the selected options
# selected = select_options()
# print(f"Selected options: {selected}")
####### #############