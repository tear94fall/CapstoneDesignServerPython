import asyncio
import aiomysql

loop = asyncio.get_event_loop()


def num_to_change_attribute(_attribute=None):
    if not _attribute:
        _column = 0

    return {
        0: None,
        1: "id",
        2: "passwd",
        # 추가되는 컬럼은 추가
    }.get(_column, "No selected!")


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
