"""
    Date: 15/12/2022
    Note:
        An Email platform simulation.
        try-except blocks to prevent errors during execution.
        assert used to prevent unrealistic input.
    :copyright: (c) 2022 Juan Carcedo, All rights reserved
    :licence: MIT, see LICENSE.txt for further details.
"""
# imports ====
from email import Email

# CONSTANTS ====
MENU = '''+\tadd
+\tshow unread
+\tread
+\tsend
+\tmark spam
+\tshow spam
+\tdelete
+\tquit
+-- Select: '''


def add_email(content: str, sender: str) -> Email:
    """
    Create a new email object and return it.
    :param content: Email body.
    :param sender: Sender.
    :return: Email.
    """
    # Create an instance of the class and return it.
    email = Email(sender, content)
    return email


def delete_email(email_number: int = 0) -> None:
    """
    Delete an email.
    :param email_number: Position/index in the inbox list of the email.
    :return: None
    """
    # Check if the index is available (it can also be done with try-except and/or assert).
    if email_number >= len(inbox):
        print(f'This email does not exists. Please select an email between 0 and {len(inbox) - 1}.')

    else:
        # Gather email and ask for confirmation before deleting.
        email_to_delete = inbox[email_number]
        print(f'+-- Email from {email_to_delete.from_address} will be deleted.')
        if input('+- Please confirm (Y/N): ').lower() == 'y':
            inbox.pop(email_number)
            print('+- Email deleted ------+')
        else:
            print('+- Deletion aborted ------+')


def get_count() -> int:
    """
    Calculate the number of emails in the inbox.
    :return: Number of emails (items) in inbox.
    """
    return len(inbox)


def get_email(email_number: int = 0) -> None:
    """
    Read an email in the inbox, print it and mark it as read.
    :param email_number: Position/index in the inbox list of the email.
    :return: None
    """
    # Check if the index is available (it can also be done with try-except).
    if email_number >= len(inbox):
        print(f'This email does not exists. Please select an email between 0 and {len(inbox) - 1}.')

    else:
        # Set email to read = True.
        email_to_read = inbox[email_number]
        email_to_read.mark_as_read()
        print(f'+-- Email from {email_to_read.from_address}:')
        print(email_to_read.email_contents)
        print('+- END of email ------+')


def send_email() -> bool:
    """
    Write and send an email.
    :return: Return True if it was successful and False else.
    """
    # Logic to gather the relevant fields.
    # Can be expanded in the future to actually send an email.
    email_to = input('+- To: ')
    email_subject = input('+- Subject: ')
    email_body = input('+- Write message:\n\t')
    # Check if the user want to send the email.
    if input(f'+- Send email to {email_to}? (Y/N): ').lower() == 'y':
        print('+- Email sent ------+')
        return True
    else:
        print('+- Draft deleted ------+')

    return False


def mark_as_spam(email_number: int = 0) -> None:
    """
    Mark an email as spam.
    :param email_number: Position/index in the inbox list of the email.
    :return: None
    """
    # Check if the index is available (it can also be done with try-except).
    if email_number >= len(inbox):
        print(f'This email does not exists. Please select an email between 0 and {len(inbox) - 1}.')

    else:
        # Set email to spam = True.
        inbox[email_number].mark_as_spam()
        print(f'+-- Email from {inbox[email_number].from_address} marked as spam.')


def count_unread_emails_and_spam() -> list:
    """
    Count the number of unread emails and spam emails currently in the inbox.
    :return: Number of unread emails, Number of spam emails in a list.
    """
    unread, spam = 0, 0
    for i in range(len(inbox)):
        # Add 1 to the unread number if has_been_read is False.
        unread += 1 if not inbox[i].check_read_status() else 0
        # Add 1 to the spam number if it is marked as spam.
        spam += 1 if inbox[i].check_spam_status() else 0

    return [unread, spam]


def get_unread_emails() -> list:
    """
    Generate a list (print) of all unread emails.
    :return: List of unread emails.
    """
    unread_list = []
    for i in range(len(inbox)):
        # If it is unread, retrieve the email.
        if not inbox[i].check_read_status():
            unread_list.append(inbox[i])

    return unread_list


