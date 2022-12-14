"""
    By: Juan Carcedo Aldecoa
    Date: 12/12/2022
    Note:
        Function converter reads a file (input) and execute the operations requested
        with the members in a list. Then save the result in output file.

        try-except used to handle errors whilst using files.
        No try-except is used for the inputs as required.
"""
# IMPORTS ====
from math import ceil, floor

# CONSTANTS ====
INPUT_FILE = 'input.txt'
OUTPUT_FILE = 'output.txt'


# CALCULATION FUNCTIONS ====
def mod_min(list_data: list):
    """
    Returns the minimum from a list.
    :param list_data: List to find the minimum.
    :return: Minimum.
    """
    # sort the list, by default the smallest number will be in position [0].
    list_data.sort()
    return list_data[0]


def mod_max(list_data: list):
    """
    Returns the maximum from a list.
    :param list_data: List to find the maximum.
    :return: Maximum.
    """
    # sort the list, by default the largest number will be in position [-1].
    list_data.sort()
    return list_data[-1]


def mod_avg(list_data: list):
    """
    Returns the average from a list.
    :param list_data: List to find the average.
    :return: Average.
    """
    # Calculate the average from the list.
    average_list = sum(list_data) / len(list_data)
    return average_list


def mod_sum(list_data: list):
    """
    Returns the sum of all members in the list.
    :param list_data: List to find the sum.
    :return: Sum.
    """
    # Calculate the sum.
    return sum(list_data)


def percentile(list_data: list, percentile_th: int):
    """
    Returns the sum of all members in the list.
    :param list_data: List to find the sum.
    :param percentile_th: Percentile th to find.
    :return: Percentile.
    """
    # Order the list
    list_data.sort()
    # Formula for percentile; final index must be reduced by 1 (else possible out of range index).
    # Only apply ceil for numbers over 0.5 (nearest-rank), else floor.
    index_percentile = (percentile_th / 100) * len(list_data)
    if index_percentile % 1 >= 0.5:
        index_percentile = ceil(index_percentile) - 1
    else:
        index_percentile = floor(index_percentile) - 1
    return list_data[index_percentile]


# FILE MANAGER ====
def file_manager(mode: str = 'read'):
    """
    Handles the read and write functions.
    :param mode: 'read' for reading and 'write' for writing.
    :return: None
    """
    global input_data
    if mode == 'write':
        # Write mode
        output_data = []
        print(f'+- Calculating.....')

        # Loop through all the required data
        for item in input_data:
            # Select the operation
            if item[0] == 'avg':
                # Calculate average
                calculation = f'The avg of {item[1]} is {mod_avg(item[1])}\n'

            elif item[0] == 'max':
                # Calculate maximum
                calculation = f'The max of {item[1]} is {mod_max(item[1])}\n'

            elif item[0] == 'min':
                # Calculate minimum
                calculation = f'The min of {item[1]} is {mod_min(item[1])}\n'

            elif item[0] == 'sum':
                # Calculate the sum
                calculation = f'The sum of {item[1]} is {mod_sum(item[1])}\n'

            elif item[0][0] == 'p':
                # Calculate the percentile
                # Get the number p90 --> 90; note cast is needed.
                percentile_number = int(item[0][1:])
                calculation = f'The {percentile_number}th percentile of {item[1]}' \
                              f' is {percentile(item[1], percentile_number)}\n'

            else:
                # Nothing, not defined
                continue

            # Append into the output data.
            output_data.append(calculation)

        # Save the new data into the output file
        with open(OUTPUT_FILE, 'w') as file:
            file.writelines(output_data)

        print(f'+- Data saved into {OUTPUT_FILE}')

    else:  # Read mode
        try:
            # try-except to prevent file not found error
            with open(INPUT_FILE, 'r', encoding='utf-8-sig') as file:
                # format of file function:numbers
                for lines in file:
                    # Replace \n for empty and split the list using : --> result ['function', 'values']
                    lines = lines.replace('\n', '').split(':')
                    # Split the 'values' into [values]
                    lines[1] = lines[1].split(',')
                    # Convert to integer using map and lambda functions.
                    lines[1] = list(map(lambda x: int(x), lines[1]))
                    input_data.append(lines)

        except FileNotFoundError:
            print(f'File {INPUT_FILE} not found in folder.')

        else:
            print(f'+- Data loaded from {INPUT_FILE}')


# MAIN ======
if __name__ == '__main__':
    # Data from input file will be saved in a multidimensional list.
    input_data = []
    print('+---------- Function converter ----------+')
    # Gather the data; note that default mode is 'read'.
    file_manager()
    # Generate an output data list.
    file_manager(mode='write')
    print('+--------------- Goodbye ---------------+')
