"""
    Date: 17/12/2022
    Description:
        This program manages tasks.
        - Users can add a new task, view all tasks available and filter by own tasks.
        - Admin user can add users to the system and see stats. Also do anything that a user can.
    Note:
        try-except block to prevent (or alert) if any errors during file handling.
    :copyright: (c) 2022 Juan Carcedo, All rights reserved
    :licence: MIT, see LICENSE.txt for further details.

    Variables notes:
    TYPE	NAME					CONTENTS
    dict	user_data				{user: password}
    list	tasks_data				[[
                                    assigned to,
                                    task,
                                    task_description,
                                    date_assigned,
                                    due_date,
                                    status (yes/no)]]
    dict	task_numbers			{key = task + date_assigned: value = number}
    dict	system_statistics		{general: [
                                        total_number_tasks,
                                        tasks_completed,
                                        not_completed_and_overdue]
                                     user: [
                                        task_assigned,
                                        task_completed,
                                        not_completed_and_overdue]
                                    ...
                                    }
"""
# =====importing libraries===========
from datetime import date

# ====Constants====
# Useful constants for the main files.
USER_DATA = 'user.txt'
TASKS_DATA = 'tasks.txt'
TASK_OVERVIEW = 'task_overview.txt'
USER_OVERVIEW = 'user_overview.txt'
# Date and time related constants +++++++++++++++
# Date today (for due dates and date assigned).
DATE_TODAY = date.today()
# Date formatted for the files.
DATE_TODAY_FORMAT = f'{DATE_TODAY.day} {DATE_TODAY.strftime("%B")[:3]} {DATE_TODAY.year}'
# Dictionary to do a quick translation between str month to int month.
MONTH_TO_INT = {
    'Jan': 1,
    'Feb': 2,
    'Mar': 3,
    'Apr': 4,
    'May': 5,
    'Jun': 6,
    'Jul': 7,
    'Aug': 8,
    'Sep': 9,
    'Oct': 10,
    'Nov': 11,
    'Dec': 12
}

