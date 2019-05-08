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
        request_number = int(request_number)
        # 요청 넘버는 2의 배수로 정한다
        if request_number == 2:
            echo = EchoRequest(self.data_buffer)
            result = await echo.main()

        elif request_number == 4:
            select = LoginRequest(self.data_buffer)
            result = await select.main()

        elif request_number == 6:
            create = CheckRegisterIdRequest(self.data_buffer)
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
        test_query = "SELECT * FROM member;"
        try:
            result = await query_operator(test_query)
            return result
        except:
            result = None
            return result


class LoginRequest(RequestHandler):
    def __init__(self, data_buffer: DataBuffer):
        super().__init__(data_buffer)

    async def main(self):
        temp = self.data_buffer.get_data()
        table_name = "member"
        login_query = "select * from" + " " + table_name

        try:
            result = await query_operator(login_query)
            id = None
            pw = None

            temp = temp.replace("[", "", 1)
            temp = temp.replace("]", "", 1)
            temp = temp.replace(" ", "")
            temp = temp.replace("'", "")
            temp = temp.split(',')

            for i in temp:
                i = i.split('=')
                if (i[0] == "user_id"):
                    id = i[1]
                if (i[0] == "user_pw"):
                    pw = i[1]

            db_id = None
            db_pw = None

            for i in result:
                db_id = i['id']
                db_pw = i['passwd']

                if (id == db_id):
                    if (pw == db_pw):
                        result = "true"
                        return result
                    else:
                        result = "false"
                else:
                    result = "false"

            return result
        except:
            result = "false"
            return result


class CheckRegisterIdRequest(RequestHandler):
    def __init__(self, data_buffer: DataBuffer):
        super().__init__(data_buffer)

    async def main(self):
        temp = self.data_buffer.get_data()
        table_name = "member"
        get_all_id_query = "select id from" + " " + table_name

        try:
            result = await query_operator(get_all_id_query)
            id = None

            temp = temp.replace("[", "", 1)
            temp = temp.replace("]", "", 1)
            temp = temp.replace(" ", "")
            temp = temp.replace("'", "")
            temp = temp.split(',')

            for i in temp:
                i = i.split('=')
                if (i[0] == "user_id"):
                    id = i[1]

            db_id = None

            for i in result:
                db_id = i['id']
                if (id == db_id):
                    result = "true"
                    return result
                else:
                    result = "false"

            return result
        except:
            result = "false"
            return result


# 테이블 생성을 위한 요청
class CreateTableRequest(RequestHandler):
    def __init__(self, data_buffer: DataBuffer):
        super().__init__(data_buffer)

    async def main(self):
        temp = self.data_buffer.get_data()
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