def get_spam_emails() -> list:
    """
    Generate a list (print) of all spam emails.
    :return: List of spam emails.
    """
    spam_list = []
    for i in range(len(inbox)):
        # If it is spam, retrieve the email.
        if inbox[i].check_spam_status():
            spam_list.append(inbox[i])

    return spam_list


if __name__ == '__main__':
    print('+----------------- Email Platform -----------------+')
    inbox = [
        Email('hello@gmail.com', 'Many, many things.\n I want to say.\n Better not!.'),
        Email('someone@gmail.com', 'More things.\n Already said.'),
        Email('fakefake@spam.com', 'You are a winner!\n Yes, you are!.'),
        Email('bank_weird@bankbank.com', 'Send your login details please.')
    ]

    user_choice = ''

    while user_choice != 'quit':
        # Note the function returns a list [number of unread, number of spam].
        status_emails = count_unread_emails_and_spam()
        print(f'\n\n+--- Status ---+')
        print(f'+ Inbox:    {get_count()} -+')
        print(f'+   Unread: {status_emails[0]} -+')
        print(f'+   Spam:   {status_emails[1]} -+')
        print(f'+---- ---- ----+')

        # Gather the choice, lower is used to allow upper and lower case answers.
        user_choice = input(f'+- What would you like to do?\n{MENU}').lower()
        if user_choice == 'read':
            try:
                # try-except to prevent issues whilst using cast into int.
                email_selected = int(input('\n+ Select the email you want to read (number): '))
                assert email_selected >= 0, 'Please input a positive number.'

            except ValueError:
                print('Please only input a number equal or higher than 0.')

            except AssertionError:
                # This will prevent the program to stop if assert is triggered.
                pass

            else:
                get_email(email_selected)

        elif user_choice == 'mark spam':
            try:
                # try-except to prevent issues whilst using cast into int.
                email_selected = int(input('\n+ Select the email you want to mark as spam (number): '))
                assert email_selected >= 0, 'Please input a positive number.'

            except ValueError:
                print('Please only input a number equal or higher than 0.')

            except AssertionError:
                # This will prevent the program to stop if assert is triggered.
                pass

            else:
                mark_as_spam(email_selected)

        elif user_choice == 'send':
            send_email()

        elif user_choice == 'delete':
            try:
                # try-except to prevent issues whilst using cast into int.
                email_selected = int(input('\n+ Select the email you want to delete (number): '))
                assert email_selected >= 0, 'Please input a positive number.'

            except ValueError:
                print('Please only input a number equal or higher than 0.')

            except AssertionError:
                # This will prevent the program to stop if assert is triggered.
                pass

            else:
                delete_email(email_selected)

        elif user_choice == 'add':
            to_whom = input('+- To: ')
            if not to_whom:
                print('+-- Cannot add email. Sender required.')
            else:
                email_body = input('+- Write message:\n\t')
                # Add the email to the inbox
                inbox.append(add_email(content=email_body, sender=to_whom))
                print('+- Email added ------+')

        elif user_choice == 'show unread':
            # Retrieve the list and then tell the user about them.
            unread_emails = get_unread_emails()
            # Logic to show unread emails only if there are any.
            if len(unread_emails) == 0:
                print('+- No emails are unread.')
            else:
                print('+- Unread emails:')
                for i in range(len(unread_emails)):
                    print(f'+ Email position {inbox.index(unread_emails[i])} from {unread_emails[i].from_address}.')
                print('+- Use "read" option to read any of the emails above.')

        elif user_choice == 'show spam':
            # Retrieve the list and then tell the user about them.
            spam_emails = get_spam_emails()
            # Logic to show spam emails only if there are any.
            if len(spam_emails) == 0:
                print('+- No spam emails. Yey!')
            else:
                print('+- Spam emails:')
                for i in range(len(spam_emails)):
                    print(f'+ Email position {inbox.index(spam_emails[i])} from {spam_emails[i].from_address}.')
                print('+- Use "read" option to read any of the emails above.')

        elif user_choice == 'quit':
            print('+- Goodbye')

        else:
            print('+-- Oops - incorrect input')

    print('\n+------------------- Program closed -------------------+')
