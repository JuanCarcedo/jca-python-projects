"""
    By: Juan Carcedo Aldecoa
    Date: 10/12/2022
    Description:
        A program to check and overview the contents of a file.
    Note:
        try-except block to prevent (or alert) if any errors during file handling.
"""

# Constant with the root to the file
INPUT_FILE = 'input.txt'

if __name__ == '__main__':
    try:
        # File's handling should be kept inside a try-except to catch errors.
        # Note all iterations with file is inside the try-except.
        # open in read only as no write action is needed. Encoding set for security reasons.
        with open(INPUT_FILE, 'r+', encoding='utf-8') as file:
            # Loop over each line to count number of lines and gather file contents.
            number_of_lines = 0
            file_contents = ''
            for line in file:
                # Counter of lines
                number_of_lines += 1
                # Gather the full text
                file_contents += line
            # Convert to list and then count the length to know how many words.
            counter_of_words = len(file_contents.split())
            # Set the full contents to lower so the count is easier (one call)
            file_contents_lower = file_contents.lower()

    except FileNotFoundError:
        print(f'File {INPUT_FILE} was not found in the folder.')

    else:
        # Display data from file
        # Note: number of characters may differ from word or notepad++, using the
        # file_contents printed in the console, and selecting it (in PyCharm), will show the
        # same numbers of characters as the variable.
        print(f'+----------- File {INPUT_FILE} overview -----------+')
        print(f'+- Number of characters: {len(file_contents)}')
        print(f'+- Number of words: {counter_of_words}')
        print(f'+- Number of lines: {number_of_lines}')
        print(f'+- Vowel counter:')
        print(f'\ta: {file_contents_lower.count("a")}')
        print(f'\te: {file_contents_lower.count("e")}')
        print(f'\ti: {file_contents_lower.count("i")}')
        print(f'\to: {file_contents_lower.count("o")}')
        print(f'\tu: {file_contents_lower.count("u")}')
        print('+- Text in file:')
        print(file_contents)
        print('+-------------------------------------+')
