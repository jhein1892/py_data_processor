import pandas
import curses
import operator
import time
from colorama import Fore
import os.path
  
class File:

    def __init__(self, name, finalName):
        if os.path.isfile(name.strip()):
            self.final = finalName.strip() # What we are going to name the file once we've completed the filter
            self.name = name.strip() # The file name that we are reading from
            self._checkExt()
            self._readFile()
        else:
            print(Fore.RED + 'Document Path name not recognized' + Fore.WHITE)

    def description(self):
        print(f"We are reading from {self.name}, and turning it into {self.final}")

    # Supplemental function used to time execution of function
    def _timing_decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            print(Fore.YELLOW + f"{func.__name__} Elapsed time: {round(end_time - start_time, 4)} seconds" + Fore.WHITE)
            return result
        return wrapper
    
    # Opening and reading the CSV file
    def _readFile(self):
        df = pandas.read_csv(self.name)
        self.df = df
        self._getColumns()

    def _checkExt(self):
        finalExt = os.path.splitext(self.final)
        currentExt = os.path.splitext(self.name)
        if finalExt[-1].lower() != currentExt[-1].lower():
            self.final = os.path.join(
                os.path.basename(self.final),
                currentExt[1].lower()
            ).replace('/','')

    # Get the columns for this file
    def _getColumns(self): #
        self.column_names = self.df.columns
        self._setFilterParams()

    # Set the Column to filter by        
    def _setColumnFilter(self):
        index = 0 # So we know where we are in the list
        height, width = curses.initscr().getmaxyx()
        pad = curses.newpad(len(self.column_names), width)

        # Print the initial list of options
        def draw(stdscr, index, offset):
            stdscr.clear()
            pad.refresh(offset, 0, 0, 0, height - 1, width - 1)
            stdscr.addstr(f"What Column would you like to filter by?\n")
            for i, option in enumerate(self.column_names):
                if i == index:
                    stdscr.addstr(f"> {option}\n", curses.A_STANDOUT)
                elif abs(i  - index) <= 2 :
                    stdscr.addstr(f" {option}\n")
                else:
                    pad.addstr(i, 0, option)
            stdscr.refresh()

        def getColumnFilter(stdscr,index,offset):
            chosen = False
            while chosen is False:
                draw(stdscr, index, offset)
                key = stdscr.getch()
                
                # Move the selected option up or down
                if key == curses.KEY_UP:
                    index = max(index - 1, 0)
                    if index < offset:
                        offset -= 1
                elif key == curses.KEY_DOWN:
                    index = min(index + 1, len(self.column_names) - 1)
                    if index >= offset + height - 1:
                        offset += 1
                elif key == curses.KEY_ENTER or key == 10 or key == 13:
                    self.filterColumn = self.column_names[index]
                    stdscr.clear()
                    self._setOperatorFilter(stdscr)
                    chosen = True

        curses.wrapper(getColumnFilter, index, 0)            

    # Set the operation to filter by
    def _setOperatorFilter(self, stdscr):
        index = 0 # So we know where we are in the list
        chosen = False
        options = ['<', '>', '==', '!=', '<=', '>=']

        # Print the initial list of options
        def draw(stdscr, index):
            stdscr.clear()
            stdscr.addstr(f"{self.filterColumn} is ____\n")
            for i, option in enumerate(options):
                if i == index:
                    stdscr.addstr(f"> {option}\n", curses.A_STANDOUT)
                else:
                    stdscr.addstr(f"  {option}\n")
        
        while chosen is False:
            draw(stdscr, index)
            key = stdscr.getch()
            # Move the selected option up or down
            if key == curses.KEY_UP:
                index = (index - 1) % len(options)
            elif key == curses.KEY_DOWN:
                index = (index + 1) % len(options)
            elif key == curses.KEY_ENTER or key == 10 or key == 13:
                self.operator = options[index]
                stdscr.clear()
                self._setValueFilter(stdscr)
                chosen = True
            
    # Set the value to filter by
    def _setValueFilter(self, stdscr):
        chosen = False
        valueStr = ''

        def draw(stdscr):
            stdscr.clear()
            stdscr.addstr(f"{self.filterColumn} is {self.operator} ____\n")
            stdscr.addstr(f"> {valueStr}\n", curses.A_STANDOUT)

        while chosen is False:
            draw(stdscr)
            key = stdscr.getch()
            if key == curses.KEY_ENTER or key == 10 or key == 13:
                self.value = valueStr
                stdscr.clear()
                chosen = True
            elif key == curses.KEY_BACKSPACE or key == 127 or key == 263:
                valueStr = valueStr[:-1]
            else:
                valueStr += curses.keyname(key).decode('utf-8')

    #Update the data frame to be filtered accoring to values
    @_timing_decorator
    def _updateDataFrame(self):
        op_dict ={
            "<": operator.lt,
            "<=": operator.le,
            ">": operator.gt,
            ">=": operator.ge,
            "==": operator.eq,
            "!=": operator.ne
        }

        op_func = op_dict[self.operator] # get opterator that we chose
        newDF = self.df.copy()
        if self.value.isnumeric():
            self.value = float(self.value)
        
        print(f"Updating {self.name} where {self.filterColumn} is {self.operator} {self.value}")
        try:
            newDF = newDF[newDF[self.filterColumn].apply(lambda x: op_func(x, self.value))]
            self.df = newDF
        except:
            print(Fore.RED + f"Oops. Seems like you've entered a wrong value type for this column" + Fore.WHITE)
            return

    # Generating the updated CSV file with the filters
    @_timing_decorator
    def _generateNewFile(self):
        self.df.to_csv(self.final, index = False) # create and write a new file with the updated files.

    # Driver for setting the filter Params
    def _setFilterParams(self):
        moreFilters = 'y'
        while moreFilters == 'y':
            self._setColumnFilter()
            self._updateDataFrame()
            moreFilters = input("Would you like to filter by another column?(y/n) ")

        self._generateNewFile()
    
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
    baseDirectory = baseDirectory.strip()
    fileName = baseDirectory + '/' + name
    newFile = File(fileName, finalName) # Create new File

    userContinue = input("Would you like to filter another file? (y/n) ")
    if userContinue !='y':
        add = False

print("Thank you for using our data processor!")