# User and admin menu below.
USER_MENU = '''
+-- Select one of the following Options below:
\tr  - Registering a user
\ta  - Adding a task
\tva - View all tasks
\tvm - View my task
\tgr - Generate reports
\te  - Exit
+\tSelect: '''
ADMIN_MENU = '''
+-- Select one of the following Options below:
\tr  - Registering a user
\ta  - Adding a task
\tva - View all tasks
\tvm - View my task
\tgr - Generate reports
\t+--- (admin only) --------- +
\t+ ds - Display statistics   +
\t+-------------------------- +
\te  - Exit
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
def reg_user() -> None:
    """
    Add a user to the system (user.txt file).
    :return: None
    """
    global user_data
    print(f'+- Please fill the following information.')
    # Gather new data:
    while True:
        new_username = input('\tNew username: ')
        # Check if the user already exists.
        if new_username in user_data.keys():
            print('+ User already exists. Please use another username.')
        else:
            break

    new_password = input('\tNew password: ')
    # Check of password with another input.
    if new_password == input('\tConfirm new password: '):
        # Add new user
        # Prepare the input with username and password.
        new_data = f'\n{new_username}, {new_password}'
        # Opening option 'a' will create the file if it is not found.
        with open(USER_DATA, 'a') as file:
            file.write(new_data)
        # Include it in the current user_data variable.
        user_data[new_username] = new_password
        print('+- Success: New user added.')
    else:
        print('+- Error, passwords do not match.')


# ====Task management====
def tasks_management(action: str) -> None:
    """
    Method that manages the tasks.
        To retrieve tasks use 'gather_tasks'.
        To update/add new task use 'add_task'.
    :param action: Selection of behaviour of method: gather_tasks or add_task
    :return: None.
    """
    global tasks_data, tasks_numbers
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
                # Update the numeration of tasks with a dictionary.
                tasks_numbers[raw_data[1]+raw_data[3]] = len(tasks_data) - 1

        except FileNotFoundError:
            print(f'{TASKS_DATA} file not found.')

    elif action == 'add_task':
        # Add new task ----------------------------------
        # Gather data for the new task
        print('+- Please fill the following data regarding the task.')
        # Directly include in a list the new data for input or
        # use hardcoded fields like completed == no or actual date (Day Month Year).
        # Note DATE_TODAY_FORMAT is Today.
        new_task_data = [
            input('Username assigned to task: '),
            input('Title: '),
            input('Description: '),
            DATE_TODAY_FORMAT,
            input('Due date (DD Mon YYYY): '),
            'No'
        ]
        # Opening option 'a' will create the file if it is not found.
        with open(TASKS_DATA, 'a') as file:
            file.write('\n' + ', '.join(new_task_data))
        # Update the task_data variable being used in the program
        tasks_data.append(new_task_data)
        # Update the numeration of tasks with a dictionary.
        tasks_numbers[new_task_data[1]+new_task_data[3]] = len(tasks_data) - 1

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
    print(f'Task number:\t\t\t{tasks_numbers[task[1]+task[3]]}')
    print(f'Task:\t\t\t\t\t{task[1]}')
    print(f'Assigned to:\t\t\t{task[0]}')
    print(f'Date assigned:\t\t\t{task[3]}')
    print(f'Due date:\t\t\t\t{task[4]}')
    print(f'Task Complete?\t\t\t{task[5]}')
    print(f'Task description:\n {task[2]}')
    print(u'\u2500' * 50)


def view_all(all_tasks) -> None:
    """
    Prepare the view to print all tasks.
    :param all_tasks: List of tasks.
    :return: None.
    """
    print('\n\n+----------- View all tasks -----------+')
    print(f'+- Printing list of tasks....')
    # Loop over all the tasks and print them.
    for task_item in all_tasks:
        print_tasks(task_item)
    print('+------------------------------------------+\n\n')


def view_mine(all_tasks) -> None:
    """
    Prepare the view to print all user's tasks.
    :param all_tasks: List of tasks.
    :return: None.
    """
    user_available_tasks = []  # Store user tasks
    user_number_tasks = []  # Number of task (ID)
    print('\n\n+----------- View my task(s) -----------+')
    print(f'+- Printing list of {user}\'s tasks....')
    # Only print user's data. Else do not print anything.
    for task_item in all_tasks:
        if task_item[0] == user:
            print_tasks(task_item)
            user_available_tasks.append(task_item)
            user_number_tasks.append(tasks_numbers[task_item[1]+task_item[3]])
    print('+------------------------------------------+\n\n')
    # Specific selection of tasks.
    print('+- Would you like to select any specific task?')
    try:
        # try-except block to prevent issues whilst using cast
        task_selected = int(input('+ Enter task number, or -1 to return to menu: '))

    except ValueError:
        print('+ Please enter a number only.')

    else:
        # Note, when wrong input or not available option is selected, the command
        # return will exit the function to the main menu.
        if task_selected == -1:
            # Exit the function to main menu.
            return

        # Gather the data.
        for task_item in user_available_tasks:
            current_task_number = tasks_numbers[task_item[1] + task_item[3]]
            if current_task_number == task_selected:
                global tasks_data  # Made it possible to change the data

                # Check first if the task can be modified.
                if tasks_data[current_task_number][5] == 'Yes':
                    print(f'+- Task {current_task_number} cannot be modified. Task is already completed.')
                    return

                print('+- Selected task:')
                # Retrieve the task and print it.
                print_tasks(all_tasks[current_task_number])
                # Get the selection from user.
                print('+- What would you like to do. Mark as complete or edit the task.')
                selection = input('+ Select "complete" or "edit": ').lower()
                if selection == 'complete':
                    # Access the task in the global variable and set to Yes.
                    tasks_data[current_task_number][5] = 'Yes'
                    print(f'+- Task {current_task_number} set to completed.')
                    return

                elif selection == 'edit':
                    edit_selection = input('+- Edit username or due date? ').lower()
                    # Base on the selection, change username or due date
                    if edit_selection == 'username':
                        tasks_data[current_task_number][0] = input('+ Enter new username: ')

                    elif edit_selection == 'due date':
                        tasks_data[current_task_number][4] = input('+ Enter new due date (DD Mon YYYY): ')

                    else:
                        print('+- Selection not available.')
                    return

                else:
                    print('+- Selection not available.')
                    # Finish the cycle.
                    return

        else:
            # End of for without any option checked.
            print('+ The selected task is not available for this user.')


# ====Reports management====
def report_files_management(action: str = 'read', task_report: str = 'empty', user_report: str = 'empty') -> tuple:
    """
    Create files in the system.
    Default values used to prevent wrong/empty definitions.
    :param action: Select if 'write' or 'read' is needed.
    :param task_report: Data gathered to create task report.
    :param user_report: Data gathered to create user report.
    :return: Only for 'read' mode. Return tuple with data from reports.
    """
    if action == 'write':
        # Opening option 'w' will create the file if it is not found. Also, it will
        # erase all previous content. No errors expected.
        # task_overview ----------------------------------
        with open(TASK_OVERVIEW, 'w') as file:
            file.write(task_report)
        print('+- Task overview created/updated.')
        # user_report ----------------------------------
        with open(USER_OVERVIEW, 'w') as file:
            file.write(user_report)
        print('+- User overview created/updated.')

    elif action == 'read':
        # read data from files.
        report_task_data, report_user_data = '', ''
        try:
            # try-except block to prevent error due to files not being created beforehand.
            # task_overview ----------------------------------
            with open(TASK_OVERVIEW, 'r') as file:
                report_task_data = file.read()
            # user_report ----------------------------------
            with open(USER_OVERVIEW, 'r') as file:
                report_user_data = file.read()

        except FileNotFoundError:
            # If file not found, they will be generated.
            # Note it will return a tuple with task and user data.
            report_task_data, report_user_data = generate_reports()

        finally:
            # Finally used so even if there is an error the data will be returned.
            # Return the data gathered.
            return report_task_data, report_user_data

    else:
        print('+- Wrong selection whilst managing report files.')
        return None, None


def generate_reports() -> tuple:
    """
    Create two reports: user_overview and task_overview.
    :return: tuple with data for user and task reports.
    """
    print('\n\n+----------- Generation of reports -----------+')
    print('+- Gathering and compiling data...')
    # Gather all data for the generation of reports.
    # Default member is general, used to save down task data.
    system_statistics = {'general': [0, 0, 0]}
    # Loop through the full list of tasks available.
    for task_item in tasks_data:
        # General data:
        system_statistics['general'][0] += 1  # Total number of tasks.
        user_in_task = task_item[0]
        # Create the new user in the statistics if it does not exist.
        if user_in_task not in system_statistics.keys():
            system_statistics.update({user_in_task: [0, 0, 0]})
        system_statistics[user_in_task][0] += 1  # Add 1 to number of tasks for user.

        # Check if the task is completed:
        if task_item[5].lower() == 'yes':
            # Update completed tasks statistics.
            system_statistics['general'][1] += 1  # General.
            system_statistics[user_in_task][1] += 1  # User.

        else:
            # Only check if it is overdue if it is not completed.
            # Transform due date to a date format.
            split_due_date = task_item[4].split(' ')
            try:
                # try-except to prevent multiple issues below: cast to int, errors during date format....
                due_date = date(int(split_due_date[2]),
                                MONTH_TO_INT.get(split_due_date[1]),
                                int(split_due_date[0]))

            except ValueError as err:
                print(f'+-- ERROR in {task_item[1]} for user {task_item[0]} when gathering statistics.')
                print(f'+-- {err}')

            except TypeError as err:
                print(f'+-- ERROR in {task_item[1]} for user {task_item[0]} when gathering statistics.')
                print(f'+-- {err}')

            else:
                # All correct.
                if DATE_TODAY > due_date:
                    # Incomplete and outdated.
                    system_statistics['general'][2] += 1  # General.
                    system_statistics[user_in_task][2] += 1  # User.

    # Use variables for the items to be easier to control later on when printing.
    # Note that if total_tasks are 0, most of the variables will be set to 0.
    total_tasks = system_statistics["general"][0]
    task_completed = system_statistics["general"][1]
    task_incomplete = total_tasks - task_completed if total_tasks > 0 else 0
    task_overdue = system_statistics["general"][1]
    total_users_with_tasks = len(system_statistics) - 1  # Not count General
    # Percentages; prevent division by 0.
    total_task_completed_per = 100 * round(task_completed / total_tasks, 2) if total_tasks > 0 else 0
    total_task_overdue_per = 100 * round(task_overdue / total_tasks, 2) if total_tasks > 0 else 0

    print('+- Gathering and compiling data --> OK.')

    # Save down the reports only if the total_tasks is higher than 0.
    if total_tasks == 0:
        print('+- Task overview and user overview will not be saved due to Total tasks being empty.')

    else:
        # Save down the data in an easy format to write later in files.
        # Task overview generation.
        print('+- Generating task overview...')
        task_report = '+------------- Task Overview Report -------------+\n' \
                     f'+- Total number of tasks:    {total_tasks}\n' \
                     '+- Of which:\n' \
                     f'+- \tCompleted:               {task_completed} ({total_task_completed_per}% of total)\n' \
                     f'+- \tIncomplete:              {task_incomplete} ({100 - total_task_completed_per}% of total)\n' \
                     f'+- \tIncomplete and overdue:  {task_overdue} ({total_task_overdue_per}% of total)\n' \
                     '+------------------------------------------------+\n'

        # User overview generation.
        print('+- Generating user overview...')
        user_report = '+------------- User Overview Report -------------+\n' \
                      f'+- Total number of users with tasks:    {total_users_with_tasks}\n' \
                      f'+- Total number of tasks:               {total_tasks}\n'
        # Gather user tasks:
        if total_users_with_tasks > 0:
            # Loop over the users to print their stats.
            for key, values in system_statistics.items():
                # Only print for users, not for General.
                if key != 'general':
                    # Create variables to be used in the report. Prevent issues whilst dividing by 0.
                    user_tasks_against_total_per = 100 * round(values[0] / total_tasks, 2) if total_tasks > 0 else 0
                    user_tasks_completed_percentage = 100 * round(values[1] / values[0], 2) if values[0] > 0 else 0
                    not_completed_and_overdue = 100 * round(values[2] / values[0], 2) if values[0] > 0 else 0
                    user_report += f'+- Data for user {key}:\n' \
                                   f'+-\tTasks assigned:                     {values[0]}\n' \
                                   f'+- \tPercentage of all tasks:           {user_tasks_against_total_per}%\n' \
                                   f'+-\tTasks completed:                    {user_tasks_completed_percentage}%\n' \
                                   f'+-\tTasks to-be completed:              {100 - user_tasks_completed_percentage}%\n' \
                                   f'+-\tTo-be completed and overdue:        {not_completed_and_overdue}%\n'

        else:
            # No users with tasks
            user_report += '+- No users with tasks.\n'

        user_report += '+------------------------------------------------+\n'

        # Generate the reports in the system.
        report_files_management('write', task_report, user_report)

        print('+-------------Process completed-------------+\n\n')

        # Return data gathered (used in display_admin_statistics()).
        return task_report, user_report


def display_admin_statistics() -> None:
    """
    Display statistics for admin user.
    :return: None
    """
    # Display system reports.
    print('\n+----------- System Statistics -----------+\n')
    # Gather the required data:
    data_admin = report_files_management(action='read')  # Tuple with full data from files.
    # Task Overview Report =====
    print(data_admin[0])
    # User Overview Report =====
    print(data_admin[1])


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
    # Save the numeration of tasks. Note the format will be:
    # key = task + date assigned. values = number.
    tasks_numbers = {}  # Used to enumerate the tasks.
    # Method to control the task file. action parameter defines what it does.
    print('\n+-- Loading tasks file -----------+')
    tasks_management(action='gather_tasks')
    print('+-- Task file loaded -----------+\n')

    # Menu available
    while True:
        # Presenting the menu to the user and
        # making sure that the user input is converted to lower case.
        # menu loaded is based on user (admin has a different menu).
        menu_type = ADMIN_MENU if user == 'admin' else USER_MENU
        menu = input(menu_type).lower()

        if menu == 'r':
            # Add a new user and password to the user.txt file.
            # Gather username and password.
            print('\n\n+----------- Register a user -----------+')
            if user == 'admin':
                # Call function to add new user.
                reg_user()
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
            # Print all tasks.
            view_all(tasks_data)

        elif menu == 'vm':
            # Print user's tasks.
            view_mine(tasks_data)

        elif menu == 'gr':
            # Generate reports as task overview and user overview.
            # Note in this case it is not needed to gather the returned data.
            generate_reports()

        elif menu == 'ds' and user == 'admin':
            # Only for admin users. Users cannot access this option even if the type it.
            display_admin_statistics()

        elif menu == 'e':
            # Updated end message.
            print('\n+----------- Session Ended -----------+')
            exit()

        else:
            print("You have made a wrong choice. Please try again.")
