"""
This is the main view for the application. It is responsible for
displaying the information to the client, and getting input from the client.

NAME: Hao Wu
SEMESTER: Spring, 2023
"""
import daily_spending_tracker
import sys
from typing import Tuple
from daily_spending_tracker import MonthList, make_ordinal

from enum import Enum
from string import punctuation
import matplotlib.pyplot as plt


class ViewOptions(Enum):
    """ The options for the view """
    EXIT = 1
    LIST = 2
    ADD = 3
    MODI = 4
    SUMMARY = 5
    SAVE = 6
    LOAD = 7
    NEW = 8
    PLOT = 9
    UNKNOWN = 10
    HELP = 11


def print_welcome() -> None:
    """ Print the welcome message """
    print('Welcome to the Daily Spending Tracker')
    print('A one step solution to control your spending in lives')
    print("If you are new to us, please type 'help'")
    print('Type "help" to get a list of commands.')
    print()


def print_goodbye() -> None:
    """ Print the goodbye message """
    print('Goodbye. Thank you for using out product')


def print_error(message: str) -> None:
    """ Print an error message
    Args:
        message (str): error message to print
    """
    print(f'Error: {message}', file=sys.stderr)


def print_list(monthspending: daily_spending_tracker.MonthSpending) -> None:
    """ Print out the month spending now
    Args:
        todo_list (TodoList): list to print
    """
    print(monthspending)


def print_menu() -> None:
    """ Print the menu """
    print('Type any of the following commands.')
    print('1. Exit - exit the program. It will save the data if one is loaded')
    print('2. List - list the spending of the\
 month recorded (if one has been loaded)')
    print('3. Add - add a day spending object')
    print('4. MODI - modify a day spending')
    print('5. SUMMARY - make a summary on the spending condition this month')
    print('6. Save - save the list to a file.')
    print('7. Load - load a list from a file.')
    print('8. New - create a new record')
    print('9. Plot - plot the graph on your spending this month')


def get_filename() -> str:
    """ Get the filename from the user
    Returns:
        str: filename
    """
    filename = input('Enter a filename: ').strip()
    if filename.endswith('.csv'):
        return filename
    else:
        print_error('Filename must end with .csv')
        return get_filename()


def get_username() -> str:
    """Get the username from the user to be a part of the filename

    Returns:
        str: with no punctuation"""
    name = input("Enter a username of the file: ").strip()
    if any(char in name for char in punctuation) or ' ' in name:
        print_error('name may not contain punctuation or spaces')
        return get_username()
    else:
        return name


def get_basic_info() -> Tuple[int, str, float]:
    """Get the basic information from the user, it would return
    to this function again if it doesn't work
    return year, month and target"""
    flag_year, flag_month, flag_target = 0, 0, 0
    while flag_year == 0:
        year = input("Please enter the year of the month ")
        try:
            if int(year) > 0:
                flag_year = 1
                year = int(year)
            else:
                print_error("year must be positive interger")
        except (TypeError, ValueError):
            print_error("year must be positive interger")

    while flag_month == 0:
        month = input("Please enter the month\n"
                      f"Month should be {MonthList} ").capitalize()
        if month in MonthList:
            flag_month = 1
        else:
            print_error("Month incorrect")

    while flag_target == 0:
        target = input("Please enter the target of the month ")
        try:
            if float(target) > 0:
                flag_target = 1
                target = float(target)
            else:
                print_error("target must be positive float")
        except (TypeError, ValueError):
            print_error("target must be positive")

    return (year, month, target)


def get_date() -> int:
    """Get the date from the user's input"""
    flag_date = 0
    while flag_date == 0:
        try:
            date = int(input('Enter the date of the month').strip())
            if isinstance(date, int) and 31 >= date >= 1:
                flag_date = 1
            else:
                raise ValueError
        except ValueError:
            print("Incorrect date")
    return date


def get_filename() -> str:
    """ Get the filename from the user
    Returns:
        str: filename
    """
    filename = input('Enter a filename: ').strip()
    if filename.endswith('.csv'):
        return filename
    else:
        print_error('Filename must end with .csv')
        return get_filename()


