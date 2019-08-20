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

        # 0번 요청은 사용하지 않는다.
        # 요청 넘버는 2의 배수로 정한다
        if request_number == 0:
            pass

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

        elif request_number == 16:
            insert = GetUserInfo(self.data_buffer)
            result = await insert.main()

        elif request_number == 18:
            insert = GetAllUserInfo(self.data_buffer)
            result = await insert.main()

        elif request_number == 20:
            insert = UpdateUserInfo(self.data_buffer)
            result = await insert.main()

        elif request_number == 22:
            insert = UpdateLastDriveDate(self.data_buffer)
            result = await insert.main()

        elif request_number == 24:
            insert = UpdateAlcoholCount(self.data_buffer)
            result = await insert.main()
            
        elif request_number == 26:
            insert = FindUserId(self.data_buffer)
            result = await insert.main()

        elif request_number == 28:
            insert = FindUserPw(self.data_buffer)
            result = await insert.main()

        return result


'''
현재 EchoRequest 로직에서만 
데이터 버퍼를 이용해 데이터를 처리 하도록함.
차후 생성하는 객체 모두에 다음과 같이 적용 시킬것
'''


# 0번 요청으로 사용하지 않는다
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


# 2번 요청
# 에코 요청으로, 받은 데이터를 그대로 보내준다.
class EchoRequest(RequestHandler):
    def __init__(self, data_buffer: DataBuffer):
        super().__init__(data_buffer)

    async def main(self):
        try:
            result = self.data_buffer.get_data()
            if result:
                return result
            else:
                result = "false"
                return result
        except:
            result = "false"
            return result


# 4번 요청
# 로그인 요청
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


# 6번 요청
# 회원가입시에 아이디 중복 검사를 위한 클래스
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


# 8번 요청
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

            current_time = (datetime.datetime.now()).strftime('%y-%m-%d')
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


# 10번 요청
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


# 12번 요청
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

                # result = result.split(" ")
                # temp1 = result[0]
                temp1 = str(result)
                # temp2 = result[1]

                temp1 = temp1.split("-")
                # temp2 = temp2.split(":")

                ''' 마지막 접속 날짜 '''
                year = int(temp1[0])
                month = int(temp1[1])
                day = int(temp1[2])

                ''' 현재 날짜 '''
                now = datetime.datetime.today()
                now = str(now).split()
                now = str(now[0]).split("-")

                now_year = int(now[0])
                now_month = int(now[1])
                now_day = int(now[2])

                ''' 날짜 연산 시작  '''
                last_access_date = datetime.date(year, month, day)
                now_date = datetime.date(now_year, now_month, now_day)
                delta = now_date - last_access_date

                result = str(delta.days)
                return result
            except:
                result = "false"
                return result
        except:
            result = "false"
            return result


# 14번 요청
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
                # 대문자로 입력했을 경우 소문자로 바꿔준다.

                captcha2_answer = captcha2_answer.lower()

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


# 16번 요청
# 운전 정보를 넘겨주는 클래스
class GetUserInfo(RequestHandler):
    def __init__(self, data_buffer: DataBuffer):
        super().__init__(data_buffer)

    async def main(self):
        temp = self.data_buffer.get_data()

        try:
            userid = None

            temp = temp.replace("[", "", 1)
            temp = temp.replace("]", "", 1)
            temp = temp.replace(" ", "")
            temp = temp.replace("'", "")
            temp = temp.split(',')

            for i in temp:
                i = i.split('=')
                if (i[0] == "userid"):
                    userid = i[1]

            get_userinfo_query="SELECT * FROM MEMBER WHERE id="+"'"+ userid +"';"

            try:
                qeury_result = await query_operator(get_userinfo_query)
                qeury_result = qeury_result[0]

                result = ""

                # 드라이브 횟수, 졸음운전 감지 횟수, 음주운전 감지 횟수, 마지막 운전 날짜
                result += str(str(qeury_result.get('drive_cnt'))+"-")
                result += str(str(qeury_result.get('sleep_detect_cnt'))+"-")
                result += str(str(qeury_result.get('alcohol_detect_cnt'))+"-")

                last_drive_date = str(str(qeury_result.get('last_drive_date')))
                last_drive_date = last_drive_date.split(" ")
                last_drive_date = last_drive_date[0]
                result += last_drive_date.replace("-", "/")

                return result
            except:
                result = "false"
                return result
        except:
            result = "false"
            return result


