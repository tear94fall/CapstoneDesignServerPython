import asyncio
import aiofiles
from os.path import exists

HOST = ''
PORT = 9999

#   ===================================================================


async def io_handle(reader, writer):
    data_transferred = 0

    filename = await reader.read(1024)
    filename = filename.decode()

    if not exists(filename):  # 파일이 해당 디렉터리에 존재하지 않으면
        return  # handle()함수를 빠져 나온다.

    print('파일[%s] 전송 시작...' % filename)

    try:
        async with aiofiles.open(filename, mode='rb') as f:
            async for data in f:
                writer.write(data)
            f.close()
            print("close file descriptor")
    except Exception as e:
        return False

#   ===================================================================

def runServer():
    print('++++++파일 서버를 시작++++++')
    print("+++파일 서버를 끝내려면 'Ctrl + C'를 누르세요.")

    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(io_handle, '127.0.0.1', 9999, loop=loop)
    server = loop.run_until_complete(coro)
    loop.run_forever()


runServer()