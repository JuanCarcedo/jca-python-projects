"""
    By: Juan Carcedo Aldecoa
    Date: 11/12/2022
    Description:
        This program manages tasks.
        - Users can add a new task, view all tasks available and filter by own tasks.
        - Admin user can add users to the system and see stats. Also do anything that a user can.
    Note:
        try-except block to prevent (or alert) if any errors during file handling.
"""
# =====importing libraries===========
from datetime import date

# ====Constants====
# Useful constants for the main files.
USER_DATA = 'user.txt'
TASKS_DATA = 'tasks.txt'
# User and admin menu below.
USER_MENU = '''
+-- Select one of the following Options below:
\tr - Registering a user
\ta - Adding a task
\tva - View all tasks
\tvm - view my task
\te - Exit
+\tSelect: '''
ADMIN_MENU = '''
+-- Select one of the following Options below:
\tr - Registering a user
\ta - Adding a task
\tva - View all tasks
\tvm - view my task
\t+ -- (admin only) ---------- +
\t+ stat - Display statistics  +
\t+ -------------------------- +
\te - Exit
+\tSelect: '''


# ====Login Section====
def login() -> str:
    """
    Login to system logic. Only existing users can connect.
    :return: str --> Username if login correct, FAILURE_LOGIN if not
    """
    global user_data
    # Gather user data (username and password) ----------------------------------
    try:
        # Read user data with a loop per each line.
        for line in open(USER_DATA, 'r'):
            # Delete the \n at the end of the line and split the line in [user, password].
            raw_data = line.\
                replace('\n', '').\
                split(', ')
            # Gather the user data in a dictionary key = user, item = password.
            user_data[raw_data[0]] = raw_data[1]

    except FileNotFoundError:
        print(f'{USER_DATA} file not found.')

    # Login -- Only allow 10 attempts  ----------------------------------
    print('\n+----------- Login to system -----------+')
    print('+- Please input your credentials:')
    security = 10
    while security >= 0:
        username = input('\tUsername: ')
        # Get the password for that username, if it does not exist it will return False.
        password = user_data.get(username)
        if password:
            # Password it is not stored in the program (not needed), therefore it is directly checked.
            if input('\tPassword: ') == password:
                print(f'+- Welcome back {username}.')
                print('+----------- Login SUCCESS -----------+\n\n')
                return username
            else:
                print(f'+- Wrong password. ({security} attempts left)')

        else:
            print(f'+- Username {username} does not exists. ({security} attempts left)')
        # Reduce the security counter.
        security -= 1

    else:
        # Only executed if the while loop ends (too many attempts).
        print('+- Number of attempts exceeded.')
        print('+----------- Login FAILED -----------+')
        return 'FAILURE_LOGIN'


# ====Add a user Section====
def add_user(username: str, password: str) -> None:
    """
    Add a user to the system (user.txt file).
    :param username: New username to add
    :param password: New password to add
    :return: None
    """
    # Prepare the input with username and password.
    new_data = f'\n{username}, {password}'
    # Opening option 'a' will create the file if it is not found.
    with open(USER_DATA, 'a') as file:
        file.write(new_data)


# ====Task management====
def tasks_management(action: str) -> None:
    """
    Method that manages the tasks.
        To retrieve tasks use 'gather_tasks'.
        To update/add new task use 'add_task'.
    :param action: Selection of behaviour of method: gather_tasks or add_task
    :return:
    """
    global tasks_data
    if action == 'gather_tasks':
        # Gather task's data ----------------------------------
        try:
            # Read tasks with a loop per each line.
            for line in open(TASKS_DATA, 'r'):
                # Delete the \n at the end of the line and split the line in a list.
                raw_data = line. \
                    replace('\n', ''). \
                    split(', ')
                # Gather task data into a multidimensional list.
                tasks_data.append(raw_data)

        except FileNotFoundError:
            print(f'{TASKS_DATA} file not found.')

    elif action == 'add_task':
        # Add new task ----------------------------------
        # Gather data for the new task
        print('+- Please fill the following data regarding the task.')
        # Get the actual date
        date_today = date.today()
        # Directly include in a list the new data for input or
        # use hardcoded fields like completed == no or actual date (Day Month Year).
        new_task_data = [
            input('Username assigned to task: '),
            input('Title: '),
            input('Description: '),
            f'{date_today.day} {date_today.strftime("%B")[:3]} {date_today.year}',
            input('Due date: '),
            'No'
        ]
        # Opening option 'a' will create the file if it is not found.
        with open(TASKS_DATA, 'a') as file:
            file.write('\n' + ', '.join(new_task_data))
        # Update the task_data variable being used in the program
        tasks_data.append(new_task_data)

    else:  # Unlikely scenario although added
        print('Invalid selection.')


