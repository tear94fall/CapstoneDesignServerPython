import asyncio
import aiomysql


def num_to_change_attribute(_attribute=None):
    if not _attribute:
        _column = 0

    return {
        0: None,
        1: "id",
        2: "passwd",
        # 추가되는 컬럼은 추가
    }.get(_column, "No selected!")

loop = asyncio.get_event_loop()


# insert 전용
async def test_example_execute(query: str):
    conn = await aiomysql.connect(host='127.0.0.1', port=3306,
                                       user='root', password='root1234', db='test', loop=loop)
    cur = await conn.cursor()
    result = await cur.execute(query)
    await conn.commit()

    conn.close()
    return result


# 나머지 쿼리
@asyncio.coroutine
def query_operator(query: str):
    conn = yield from aiomysql.connect(host='127.0.0.1', port=3306,
                                       user='root', password='root1234', db='test', loop=loop)

    cursor = yield from conn.cursor(aiomysql.DictCursor)
    yield from cursor.execute(query)

    tuple = yield from cursor.fetchall()
    conn.close()
    return tuple


test_query = "CREATE TABLE dept (dept_no INT(11) unsigned NOT NULL,dept_name VARCHAR(32) NOT NULL,PRIMARY KEY (dept_no))"
test_query2 = "SELECT * from students"
test_query3 = "SELECT * from person"


data_insert_query = "INSERT INTO person (name, belong, phone) VALUES('유재석', 'IDE','01112345678')"


# loop.run_until_complete(query_operator(loop, test_query3))
