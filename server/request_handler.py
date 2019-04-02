import hashlib
from server.async_database import *
from asyncio import StreamReader, StreamWriter
from server.async_database import *


class RequestHandler:
    def __init__(self):
        self.request = []

    async def Request_Binding(self, request_number):
        # 요청 넘버는 2의 배수로 정한다
        if request_number == 2:
            echo = EchoRequest()
            result = await echo.main()
        elif request_number == 4:
            select = SelectRequest()
            result = await select.main()
        elif request_number == 6:
            pass
        elif request_number == 8:
            pass

        return result


class EchoRequest(RequestHandler):
    def __init__(self):
        super().__init__()

    async def main(self):
        test_query2 = "SELECT student_name from students"
        result = await query_operator(test_query2)
        return result


class SelectRequest(RequestHandler):
    def __init__(self):
        super().__init__()

    async def main(self):
        test_query2 = "SELECT insert_date from students"
        result = await query_operator(test_query2)
        return result


class CreateTableRequest(RequestHandler):
    def __init__(self):
        super().__init__()

    async def main(self):
        result = None
        return result