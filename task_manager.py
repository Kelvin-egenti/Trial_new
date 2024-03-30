# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

#=====importing libraries===========
import os
from datetime import datetime, date
from tabulate import tabulate

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]
    
    text_editor = [t.split(";") for t in task_data]
    # print(text_editor)
task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

def reg_user():
    '''Add a new user to the user.txt file'''
    # - Request input of a new username
    while True:
        new_username = input("New Username: ")
        with open("user.txt", "r") as user_file:
            username_data = user_file.read().split("\n")
            username_dict = {}
            for saved_users in username_data:
                username_select, password_select = saved_users.split(';')
                username_dict[username_select] = password_select
            if new_username in username_dict.keys():
                print("This username is in use. Try another.\n\n")
                continue
            else:
                break
        

    # - Request input of a new password
    new_password = input("New Password: ")

    # - Request input of password confirmation.
    confirm_password = input("Confirm Password: ")

    # - Check if the new password and confirmed password are the same.
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password
        
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")


#Fuction to add task
def add_task():
    '''
    Allow a user to add a new task to task.txt file
    Prompt a user for the following: 
    - A username of the person whom the task is assigned to,
    - A title of a task,
    - A description of the task and 
    - the due date of the task.
    '''
    while True:
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        else:
            break
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
        
        

    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")


    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    
    return print("Task successfully added.")


#Function to view all tasks
def view_all():
    '''
    Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling) 
    
    '''

    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
    return print(disp_str)


#Fuction to view individually assigned tasks
def view_mine():
    '''
    Reads the task from task.txt file and prints to the console in the 
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)
    
    '''
    
    header = ["Index", "Title", "Assigned Date", "Due Date", "Description", "Completed"]
    disp_str = [[t["title"], t["assigned_date"].strftime(DATETIME_STRING_FORMAT), t["due_date"].strftime(DATETIME_STRING_FORMAT), t["description"], t["completed"]] for t in task_list if t['username'] == curr_user]
    display_str = [" "]
    for d in disp_str:
        display_str += [d]
   
            
    return print(tabulate(display_str, headers=header, showindex='always', tablefmt='grid'))

def task_editor():
    while True:
        task_select = int(input("\n\nInput a task's index number to edit status or input '-1' to exit: ")) - 1
        if task_select == -2:
            break
        elif task_select not in range(1, len(text_editor)+1):
            print("Please select a valid task number.")
            continue
        
        else:
            edit_menu = input("Update Status:\n\n1) Mark task as 'Completed'.\n\nOr would you like to edit a task?\
                            \n2: Reassign task to a new person.\n3: Change task's due date.\n:")
            

#Checking for the completion status of tasks and the going through menu items
            if text_editor[task_select][5] == "Yes":
                print(f"Task has already been completed by {text_editor[task_select][0]} and cannot be edited")
                continue
            else:
                if edit_menu == "1":
                    text_editor[task_select][5] = "Yes"
                    continue
                elif edit_menu == "2":
                    new_assignee = input("Please enter name of new assignee: ")
                    usernames = [t["username"] for t in task_list]
                    if new_assignee not in usernames:
                        print("This username is not in use. Try another or exit to the main menu to register user.\n\n")
                        continue

#update the text file to reflect new changes
                    else:                                                       
                        text_editor[task_select][0] = new_assignee
                        updated_text = [";".join(t) for t in text_editor]
                        updated_text = "\n".join(updated_text)
                        with open("tasks.txt", "w") as task_file:
                            task_file.write(updated_text)
                        print(f"A new person has been assigned this task: {text_editor[task_select][0]}")
                    continue

#Edit due date for tasks
                elif edit_menu =="3":
                    while True:
                        try:
                            new_due_date = input("Enter new due date of task (YYYY-MM-DD): ")
                            due_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                            text_editor[task_select][3] = due_date_time
                            updated_text = [";".join(t) for t in text_editor]
                            updated_text = "\n".join(updated_text)
                            with open("tasks.txt", "w") as task_file:
                                task_file.write(updated_text)
                            print("A new due date has been set.")

                            break

                        except ValueError:
                            print("Invalid datetime format. Please use the format specified")
                    continue
                else:
                    print(f"Looks like you have selected an invalid number. Try again.")
            continue

def task_overview():

#task counter
    completed_count = 0
    for t in task_list:
        if t["completed"] == "Yes":
            completed_count += 1
    incomplete_count = 0
    for t in task_list:
        if t["completed"] == "No":
            incomplete_count += 1
    overdue_count = 0
    for t in task_list:
        if t["completed"] == "No" and t["due_date"] < t["assigned_date"] :
            overdue_count += 1
    
    incomplete_percent = incomplete_count / len(task_data) * 100
    
    overdue_percent = overdue_count / len(task_data) * 100

#Display table
    task_display = F"\n Here is an overview of tasks to date:\
            \n\nTotal number of Completed Tasks:       \t\t{completed_count}\
            \nTotal number of Uncompleted Tasks:     \t\t{incomplete_count}\
            \nTotal number of Incomplete and Overdue:\t\t{overdue_count}\
            \nPercentage of Incomplete Tasks:        \t\t{incomplete_percent}%\
            \nPercentage of Overdue Tasks:           \t\t{overdue_percent}%"
        
    with open("task_overview.txt", "w") as task_overview:
        task_overview.write(task_display)
    
    return task_display

def user_overview():
    with open("user.txt", "r") as user_file:
        user_info = [u.strip(";") for u in user_file.read().split("\n")]
        user_count = len(user_info)
    users_task_track = len(task_list)
    user_task_count = 0
    user_comp_count = 0
    for t in task_list:
        if t["username"] == {curr_user}:
            user_task_count += 1
            if t["completed"] == False:
                user_comp_count += 1
    user_task_percent = (user_task_count / users_task_track) * 100
    user_comp_percent = (user_comp_count / user_task_count) * 100
    
    user_overview_display = f"USER OVERVIEW: \n\
        Total number of Users Registered:             \t\t{user_count}\n\
        Total number of Tasks Generated and Tracked:  \t\t{users_task_track}\n\
        For Current  User: {curr_user}\
        Total number of tasks assigned:               \t\t{user_task_count}\n\
        Percentage Tasks to Total Tasks:              \t\t{user_task_percent}\n\
        Percentage of Completed tasks for User:       \t\t{user_comp_percent}"
    
    with open("user_overview.txt", "w") as user_overview:
        user_overview.write(user_overview_display)

    return user_overview_display

while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my tasks
gr - Generate All Reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()


    elif menu == 'va':
        view_all()
            


    elif menu == 'vm':
        view_mine()
        print("\n\nHere is a list of tasks that are currently assigned to you.\nWhat would you like to today?")
        task_editor ()

    
    elif menu == "gr":
        print("-" * 80)
        print("-" * 80)
        print(task_overview())
        print("-" * 80)

        print("-" * 80)
        print(user_overview())
        print("-" * 80)
        print("-" * 80)



            
            
            


        

    
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")

        