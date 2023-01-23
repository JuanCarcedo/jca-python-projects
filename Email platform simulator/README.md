# Email Simulator
I used this program as part of an exercise to show a basic structure of an email handler program.  
I know it can be updated using smtplib and a proper password, although I did not include it here.
(maybe in the future will do it).  

## Future (possible) improvements
Code to allow sending emails:  
```python
import smtplib

# Constants
Y_HOST = 'smtp.mail.yahoo.com'  # Change to provider
Y_EMAIL = 'my_email@yahoo.com'  # Your email
Y_PASS = 'my_pass_for_email'  # Keep secret!

def send_email(to_address: str = None, email_body: str = None) -> None:
    """
    Send email to someone.
    :param to_address: str. Who will receive your email.
    :param email_body: str. Body of the email.
    :return: None.
    """
    if not to_address or not email_body:
      # Prevent sending empty emails or to no one.
      return
    
    else:
      # Create try-except accordingly.
      with smtplib.SMTP(Y_HOST) as s:
          s.login(Y_EMAIL, Y_PASS)
          s.starttls()
          s.sendmail(from_addr=Y_EMAIL, to_addrs=to_address, msg=email_body)
```

Implement GUI with Tkinter, Kivy or even Django.  
Create a class for email management and clean ```main.py```.

## Instructions
- Create a Fork of the repository (you can access all projects).
- Open your favourite IDE (I use [PyCharm](https://www.jetbrains.com/pycharm/)).
- Check the ***[requirements.txt](https://github.com/JuanCarcedo/jca-python-projects/blob/main/requirements.txt)*** file.  
  - For this project you will not need any specific library.

Note: This is a no-GUI program, therefore you will see the outputs in the console.

## How to use
Run the file ```main.py```.  
A status window will let you know the number of emails (categories) that you currently have.  
Follow the instructions in the terminal (see Example of output for more details).

The main options are:
```
+- What would you like to do?
+ (0) 	add item to inbox
+ (1) 	show unread
+ (2) 	read
+ (3) 	send
+ (4) 	mark spam
+ (5) 	show spam
+ (6) 	delete
+ (99) 	quit
+-- Select: 
```
Input via terminal the action/option you wish to do.  
Note that the system will guide you through the options and fields that you need to input.

Feel free to try weird inputs; the program should handle exceptions well.

### Note:
There is no database. Every time you start the program, it will be fresh from the examples.

## Example of output
Welcome to system:  
```
+----------------- Email Platform -----------------+


+--- Status ---+
+ Inbox:    4 -+
+   Unread: 4 -+
+   Spam:   0 -+
+---- ---- ----+ 
```

Main menu:  
```
+- What would you like to do?
+ (0) 	add item to inbox
+ (1) 	show unread
+ (2) 	read
+ (3) 	send
+ (4) 	mark spam
+ (5) 	show spam
+ (6) 	delete
+ (99) 	quit
+-- Select: 
```

Add email is used to recreate a new email in your inbox:
```
+- From: new_account@madeup.com
+- Write message:
	Hello you! I am a message.
+- Email added ------+ 
```  

Note that, now, the Status is updated:  
```
+--- Status ---+
+ Inbox:    5 -+
+   Unread: 5 -+
+   Spam:   0 -+
+---- ---- ----+
+ ```


Show unread:  
```
+- Unread emails:
+ Email position 0 from hello@gmail.com.
+ Email position 1 from someone@gmail.com.
+ Email position 2 from fakefake@spam.com.
+ Email position 3 from bank_weird@bankbank.com.
+ Email position 4 from new_account@madeup.com.
+- Use "read" option to read any of the emails above.
```
Note ```position x``` is used to access an email.

Read an email:  
```
+ Select the email you want to read (number): 1
+-- Email from someone@gmail.com:
More things.
 Already said.
+- END of email ------+
```

Mark spam:  
Note Spam is now 1. Inbox is still 5.
```
+-- Select: mark spam

+ Select the email you want to mark as spam (number): 3
+-- Email from bank_weird@bankbank.com marked as spam.


+--- Status ---+
+ Inbox:    5 -+
+   Unread: 4 -+
+   Spam:   1 -+
+---- ---- ----+
```

Send email:  
```
+-- Select: send
+- To: new_friend@gmail.com
+- Subject: Happy day!
+- Write message:
	I wish you a happy day. Best regards,
+- Send email to new_friend@gmail.com? (Y/N): y
+- Email sent ------+
```

## Author and Licence
**[Juan Carcedo](https://github.com/JuanCarcedo)**  
2022 Copyright © - Licence [MIT](https://github.com/JuanCarcedo/jca-python-projects/blob/main/LICENSE.txt)
