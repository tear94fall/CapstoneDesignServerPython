import hashlib
from server.async_database import *
from asyncio import StreamReader, StreamWriter
from server.async_database import *
import aiomysql
from server.data_buffer import DataBuffer
import random
import datetime


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
            insert = CreateNewAccount(self.data_buffer)
            result = await insert.main()

        elif request_number == 10:
            insert = GetCaptchaTestSet(self.data_buffer)
            result = await insert.main()

        elif request_number == 12:
            insert = GetLastDriveDate(self.data_buffer)
            result = await insert.main()

        elif request_number == 14:
            insert = GetCaptchaTestSet2(self.data_buffer)
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


# 사용하지 않는다
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


# 새로운 계정 생성 하는 객체
class CreateNewAccount(RequestHandler):
    def __init__(self, data_buffer: DataBuffer):
        super().__init__(data_buffer)

    async def main(self):
        temp = self.data_buffer.get_data()

        try:
            id = None
            passwd = None
            name = None
            tel = None

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
                    passwd = i[1]
                if (i[0] == "user_name"):
                    name = i[1]
                if (i[0] == "user_tel"):
                    tel = i[1]

            current_time = (datetime.datetime.now()).strftime('%y/%m/%d %H:%M:%S')
            create_new_account_query = "INSERT INTO member (id, passwd, name, tel, last_drive_date) " \
                                       "VALUES('" + str(id) + "', '" + str(passwd) + "', '" + str(name) + "', '" + str(tel) + "', '" + current_time + "');"

            '''
            name = "asdfasdf"
            pw = "asdfadf"
            data_insert_query = "INSERT INTO person (userid, passwd) VALUES('" + str(name) + "', '" + str(pw) + "');"
            '''

            try:
                result = await test_example_execute(create_new_account_query)
                return result
            except:
                result = "false"
                return result
            result = "true"
            return result
        except:
            result = "false"
            return result


# 10
# 캡차 문제와 정답을 가져오는 클래스
class GetCaptchaTestSet(RequestHandler):
    def __init__(self, data_buffer: DataBuffer):
        super().__init__(data_buffer)

    async def main(self):
        temp = self.data_buffer.get_data()

        try:
            # 캡챠 문제는 늘릴것 현재는 3번 문제까지 있음
            answer = ""
            test_set_num = random.randrange(1, 100)
            test_set_num %= 9
            # 디비는 1번 부터 시작하므로, +1을 해줘야함
            test_set_num += 1

            check_captcha_answer_query = "SELECT captcha_answer FROM captcha where captcha_num=" + "'" + str(test_set_num) + "';"

            try:
                result = await query_operator(check_captcha_answer_query)
                result = result[0]
                result = result.get('captcha_answer')

                return result
            except:
                result = "false"
                return result

            return result
        except:
            result = "false"
            return result


# 12
# 마지막 운전 날짜를 가져오는 클래스
class GetLastDriveDate(RequestHandler):
    def __init__(self, data_buffer: DataBuffer):
        super().__init__(data_buffer)

    async def main(self):
        temp = self.data_buffer.get_data()

        user_id=None

        temp = temp.replace("[", "", 1)
        temp = temp.replace("]", "", 1)
        temp = temp.replace(" ", "")
        temp = temp.replace("'", "")
        temp = temp.split(',')

        for i in temp:
            i = i.split('=')
        if (i[0] == "user_id"):
            user_id = i[1]

        try:
            query = "SELECT last_drive_date FROM member where id="+"'"+user_id + "';"

            try:
                result = await query_operator(query)
                result = result[0]
                result = result.get('last_drive_date')
                return result
            except:
                result = "false"
                return result
        except:
            result = "false"
            return result


# 14
# 캡차 문제와 정답을 가져오는 클래스
class GetCaptchaTestSet2(RequestHandler):
    def __init__(self, data_buffer: DataBuffer):
        super().__init__(data_buffer)

    async def main(self):
        temp = self.data_buffer.get_data()

        try:
            captcha2_number = None
            captcha2_answer = None

            temp = temp.replace("[", "", 1)
            temp = temp.replace("]", "", 1)
            temp = temp.replace(" ", "")
            temp = temp.replace("'", "")
            temp = temp.split(',')

            for i in temp:
                i = i.split('=')
                if (i[0] == "captcha2_number"):
                    captcha2_number = i[1]
                if (i[0] == "captcha2_answer"):
                    captcha2_answer = i[1]

            # check_captcha_answer_query = "SELECT captcha_answer FROM captcha2 where captcha_num=captcha2_number ;"
            check_captcha_answer_query = "SELECT captcha_answer FROM captcha2 where captcha_num="+"'"+captcha2_number +"';"
            try:
                result = await query_operator(check_captcha_answer_query)
                result = result[0]
                result = result.get('captcha_answer')

                if captcha2_answer == result:
                    result = "true"
                    return result
                else:
                    result = "false"
                    return result
            except:
                result = "false"
                return result
        except:
            result = "false"
            return result
