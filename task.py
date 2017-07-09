import datetime
import csv


class Task():
    def __init__(self, date, title, time_spent, notes):
        self.date = datetime.datetime.strptime(date, '%d/%m/%Y')
        self.title = title
        self.time_spent = int(time_spent)
        self.notes = notes

    def print(self):
        task_output = ("Date: {},\n"
                       "Title: {},\n"
                       "Time Spent: {},\n"
                       "Notes: {}\n")
        print(task_output.format(self.date.strftime('%d/%m/%Y'), self.title,
                                 self.time_spent, self.notes))

    def to_dict(self):
        return {
            'date': self.date.strftime('%d/%m/%Y'),
            'title': self.title,
            'time_spent': str(self.time_spent),
            'notes': self.notes
        }


class TaskManager():
    fieldnames = ['date', 'title', 'time_spent', 'notes']

    def __init__(self, file):
        self.file = file
        with open(file, 'a+') as csvfile:
            csvfile.seek(0)
            if csvfile.read() == '':
                worklog_writer = csv.DictWriter(csvfile,
                                                fieldnames=self.fieldnames)
                worklog_writer.writeheader()

    def delete_task(self, index):
        with open(self.file, 'r') as csvfile:
            rows = list(csv.DictReader(csvfile))
        del rows[index]
        with open(self.file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def edit_task(self, index, new_task):
        with open(self.file, 'r') as csvfile:
            rows = list(csv.DictReader(csvfile))
        rows[index] = new_task.to_dict()
        with open(self.file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(rows)
