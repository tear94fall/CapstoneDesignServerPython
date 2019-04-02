import asyncio
import unittest

from server.async_database import *

loop = asyncio.get_event_loop();

test_query2 = "SELECT * from students"


class UnitTestClass(unittest.TestCase):
    def test_runs(self):
        loop.run_until_complete(query_operator(test_query2))


class DatabaseUnitTest(unittest.TestCase):
    def test_runs(self):
        loop.run_until_complete(query_operator(test_query2))


# unittest를 실행
if __name__ == '__main__':
    unittest.main()
