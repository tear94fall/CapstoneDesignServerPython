import asyncio
import aiomysql

# 절대 지우지 말것
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


class DataBaseInIt:
    def __init__(self):
        self.conn = None

    async def db_init(self):
        self.conn = await aiomysql.connect(host='127.0.0.1', port=3306,
                                       user='root', password='root1234', db='test', loop=loop)


# insert 전용
async def test_example_execute(query: str):
    try:
        conn = await aiomysql.connect(host='127.0.0.1', port=3306,
                                       user='root', password='root1234', db='test', loop=loop)
        cur = await conn.cursor()
        result = await cur.execute(query)
        await conn.commit()

        conn.close()
        result = "true"
        return result
    except:
        result = "false"
        return result


# 나머지 쿼리
@asyncio.coroutine
def query_operator(query: str):
    conn = yield from aiomysql.connect(host='127.0.0.1', port=3306, user='root', password='root1234', db='test', loop=loop)
    cursor = yield from conn.cursor(aiomysql.DictCursor)
    yield from cursor.execute(query)

    tuple = yield from cursor.fetchall()
    conn.close()
    return tuple
