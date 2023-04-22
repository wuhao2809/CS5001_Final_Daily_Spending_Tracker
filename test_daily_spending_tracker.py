"""
test_daily_spending_tracker is used to test methods or functions in the
daily_spending_tracker

Classes included: Day_day_spending, Spending_tracker
Functions included: load_spending_from_file, save_spending_to_file

NAME: Hao Wu
SEMESTER: Spring 2023
"""
import unittest
from daily_spending_tracker import DaySpending, MonthSpending, make_ordinal

class TestDaySpending(unittest.TestCase):
    def test_init(self):
        """Tests if the class can assign the initial value to
        the attributes

        This one is specifically test whether it would ignore all the
        other categories except food, entertainment or other.
        """
        day = DaySpending(18, {"food": 10.5,
                 "entertainment": 20.7, "other": 30.8})
        self.assertEqual(day.date, 18)
        self.assertEqual(day.category, {"food": 10.5,
                 "entertainment": 20.7, "other": 30.8})

    def test_init(self):
        """Tests if the class can assign the initial value to
        the attributes

        This one is specifically test whether it would check
        the date can be automatically validate and raise a
        ValueError
        """
        # test the form
        with self.assertRaises(ValueError):
            day = DaySpending(30.3, {"food": 10.5,
                    "entertainment": 20.7, "other": 30.8})

        # test the day
        with self.assertRaises(ValueError):
            day = DaySpending(32, {"food": 10.5,
                    "entertainment": 20.7, "other": 30.8})


    def test_str(self):
        """test the str of the class"""
        message = "On 30th, you spent $10.5 on"\
            " food $20.7 on entertainment,and $30.8 on others"
        day = DaySpending(30, {"food": 10.5,
                    "entertainment": 20.7, "other": 30.8, "hello": 123})
        self.assertEqual(str(day), message)


    def test_category_set(self):
        """test the category.setter of the class"""
        # The test dictionary to be added
        add_dict = {"food": 10.5,
                    "entertainment": 20.7, "other": 30.8, "hello": 123}

        # The final dict after modified
        modi_dict = {"food": 10.5, "entertainment": 20.7, "other": 30.8}

        day = DaySpending(30, {"food": 5,
                    "entertainment": 10, "other": 13, "hello": 123})

        day.category = add_dict
        self.assertEqual(day.category, modi_dict)
    
    
    def test_sum_day(self):
        """tests the sum method"""
        day = DaySpending(30, {"food": 5.1,
                    "entertainment": 0, "other": 13.3})
        sum = 5.1 + 13.3
        self.assertEqual(day.sum_day(), sum)

class Testmakeordinal(unittest.TestCase):
    """Tests make_ordinal"""
    def test_makordinal(self):
        self.assertEqual(make_ordinal(31), "31st")
        self.assertEqual(make_ordinal(3), "3rd")
        self.assertEqual(make_ordinal(1), "1st")
        self.assertEqual(make_ordinal(2), "2nd")
    
    
class TestMonthspending(unittest.TestCase):
    def test_init(self):
        """Tests if the class can assign the initial value to
        the attributes
        """
        day = DaySpending(30, {"food": 10.5,
                    "entertainment": 20.7, "other": 30.8})
        month = MonthSpending(2023, "Apr", day)
        
        self.assertEqual(month.items, day)
        self.assertEqual(month.month, "Apr")

    
    def test_init_default(self):
        """Test the default status of this class"""
        month = MonthSpending(2023, "Apr")
        self.assertEqual(month.items, [None] * 30)
        self.assertEqual(month.month, "Apr")
    
    
    def test_add_dayspending(self):
        """Test if add_dayspending can add and validate the
        input's legality"""
        day = DaySpending(30, {"food": 10.5,
                    "entertainment": 20.7, "other": 30.8})
        month = MonthSpending(2023, "Apr")
        
        # Tests if it can add
        month.add_dayspending(day)
        self.assertEqual(month.items[29], day)
        
        # Tests if it can validate the inputs
        with self.assertRaises(TypeError):
            month.add_dayspending(["This is wrong"])
    
    def test_str_monthspending(self):
        """Tests the str method"""
        message = ""
        message += f"Your target for this month is 50\n"
        for i in range(1, 30):
            message += f"On {make_ordinal(i)}, no data\n"
        message +=("On 30th, you spent $10.5 on food $20.7"
        " on entertainment,and $30.8 on others\n")
        
        # create the test data
        day = DaySpending(30, {"food": 10.5,
                    "entertainment": 20.7, "other": 30.8})
        month = MonthSpending(2023, "Apr", target= 50)
        month.add_dayspending(day)
        
        self.assertEqual(str(month), message)
    
    
    # def test_modi_dayspending_month(self):
    #     """test the modify method in the month"""
    #     day = DaySpending(30, {"food": 10.5,
    #                 "entertainment": 20.7, "other": 30.8})
    #     modi_day_not_exist = DaySpending(5, {"food": 1,
    #                 "entertainment": 1, "other": 1})
    #     modi_day_correct = DaySpending(30, {"food": 1,
    #                 "entertainment": 1, "other": 1})
    #     month = MonthSpending(2023, "Apr")
    #     month.add_dayspending(day)
        
        
    #     # test validation of the item when it is not exist
    #     with self.assertRaises(ValueError):
    #         month.modi_dayspending(modi_day_not_exist)
        
    #     # test validation of the item when it is not correct type
    #     with self.assertRaises(AttributeError):
    #         month.modi_dayspending([])
        
    #     # test whether it can be modified
    #     month.modi_dayspending(modi_day_correct)
    #     self.assertEqual(month.items[29], modi_day_correct)
    
    
    def test_sum_month(self):
        """Tests the sum of the month"""
        day = DaySpending(30, {"food": 10.5,
                    "entertainment": 20.7, "other": 30.8})
        modi_day = DaySpending(29, {"food": 1,
                    "entertainment": 1, "other": 1})
        month = MonthSpending(2023, "Apr")
        month.add_dayspending(day)
        month.add_dayspending(modi_day)
        real_sum = day.sum_day() + modi_day.sum_day()
        
        self.assertEqual(month.sum_month(), real_sum)
        
if __name__ == '__main__':
    unittest.main()