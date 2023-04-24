"""
This is the main app for the application. It is responsible for
handling the main parts of each functions and serves as the main
controller of the program.

NAME: Hao Wu
SEMESTER: Spring, 2023
"""
import daily_spending_tracker
import view


def handle_list(monthspending: daily_spending_tracker.MonthSpending) -> None:
    """Handle the list command"""
    view.print_list(monthspending)


def handle_new() -> daily_spending_tracker.MonthSpending:
    """handle the establishment of a new monthspending"""
    year, month, new_target = view.get_basic_info()
    return daily_spending_tracker.MonthSpending(year, month, target=new_target)


def handle_add(monthspending=daily_spending_tracker.MonthSpending
               ) -> daily_spending_tracker.MonthSpending:
    """Handles the add function of the program"""
    date, category = view.get_add_day()
    new_day = daily_spending_tracker.DaySpending(date, category)
    return monthspending.add_dayspending(new_day)


def handle_modi(monthspending=daily_spending_tracker.MonthSpending
                ) -> daily_spending_tracker.MonthSpending:
    """Handles the modify function of the program"""
    date = view.get_date()
    print(monthspending.items[date - 1])
    print("How would you like to change? ")
    category = view.get_category()

    modi_day = daily_spending_tracker.DaySpending(date, category)
    monthspending.add_dayspending(modi_day)

    return monthspending


def handle_summary(monthspending=daily_spending_tracker.MonthSpending
                   ) -> None:
    """Handles the summary message"""
    daysrecorded = monthspending.days_recorded()
    print(view.summary(daysrecorded, monthspending.daysinmonth(),
                       monthspending.sum_month(), monthspending.target))


def handle_plot(monthspending=daily_spending_tracker.MonthSpending
                ) -> None:
    """Handles the plot drawing process"""
    view.plot(monthspending)


def handle_load() -> daily_spending_tracker.MonthSpending:
    """Handles the load command"""
    try:
        filename = view.get_filename()
        monthspending = daily_spending_tracker.load_month_from_file(filename)
        view.print_list(monthspending)
        return monthspending
    except FileNotFoundError:
        view.print_error(f"File not found: {filename}")
        return None


def handle_save(monthspending: daily_spending_tracker.MonthSpending) -> None:
    name = view.get_username()
    daily_spending_tracker.save_month_to_file(monthspending, name)


def main():
    """
    This is the main entry point for the application.
    """
    monthspending = None
    view.print_welcome()
    command = view.get_command()
    while command != view.ViewOptions.EXIT:
        if monthspending and command == view.ViewOptions.LIST:
            handle_list(monthspending)
        elif monthspending and command == view.ViewOptions.ADD:
            handle_add(monthspending)
        elif monthspending and command == view.ViewOptions.MODI:
            handle_modi(monthspending)
        elif monthspending and command == view.ViewOptions.SUMMARY:
            handle_summary(monthspending)
        elif monthspending and command == view.ViewOptions.SAVE:
            handle_save(monthspending)
        elif monthspending and command == view.ViewOptions.PLOT:
            handle_plot(monthspending)
        elif command == view.ViewOptions.LOAD:
            monthspending = handle_load()
        elif command == view.ViewOptions.NEW:
            monthspending = handle_new()
        elif command == view.ViewOptions.HELP:
            view.print_menu()
        elif (monthspending is None
              and command != view.ViewOptions.UNKNOWN
              and command != view.ViewOptions.EXIT):
            view.print_error("Make sure to load or create a new list first.")
        else:
            view.print_error(f"Unknown command")
            view.print_menu()
        command = view.get_command()
    if monthspending:
        handle_save(monthspending)
    view.print_goodbye()


if __name__ == "__main__":
    main()
