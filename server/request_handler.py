import hashlib
from server.async_database import *
from asyncio import StreamReader, StreamWriter
from server.async_database import *
import aiomysql
from server.data_buffer import DataBuffer


class RequestHandler:
    def __init__(self, data_buffer: DataBuffer):
        self.request = []
        self.data_buffer = data_buffer

    async def Request_Binding(self, request_number):
        result = None
        # 요청 넘버는 2의 배수로 정한다
        if request_number == 2:
            echo = EchoRequest(self.data_buffer)
            result = await echo.main()

        elif request_number == 4:
            select = DataSelectRequest()
            result = await select.main()

        elif request_number == 6:
            create = CreateTableRequest()
            result = await create.main()

        elif request_number == 8:
            insert = DataInsertRequest()
            result = await insert.main()

        return result


'''
현재 EchoRequest 로직에서만 
데이터 버퍼를 이용해 데이터를 처리 하도록함.
차후 생성하는 객체 모두에 다음과 같이 적용 시킬것
'''


class EchoRequest(RequestHandler):
    def __init__(self, data_buffer: DataBuffer):
        super().__init__(data_buffer)

    async def main(self):
        temp = self.data_buffer.get_data()
        print("data_buffer data is " + temp)
        test_query = "SELECT * FROM students;"
        result = await query_operator(test_query)
        return result


class DataSelectRequest(RequestHandler):
    def __init__(self):
        super().__init__()

    async def main(self):
        select_query = "SELECT insert_date from students"
        result = await query_operator(select_query)
        return result


class CreateTableRequest(RequestHandler):
    def __init__(self):
        super().__init__()

    async def main(self):
        table_create_query = "CREATE TABLE person " \
                             "( _id INT AUTO_INCREMENT, name VARCHAR(32) NOT NULL, " \
                             "belong VARCHAR(12) DEFAULT 'FOO', " \
                             "phone VARCHAR(12), PRIMARY KEY(_id) ) " \
                             "ENGINE=INNODB"
        result = await query_operator(table_create_query)
        return result


class DataInsertRequest(RequestHandler):
    def __init__(self):
        super().__init__()

    async def main(self):
        data_insert_query = "INSERT INTO person (name, belong, phone) VALUES('유재석', 'IDE','01112345678')"

        result = await test_example_execute(data_insert_query)
        return result