# 18번 요청
# 사용자의 모든 정보를 넘겨주는 클래스
class GetAllUserInfo(RequestHandler):
    def __init__(self, data_buffer: DataBuffer):
        super().__init__(data_buffer)

    async def main(self):
        temp = self.data_buffer.get_data()

        try:
            userid = None

            temp = temp.replace("[", "", 1)
            temp = temp.replace("]", "", 1)
            temp = temp.replace(" ", "")
            temp = temp.replace("'", "")
            temp = temp.split(',')

            for i in temp:
                i = i.split('=')
                if (i[0] == "userid"):
                    userid = i[1]

            get_all_userinfo_query="SELECT * FROM MEMBER WHERE id="+"'" + userid + "';"

            try:
                qeury_result = await query_operator(get_all_userinfo_query)
                qeury_result = qeury_result[0]

                result = ""

                # 드라이브 횟수, 졸음운전 감지 횟수, 음주운전 감지 횟수, 마지막 운전 날짜
                result += str(str(qeury_result.get('id'))+"-")
                result += str(str(qeury_result.get('passwd'))+"-")
                result += str(str(qeury_result.get('name'))+"-")
                result += str(str(qeury_result.get('tel'))+"-")

                return result
            except:
                result = "false"
                return result
        except:
            result = "false"
            return result


# 20번 요청
# 사용자 정보를 업데이트 하는 클래스
class UpdateUserInfo(RequestHandler):
    def __init__(self, data_buffer: DataBuffer):
        super().__init__(data_buffer)

    async def main(self):
        temp = self.data_buffer.get_data()

        try:
            userid = None
            userpassword = None
            username = None
            usertel = None

            temp = temp.replace("[", "", 1)
            temp = temp.replace("]", "", 1)
            temp = temp.replace(" ", "")
            temp = temp.replace("'", "")
            temp = temp.split(',')

            for i in temp:
                i = i.split('=')
                if (i[0] == "userid"):
                    userid = i[1]
                if (i[0] == "userpassword"):
                    userpassword = i[1]
                if (i[0] == "username"):
                    username = i[1]
                if (i[0] == "usertel"):
                    usertel = i[1]

            get_primary_key ="SELECT * FROM MEMBER WHERE id="+"'" + userid + "';"

            primary_key = None
            try:
                primary_key = await query_operator(get_primary_key)
                primary_key = primary_key[0]
                primary_key = int(primary_key.get('index'))

                update_userinfo_query = "UPDATE member SET `passwd` = "+"'" + str(userpassword) + "'" + " , `name` = "+"'" + str(username) + "'" + " , `tel` = " + "'" + str(usertel) + "'" + " WHERE (`index` = " + "'" + str(primary_key) + "');"
                qeury_result = await update_execute(update_userinfo_query)

                if qeury_result:
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


# 22번 요청
# 마지막 운전 날짜를 업데이트 하는 함수
class UpdateLastDriveDate(RequestHandler):
    def __init__(self, data_buffer: DataBuffer):
        super().__init__(data_buffer)

    async def main(self):
        temp = self.data_buffer.get_data()

        try:
            userid = None

            temp = temp.replace("[", "", 1)
            temp = temp.replace("]", "", 1)
            temp = temp.replace(" ", "")
            temp = temp.replace("'", "")
            temp = temp.split(',')

            for i in temp:
                i = i.split('=')
                if (i[0] == "userid"):
                    userid = i[1]

            get_primary_key ="SELECT * FROM MEMBER WHERE id="+"'" + userid + "';"

            primary_key = None
            try:
                primary_key = await query_operator(get_primary_key)
                temp_result = primary_key
                primary_key = primary_key[0]
                primary_key = int(primary_key.get('index'))

                temp_result = temp_result[0]
                drive_cnt = int(temp_result.get('drive_cnt'))
                drive_cnt += 1

                new_last_drive_date = (datetime.datetime.now()).strftime('%y-%m-%d')

                update_userinfo_query = "UPDATE member SET `drive_cnt` = "+"'" + str(drive_cnt) + "'" + " , `last_drive_date` = "+"'" + str(new_last_drive_date) + "'" + " WHERE (`index` = " + "'" + str(primary_key) + "');"
                qeury_result = await update_execute(update_userinfo_query)

                if qeury_result:
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


