#####################################################
# Work Log Application: Record and Manage tasks
#####################################################

import datetime
import csv
import re
import os

from task import Task, TaskManager


class Worklog:
    fieldnames = ['date', 'title', 'time_spent', 'notes']

    main_prompt = ("WORK LOG\n"
                   "What would you like to do?\n"
                   "a) Add new entry\n"
                   "b) Search in existing entries\n"
                   "c) Quit program\n"
                   "> ")

    task_date_prompt = ("Date of the task\n"
                        "Please use DD/MM/YYYY: ")

    task_title_prompt = "Title of the task: "

    task_time_prompt = "Time spent (rounded to minutes): "

    task_notes_prompt = "Notes (Optional, you can leave this empty): "

    search_type_prompt = ("Do you want to search by:\n"
                          "a) Exact Date\n"
                          "b) Range of Dates\n"
                          "c) Time Spent\n"
                          "d) Exact Search\n"
                          "e) Regex Pattern\n"
                          "f) Return to Menu\n"
                          "> ")

    search_date_prompt = ("Enter the date\n"
                          "Please use DD/MM/YYY: ")

    search_range_of_dates_prompts = [
        "Start date (DD/MM/YYY): ",
        "End date (DD/MM/YYY): "
    ]

    search_time_spent_prompt = "Time spent (rounded to minutes): "

    search_phrase_prompt = 'Enter your phrase: '

    search_regex_prompt = "Enter your regex expression: "

    search_result_prompt = ("[N]ext (Default), [E]dit, [D]elete, [R]eturn to "
                            "search menu\n> ",
                            "[N]ext (Default), [P]revious, [E]dit, [D]elete, "
                            "[R]eturn to search menu\n> ",
                            "[P]revious, [E]dit, [D]elete, [R]eturn to "
                            "search menu (Default)\n> ")

    edit_task_prompt = ("Which attribute do you want to change?\n"
                        "a) Date\n"
                        "b) Title\n"
                        "c) Time Spent\n"
                        "d) Notes\n"
                        "e) Finish\n"
                        "> ")

    def __init__(self, worklog_file_name):
        self.worklog_file_name = worklog_file_name
        self.task_manager = TaskManager(worklog_file_name)

    def run(self):
        while True:
            action = self.get_main_action()
            if action == 'c':
                break
            elif action == 'b':
                self.search_task()
            elif action == 'a':
                self.add_new_task()

    def quit(self):
        pass

    def get_main_action(self):
        """Prompt user to get action, return a or b or c"""
        while True:
            action = input(self.main_prompt).lower()
            if action in ('a', 'b', 'c'):
                return action
            else:
                print('Invalid selection. Please select again.')

    ###################################################
    # Search existing task and related subfunctions
    ###################################################
    def search_task(self):
        while True:
            self.__clear_screen()
            search_type = self.get_search_type()
            self.__clear_screen()
            if search_type == 'a':
                self.search_by_date()
            elif search_type == 'b':
                self.search_by_range_of_dates()
            elif search_type == 'c':
                self.search_by_time_spent()
            elif search_type == 'd':
                self.search_by_exact_phrase()
            elif search_type == 'e':
                self.search_by_regex()
            else:
                return

    def get_search_type(self):
        """Prompt user to get type of search, return a or b or c or d or e
        or f
        """
        while True:
            search_type = input(self.search_type_prompt)
            if search_type in ('a', 'b', 'c', 'd', 'e', 'f'):
                return search_type
            else:
                print('Invalid selection. Please select again.')

    def search_by_regex(self):
        while True:
            pattern = input(self.search_regex_prompt)
            if not pattern.isspace():
                break
            else:
                print("pattern cannot be empty.")

        def match_regex(task):
            return re.match(pattern, task.title) or re.match(pattern,
                                                             task.notes)
        self.__search_and_present_results(criterion=match_regex)

    def search_by_exact_phrase(self):
        while True:
            phrase = input(self.search_phrase_prompt)
            if not phrase.isspace():
                break
            else:
                print("phrase cannot be empty.")

        def contain_phrase(task):
            return phrase in task.title or phrase in task.notes
        self.__search_and_present_results(criterion=contain_phrase)

    def search_by_time_spent(self):
        self.__print_list_of_choices(choice='time_spent')
        time_spent = self.__get_time_spent(self.search_time_spent_prompt)

        def same_time_spent(task):
            return time_spent == task.time_spent
        self.__search_and_present_results(criterion=same_time_spent)

    def search_by_date(self):
        self.__print_list_of_choices(choice='date')
        search_date = self.__get_date(self.search_date_prompt)

        def same_date(task):
            return task.date == search_date
        self.__search_and_present_results(criterion=same_date)

    def search_by_range_of_dates(self):
        self.__print_list_of_choices(choice='date')
        search_start_date = self.__get_date(
            self.search_range_of_dates_prompts[0])
        search_end_date = self.__get_date(
                self.search_range_of_dates_prompts[1])

        def within_date_range(task):
            return search_start_date <= task.date <= search_end_date
        self.__search_and_present_results(criterion=within_date_range)

    ###################################################
    # Add new task and related subfunctions
    ###################################################
    def add_new_task(self):
        date = self.get_task_date()
        title = self.get_task_title()
        time_spent = self.get_task_time_spent()
        notes = input(self.task_notes_prompt)

        self.add_entry(date, title, time_spent, notes)
        # print("Add new entry:")
        # print("date: {}".format(date))
        # print("title: {}".format(title))
        # print("time: {}".format(time))
        # print("notes: {}".format(notes))

    def add_entry(self, date, title, time_spent, notes):
        """Add entry to the work log file
        :param date: datetime object
        :param title: string
        :param time_spent: integer
        :param notes: string
        """
        with open(self.worklog_file_name, 'a') as csvfile:
            worklog_writer = csv.DictWriter(csvfile,
                                            fieldnames=self.fieldnames)
            date_string = date.strftime("%d/%m/%Y")
            worklog_writer.writerow({
                'date': date_string,
                'title': title,
                'time_spent': time_spent,
                'notes': notes
            })
        print("The entry has been added.")

    def get_task_date(self):
        """Prompt user and get task date, return datetime object"""
        return self.__get_date(self.task_date_prompt)

    def get_task_title(self):
        """Prompt user and get task title, return string"""
        return self.__get_title(self.task_title_prompt)

    def get_task_time_spent(self):
        """Prompt user and get task time spent, return as minutes in int"""
        return self.__get_time_spent(self.task_time_prompt)

    ###################################################
    # Utilities
    ###################################################
    def __browse_through_tasks(self, matched_tasks):
        if matched_tasks:
            total_len = len(matched_tasks)
            index = 0
            while index < total_len:
                matched_tasks[index][1].print()
                print('Result {} of {}\n'.format(index + 1, total_len))
                if index == 0:
                    answer = input(self.search_result_prompt[0]).lower()
                elif index != total_len-1:
                    answer = input(self.search_result_prompt[1]).lower()
                else:
                    answer = input(self.search_result_prompt[2]).lower()
                if answer == 'e':
                    self.__edit_task(matched_tasks[index][0], matched_tasks[
                        index][1])
                elif answer == 'd':
                    self.__delete_task(index=matched_tasks[index][0])
                elif answer == 'r':
                    return
                elif answer == 'p':
                    index -= 1
                else:
                    pass  # Next item
                index += 1
        else:
            print("No matched results.")

    def __delete_task(self, index):
        self.task_manager.delete_task(index)
        input("Successfully deleted item. Press any key to return.")

    def __edit_task(self, index, old_task):
        while True:
            answer = input(self.edit_task_prompt)
            if answer == 'e':
                break
            elif answer == 'a':
                new_date = self.__get_date("Enter new date (DD/MM/YYYY): ")
                old_task.date = new_date
            elif answer == 'b':
                new_title = self.__get_title("Enter new title: ")
                old_task.title = new_title
            elif answer == 'c':
                new_time_spent = self.__get_time_spent("Enter new time "
                                                       "spent: ")
                old_task.time_spent = new_time_spent
            elif answer == 'd':
                new_notes = input("Enter new notes: ")
                old_task.notes = new_notes
            self.task_manager.edit_task(index, old_task)

    def __search_and_present_results(self, criterion):
        """Take criterion as a function that return Boolean, search and
        present tasks that match this criterion
        """
        self.__clear_screen()
        with open(self.worklog_file_name, 'r') as csvfile:
            rows = list(csv.DictReader(csvfile))
        tasks = [Task(**row) for row in rows]
        matched_tasks = [(index, task) for (index, task) in enumerate(tasks)
                         if criterion(task)]
        self.__browse_through_tasks(matched_tasks)

    def __get_time_spent(self, prompt):
        while True:
            time = input(prompt)
            try:
                time = int(time)
                assert time >= 0
            except ValueError:
                print("Error: invalid time spent. Please enter again.")
            except AssertionError:
                print("Error: spent time cannot be negative. Please enter "
                      "again.")
            else:
                return time

    def __get_date(self, prompt):
        while True:
            date = input(prompt)
            try:
                date = datetime.datetime.strptime(
                    date, '%d/%m/%Y')
            except ValueError:
                print("Error: {} doesn't seem to be a valid date. Please "
                      "enter again.".format(date))
            else:
                return date

    def __get_title(self, prompt):
        """Prompt user and get task title, return string"""
        while True:
            title = input(prompt)
            if not title.isspace():
                return title
            else:
                print("task title cannot be empty.")

    def __print_list_of_choices(self, choice):
        with open(self.worklog_file_name, 'r') as csvfile:
            rows = list(csv.DictReader(csvfile))
            tasks = [Task(**row) for row in rows]
            if choice == 'date':
                print("Dates: ")
                dates = set([task.date for task in tasks])
                for date in dates:
                    print(date.strftime('%d/%m/%Y'))
            elif choice == 'time_spent':
                print("Time spent: ")
                time_spents = set([task.time_spent for task in tasks])
                for time_spent in time_spents:
                    print("{} minutes".format(time_spent))

    def __clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

def main():
    worklog = Worklog(worklog_file_name='worklog.csv')
    worklog.run()


if __name__ == '__main__':
    main()
