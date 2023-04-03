# Py Data Processor
This Python application allows you to filter a CSV file by a specified column, operator, and value. The resulting filtered data is then saved as a new CSV file.

## Getting Started
1. Clone the repository onto your local machine.
2. Ensure that you have pandas, csv, and curses installed by running `pip install pandas csv curses`.
3. Open a terminal window and navigate to the directory containing the main.py file.
4. Run python main.py.
5. Follow the on-screen prompts to select the CSV file you wish to filter and provide the necessary filtering criteria.

## How to Use
### Selecting a File
Upon launching the application, you will be prompted to provide the absolute path to the base directory for your data files. Make sure to leave out the final '/' as the application will fill that in for you. 

### Filtering the Data
After selecting a file, you will be prompted to select the column you would like to filter by. You can navigate through the options by pressing the up and down arrow keys. Press enter to select the desired column.

You will then be prompted to select an operator to apply to the selected column. You can choose from <, >, ==, !=, <=, or >=. Once again, you can navigate through the options by pressing the up and down arrow keys, and press enter to select your operator.

Finally, you will be prompted to enter a value to filter the selected column by. You can enter any numerical value you choose, and use backspace to correct mistakes. Press enter once you have entered your desired value.

### Generating a New File
After selecting a column, operator, and value, the application will generate a new CSV file containing only the rows that meet the specified filtering criteria. The new file will be saved under a name of your choosing.

You will be prompted to filter another file once your filtered data has been generated.

# Authors
- Jacob Hein
