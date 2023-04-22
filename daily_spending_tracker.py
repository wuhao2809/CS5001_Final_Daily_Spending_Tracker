"""
daily_spending_tracker handles multiple daily spending lists, including
reading the information from a file, and writing it to a file.

Classes included: SingleSpending, Spending_tracker
Functions included: load_spending_from_file, save_spending_to_file

NAME: Hao Wu
SEMESTER: Spring 2023
"""
from typing import Optional
import csv
from datetime import datetime
import re
from calendar import monthrange
import random

MonthList = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"
                      "Jul", "Aug", "Sept", "Oct", "Nov", "Dec"]
class DaySpending():
    """This class handles the spending of the single
    day, and the basic type of the data should be in
    the following form:
    date, category1, spending1, category2, spending2...

    it also contains methods that can add, delete or modify
    the data
    """
    def __init__(self, date: int, category: dict={"food": 0,
                 "entertainment": 0, "other": 0}) -> None:
        """

        Args:
            date (str): The date of the data, this date can only
            be set through setter
            category (dict): contains three categories include
            food, entertainment and other
        
        NOTED: A category should have all three keys contained
        """
        try:
            if isinstance(date, int) and 31 >= date >= 1:
                self.__date = date
            else: raise ValueError
        except ValueError:
            raise ValueError("Incorrect date, it should be 1-31")
        self.__category = dict()
        self.__category["food"] = float(category["food"])
        self.__category["entertainment"] = float(category["entertainment"])
        self.__category["other"] = float(category["other"])


    @property
    def date(self) -> str:
        """returns the date of the spending"""
        return self.__date


    @property
    def category(self) -> dict:
        """returns the spending on the food of the day"""
        return self.__category


    @category.setter
    def category(self, new_item: dict) -> None:
        # modify the values of food, entertainment and other
        # in the category.
        for key in new_item:
            if key in self.__category:
                self.__category[key] = new_item[key]
                print(f"{key} has modified to be {self.__category[key]}")

            # find out if other keys exist in new_item, if so, prompt
            # the message to users
            else:
                print(f"{key} is not supported to add in the list")


    def sum_day(self) -> float:
        """Returns the total spending of the day"""
        return sum(self.__category.values())
    
    
    def __str__(self) -> str:
        """returns a string representation of the spending."""
        return f"On {make_ordinal(self.date)}, you spent ${self.category['food']} on food"\
                f" ${self.category['entertainment']} on entertainment,"\
                f"and ${self.category['other']} on others"
    
    
def make_ordinal(n: int) -> str:
    """
    Convert an integer into its ordinal representation::

        make_ordinal(0)   => '0th'
        make_ordinal(3)   => '3rd'
        make_ordinal(122) => '122nd'
        make_ordinal(213) => '213th'
    """
    n = int(n)
    if 11 <= (n % 100) <= 13:
        suffix = 'th'
    else:
        suffix = ['th', 'st', 'nd', 'rd', 'th'][min(n % 10, 4)]
    return str(n) + suffix

