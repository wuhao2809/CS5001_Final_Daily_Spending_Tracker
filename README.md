# CS5001_Final_Daily_Spending_Tracker
This project is called Daily Spending Tracker, which is for the final of CS5001 in NEU. The concept behind this program is straightforward: users establish a target spending amount for the month and input their daily expenditures for each day of the month. The program then generates a plot and messages to indicate whether users have successfully adhered to their spending limits. 

## Features
* Tracks your daily spending and sets your in a month
* Categories the daily spending into three categories: food, entertainment, and other
* The summary of the daily spending so far could be printed on terminal
* A curve plot could be plotted to indicate whether users have successfully adhered to spending limits

## Basic Usage and Introduction
### Basic Usage (menu)
The function of the program is shown in the menu:
```python
    print('Type any of the following commands.')
    print('1. Exit - exit the program. It will save the data if one is loaded')
    print('2. List - list the spending of the month recorded (if one has been loaded)')
    print('3. Add - add a day spending object')
    print('4. MODI - Modify a day spending')
    print('5. SUMMARY - make a summary on the spending condition this month')
    print('6. Save - save the list to a file.')
    print('7. Load - load a list from a file.')
    print('8. New - create a new record')
    print('9. Plot - plot the graph on your spending this month')
```
### Plot the graph through matplotlib
This function would plot a curve graph with two lines showing that whether users have successfully adhered to their spending limits on an average of each day.
The graph is shown below:

The codes are shown below:
```python
def plot(monthspending: daily_spending_tracker.MonthSpending) -> None:
    # The first line which is the spending in this month
    x1 = []
    y1 = []
    for i in range(monthspending.daysinmonth()):
        x1.append(i + 1)
        if monthspending.items[i] == None:
            y1.append(0)
        else:
            y1.append(monthspending.items[i].sum_day())
    # plotting the points
    plt.plot(x1, y1, label = "Actual day spending")

    # The second line which is the average spending in this month
    average_day_target = monthspending.target / monthspending.daysinmonth()
    y2 = [average_day_target] * monthspending.daysinmonth()
    plt.plot(x1, y2, label = "Target distributed in each day")

    # naming the x axis
    plt.xlabel('Date')
    # naming the y axis
    plt.ylabel('spending')

    # giving a title to my graph
    plt.title('Actual Spending vs. Target')

    # function to show the plot
    plt.show()
```




### DaySpending Class
This class handles the spending of a single day, and the basic type of the data should be in the following form: date, dict(category1, spending1, category2, spending2...). It also contains methods that can add or modify the data. The items in the dictionary can be extended in the future.
```python
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
```

### MonthSpending Class
 This class handles the monthly spending of a user. All of the data must be added through this class by users. It contains several methods, which are shown in the following codes:

```python
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
```