# Repeated action from printing tasks
def print_tasks(task: list) -> None:
    """
    Method will print the 'task' sent as parameter.
    :param task: Task to print.
    :return: None
    """
    # Get all task fields and print in correct placement.
    # Use unicode to print a full solid line.
    print(u'\u2500' * 50)
    print(f'Task:\t\t\t\t\t{task[1]}')
    print(f'Assigned to:\t\t\t{task[0]}')
    print(f'Date assigned:\t\t\t{task[3]}')
    print(f'Due date:\t\t\t\t{task[4]}')
    print(f'Task Complete?\t\t\t{task[5]}')
    print(f'Task description:\n {task[2]}')
    print(u'\u2500' * 50)


# ====Main program execution====
if __name__ == '__main__':
    print('\n+----------- Task manager started -----------+')
    # Variable for user_data will be kept available for statistics with admins
    user_data = {}
    # If login it is not successful then exit the program
    user = login()
    if user == 'FAILURE_LOGIN':
        exit()

    # Gather tasks from the task.txt file into a multidimensional list
    tasks_data = []
    # Method to control the task file. action parameter defines what it does.
    print('\n+-- Loading tasks file -----------+')
    tasks_management(action='gather_tasks')
    print('+-- Task file loaded -----------+\n')

    # Menu available
    while True:
        # presenting the menu to the user and making sure that
        # the user input is converted to lower case.
        # menu loaded is based on user (admin has a different menu).
        menu_type = ADMIN_MENU if user == 'admin' else USER_MENU
        menu = input(menu_type).lower()

        if menu == 'r':
            # Add a new user and password to the user.txt file.
            # Gather username and password.
            print('\n\n+----------- Register a user -----------+')
            if user == 'admin':
                print(f'+- Please fill the following information.')
                # Gather new data:
                new_username = input('\tNew username: ')
                new_password = input('\tNew password: ')
                # Check of password with another input.
                if new_password == input('\tConfirm new password: '):
                    # Add new user
                    add_user(username=new_username, password=new_password)
                    # Include it in the current user_data variable.
                    user_data[new_username] = new_password
                    print('+- Success: New user added.')
                else:
                    print('+- Error, passwords do not match.')
            else:
                # User is not an admin.
                print('+- Error. Only admin can add users.')
            print('+------------------------------------------+\n\n')

        elif menu == 'a':
            print('\n\n+----------- Add a task -----------+')
            # Call the function that manages tasks
            tasks_management(action='add_task')
            print('+- Success: New task added.')
            print('+------------------------------------------+\n\n')

        elif menu == 'va':
            print('\n\n+----------- View all tasks -----------+')
            print(f'+- Printing list of tasks....')
            # Loop over all the tasks and print them.
            for task_item in tasks_data:
                print_tasks(task_item)
            print('+------------------------------------------+\n\n')

        elif menu == 'vm':
            print('\n\n+----------- View my task(s) -----------+')
            print(f'+- Printing list of {user}\'s tasks....')
            # Only print user's data. Else do not print anything.
            for task_item in tasks_data:
                if task_item[0] == user:
                    print_tasks(task_item)
            print('+------------------------------------------+\n\n')

        elif menu == 'stat' and user == 'admin':
            # Only for admin users. Users cannot access this option even if the type it.
            # Displayed max number of users and total number of tasks.
            print('\n\n+----------- Display statistics -----------+')
            print(f'+- Users in the system (admin included): {len(user_data)}')
            print(f'+- Tasks stored in the system: {len(tasks_data)}')
            print('+------------------------------------------+\n\n')

        elif menu == 'e':
            # Updated end message.
            print('\n+----------- Session Ended -----------+')
            exit()

        else:
            print("You have made a wrong choice. Please try again.")