# 24번 요청
# 테스트 실패시에 음주운전 횟수 1회 증가 시킴
class UpdateAlcoholCount(RequestHandler):
    def __init__(self, data_buffer: DataBuffer):
        super().__init__(data_buffer)

    async def main(self):
        temp = self.data_buffer.get_data()

        try:
            userid = None

            temp = temp.replace("[", "", 1)
            temp = temp.replace("]", "", 1)
            temp = temp.replace(" ", "")
            temp = temp.replace("'", "")
            temp = temp.split(',')

            for i in temp:
                i = i.split('=')
                if (i[0] == "userid"):
                    userid = i[1]

            get_primary_key ="SELECT * FROM MEMBER WHERE id="+"'" + userid + "';"

            primary_key = None
            try:
                primary_key = await query_operator(get_primary_key)
                temp_result = primary_key
                primary_key = primary_key[0]
                primary_key = int(primary_key.get('index'))

                temp_result = temp_result[0]
                alcohol_detect_count = int(temp_result.get('alcohol_detect_cnt'))
                alcohol_detect_count += 1

                 # update_userinfo_query = "UPDATE member SET `alcohol_detect_cnt` = "+"'" + str(alcohol_detect_count) + "'" + " WHERE (`index` = " + "'" + str(primary_key) + "');"
                update_userinfo_query = "UPDATE `test`.`member` SET `alcohol_detect_cnt` = '" + str(alcohol_detect_count) + "' WHERE(`index` = '" + str(primary_key) + "');"
                qeury_result = await update_execute(update_userinfo_query)

                if qeury_result:
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


# 26번 요청
# 사용자의 아이디를 찾아 반환함
class FindUserId(RequestHandler):
    def __init__(self, data_buffer: DataBuffer):
        super().__init__(data_buffer)

    async def main(self):
        temp = self.data_buffer.get_data()

        try:
            username = None
            usertel = None

            temp = temp.replace("[", "", 1)
            temp = temp.replace("]", "", 1)
            temp = temp.replace(" ", "")
            temp = temp.replace("'", "")
            temp = temp.split(',')

            for i in temp:
                i = i.split('=')
                if (i[0] == "username"):
                    username = i[1]
                if (i[0] == "usertel"):
                    usertel = i[1]

            get_all_userinfo_query = "SELECT * FROM MEMBER WHERE name=" + "'" + username + "'" + " AND tel=" + "'" + usertel + "'" + "; "

            try:
                qeury_result = await query_operator(get_all_userinfo_query)
                qeury_result = qeury_result[0]

                result = ""

                # 보낸 이름과 전화번호가 저장된 이름과 전화번호화 일치하는지 점검
                if username == str(qeury_result.get('name')) and usertel == str(qeury_result.get('tel')):
                    result += str(qeury_result.get('id'))
                else:
                    result += "false"

                return result
            except:
                result = "false"
                return result
        except:
            result = "false"
            return result


# 28번 요청
# 사용자의 비밀번호를 찾아 반환함
class FindUserPw(RequestHandler):
    def __init__(self, data_buffer: DataBuffer):
        super().__init__(data_buffer)

    async def main(self):
        temp = self.data_buffer.get_data()

        try:
            userid = None
            username = None

            temp = temp.replace("[", "", 1)
            temp = temp.replace("]", "", 1)
            temp = temp.replace(" ", "")
            temp = temp.replace("'", "")
            temp = temp.split(',')

            for i in temp:
                i = i.split('=')
                if (i[0] == "userid"):
                    userid = i[1]
                if (i[0] == "username"):
                    username = i[1]

            get_all_userinfo_query = "SELECT * FROM MEMBER WHERE name=" + "'" + username + "'" + " AND id=" + "'" + userid + "'" + "; "

            try:
                qeury_result = await query_operator(get_all_userinfo_query)
                qeury_result = qeury_result[0]

                result = ""

                # 보낸 이름과 전화번호가 저장된 이름과 전화번호화 일치하는지 점검
                if userid == str(qeury_result.get('id')) and username == str(qeury_result.get('name')):
                    result += str(qeury_result.get('passwd'))
                else:
                    result += "false"

                return result
            except:
                result = "false"
                return result
        except:
            result = "false"
            return result