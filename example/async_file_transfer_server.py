import asyncio
import aiofiles
from os.path import exists

HOST = ''
PORT = 9999

#   ===================================================================


async def io_handle(reader, writer):
    data_transferred = 0
    filename = None

    try:
        filename = await reader.read(1024)
        filename = filename.decode()
    except asyncio.IncompleteReadError:
        print(">>파일 이름 전송 실패")

    if not exists(filename):  # 파일이 해당 디렉터리에 존재하지 않으면
        return  # handle()함수를 빠져 나온다.

    print('>>파일[%s] 전송 시작...' % filename)

    try:
        async with aiofiles.open(filename, mode='rb') as f:
            async for data in f:
                writer.write(data)
                data_transferred += len(data)
            f.close()
            print(">>파일 전송 완료")
            print(">>파일 용량: %s" % data_transferred)
    except Exception as e:
        return False

#   ===================================================================


def run_server():
    print(">>서버 초기화 시작")

    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(io_handle, '127.0.0.1', 9999, loop=loop)
    server = loop.run_until_complete(coro)
    loop.run_forever()



run_server()