def get_category() -> dict:
    """Get the dictionary from the users"""
    flag_category = 0
    category = {"food": 0, "entertainment": 0, "other": 0}

    while flag_category == 0:
        try:
            for i in category.keys():
                value = float(input(f"How much did you spend on {i}? "))
                if value >= 0:
                    category[i] = value
                    flag_category = 1
        except (TypeError, ValueError):
            print_error("Wrong input. Must be positive numbers")
            flag_category = 0
    return category


def get_add_day() -> Tuple[int, dict]:
    """ Get the information for adding an item
    Returns:
        tuple: (date, category)
    """

    # get the date
    date = get_date()

    # get the category dictionary
    category = get_category()

    return (date, category)


def get_add_info() -> Tuple[str, str]:
    """ Get the information for adding a todo item
    Returns:
        tuple: (name, description)
    """
    name = input('Enter the name of the item: ').strip()
    description = input('Enter the description \
        of the item (hit return for blank): ').strip()
    return (name, description)


def get_item_query() -> str:
    """ Get the item to query for
    Returns:
        str: item to query for
    """
    return input('Enter the item name or index value: ').strip()


def summary(days_recorded: int, days_in_month: int, total_spending: float,
            target_set: float) -> None:
    """It would print out the message of the summary to the user"""
    gap = abs(total_spending - target_set)
    message = ""
    message += f"There are \
{days_recorded}/{days_in_month} days recorded in this month\n"
    message += f"The total spending of this month is ${total_spending}\n"
    message += f"The target of this month is ${target_set}"
    if target_set < total_spending:
        message += f"You didn't \
reach the goal this month, with the gap of ${gap} from the target"
    else:
        message += f"You are awesome! \
You reach the goal with ${gap} less than the target"
    return message


def plot(monthspending: daily_spending_tracker.MonthSpending) -> None:
    """This function would plot a curve graph with two lines showing that
    whether users have successfully adhered to their spending limits on an
    average of each day.
    """
    # The first line which is the spending in this month
    x1 = []
    y1 = []
    for i in range(monthspending.daysinmonth()):
        x1.append(i + 1)
        if monthspending.items[i] is None:
            y1.append(0)
        else:
            y1.append(monthspending.items[i].sum_day())
    # plotting the points
    plt.plot(x1, y1, label="Actual day spending")

    # The second line which is the average spending in this month
    average_day_target = monthspending.target / monthspending.daysinmonth()
    y2 = [average_day_target] * monthspending.daysinmonth()
    plt.plot(x1, y2, label="Target distributed in each day")

    # naming the x axis
    plt.xlabel('Date')
    # naming the y axis
    plt.ylabel('spending')

    # giving a title to my graph
    plt.title('Actual Spending vs. Target')

    # show a legend on the plot
    plt.legend()
    
    # function to show the plot
    plt.show()


def get_command() -> Tuple[ViewOptions]:
    """ Get the command from the user
    Returns:
       tuple: command
    """
    command = input('What would you like to do? ').strip()
    command = command.lower()
    if command == 'exit' or command == '1':
        return (ViewOptions.EXIT)
    elif command == 'list' or command == '2':
        return (ViewOptions.LIST)
    elif command == 'add' or command == '3':
        return (ViewOptions.ADD)
    elif command == 'modi' or command == '4':
        return (ViewOptions.MODI)
    elif command == 'summary' or command == '5':
        return (ViewOptions.SUMMARY)
    elif command == 'save' or command == '6':
        return (ViewOptions.SAVE)
    elif command == 'load' or command == '7':
        return (ViewOptions.LOAD)
    elif command == 'new' or command == '8':
        return (ViewOptions.NEW)
    elif command == 'plot' or command == '9':
        return (ViewOptions.PLOT)
    elif command == 'help' or command == '11':
        return (ViewOptions.HELP)
    else:
        return (ViewOptions.UNKNOWN)
