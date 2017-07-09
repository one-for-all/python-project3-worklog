#####################################################
# Test file: Unfinished
# Seems to require mock. Might come to it later
#####################################################

import unittest
import os

from worklog import Worklog


class WorklogTest(unittest.TestCase):
    def setUp(self):
        self.worklog = Worklog(worklog_file_name='test_work_log.csv')

    def test_creation(self):
        test_file_name = 'test_creation.csv'
        os.remove(test_file_name)
        Worklog(worklog_file_name=test_file_name)
        with open(test_file_name, 'r') as file:
            data = file.read()
            self.assertEqual(data, 'date,title,time spent,notes')

    def test_get_task_date(self):
        self.worklog.get_task_date()


if __name__ == '__main__':
    unittest.main()