class MonthSpending():
    """
    This class handles the monthly spending of a user.
    All of the data must be added through this class by users.
    """
    def __init__(self, year: int, month: str,
                 items=None, target :float = 0) -> None:
        """This class would automatically check if the users enter the
        right month, and it would generate a list with the number of items
        the same of number of days in that particular month.

        Args:
            year (int): _description_
            month (str): _description_
            items (_type_, optional): _description_. Defaults to None.

        Raises:
            TypeError: _description_
        """
        self.__year = year
        
        if month.capitalize() not in MonthList:
            raise TypeError(f"the month you entered must be {MonthList}")
        else:
            self.__month = month
        
        self.__items = (items if items is not None else
        [None] * monthrange(year, MonthList.index(month) + 1)[1])
        
        if target >= 0:
            self.target = target
        else:
            raise ValueError("The target of this month's spending must be positive number")
        

    @property
    def month(self):
        return self.__month
    
    
    @property
    def year(self):
        return self.__year
    
    @property
    def items(self):
        return self.__items
    
    
    def size(self) -> int:
        """returns the size of the list"""
        return len(self.__items)
    
    def daysinmonth(self) -> int:
        """returns the days of the month"""
        return monthrange(self.__year, MonthList.index(self.month) + 1)[1]
    
    
    def days_recorded(self) -> int:
        """returns the number of days being recorded in
        this month
        """
        count = 0
        for i in self.items:
            if i is not None:
                count += 1
        return count
                
        
    def add_dayspending(self, dayspending: DaySpending) -> None:
        """adds an item to the list.
        It should check to make sure the item is a DaySpending object,
        and if not, raise a TypeError.
        """
        if isinstance(dayspending, DaySpending):
            self.__items[dayspending.date - 1] = dayspending
        else:
            raise TypeError("The spending you add is not DaySpending class")
    
    
    # def modi_dayspending(self, dayspending: DaySpending) -> None:
    #     """modify the dayspending.
    #     If the date is incorrect or there has already existed the spending on
    #     that particular, ValueError would be raised.
    #     Args:
    #         dayspending (DaySpending): day_spending on the day
    #     """
    #     date = dayspending.date
    #     if date < 1 or date > self.daysinmonth():
    #         raise ValueError("Incorrect day, must be in range of days in month")
    #     elif not self.items[date - 1]:
    #         raise ValueError("data do not exist, please use add")
    #     elif isinstance(dayspending, DaySpending):
    #         self.__items[date - 1] = dayspending
    #     else:
    #         raise TypeError("The spending you add is not DaySpending class")
            
    def __str__(self) -> str:
        """return the status of each day of the month"""
        message = ""
        message += f"Your target for this month is {self.target}\n"
        for i in range(self.size()):
            if self.items[i] is not None:
                message += f"{str(self.items[i])}\n"
            else:
                message += f"On {make_ordinal(i +1)}, no data\n"
        return message
    
    
    def sum_month(self) -> float:
        """returns the total spending of the month,
        if the spending of some specific days are missed, they
        would be counted as 0"""
        sum = 0.0
        for day in self.items:
            if day:
                sum += day.sum_day()
        return sum

def load_month_from_file(filename: str) -> MonthSpending:
    """this function should read the file specified by filename,
    and return a MonthSpending object. The file will be a CSV file,
    with the following format: 
    first row: year, month
    second row to nth row: date, category
    """
    with open(filename, mode='r') as csvfile:
        filereader = csv.reader(csvfile)
        first_line = next(filereader)
        year, month, new_target = int(first_line[0]), first_line[1], float(first_line[2])
        result = MonthSpending(year, month, target=new_target)
        for row in filereader:
            if row[0] != "None":
                item = DaySpending(int(row[0]), eval(row[1]))
                result.add_dayspending(item)
    return result


def save_month_to_file(month: MonthSpending, name = "New user",) -> None:
    """this function should write the MonthSpending to a file.
    The file name should be the Year and Month, with a .csv extension.
    The format of the file should be the same as the load function,
    writing each property of the ListItem on a separate line.
    """
    with open(f"{name}_{month.year}_{month.month}.csv", mode="w") as csvfile:
        csvwrite = csv.writer(csvfile)
        csvwrite.writerow([month.year, month.month, month.target])

        for item in month.items:
            if item == None:
                csvwrite.writerow(["None"])
            else:
                csvwrite.writerow([f"{item.date}",
                                f"{item.category}"])
    
def main():
    day = DaySpending(30, {"food": 10.5,
                    "entertainment": 20.7, "other": 30.8})
    month = MonthSpending(2023, "Apr", target = 2000)
    
    day2 = DaySpending(5, {"food": 1,
                    "entertainment": 2, "other": 3})
        # Tests if it can add
    for i in range(1, 31):
        day_set = DaySpending(i, {"food": random.random() * 30,
                    "entertainment": random.random() * 30,
                    "other": random.random() * 50})
        month.add_dayspending(day_set)
    # save_month_to_file(month)
    save_month_to_file(month, "wuhao")
    
if __name__ == "__main__":
    main()