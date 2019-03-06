import asyncio
from os.path import exists


async def handle_echo(reader, writer):

    filename = await reader.read(1024)
    filename = filename.decode()
    data_transferred = 0

    print("Received File Name %r" % filename)

    if not exists(filename):  # 파일이 해당 디렉터리에 존재하지 않으면
        print("file is not exist")
        return  # handle()함수를 빠져 나온다.

    print('파일[%s] 전송 시작...' % filename)
    with open(filename, 'rb') as f:
        try:
            data = f.read(1024)  # 파일을 1024바이트 읽음
            while data:  # 파일이 빈 문자열일때까지 반복
                writer.write(data)
                data_transferred += len(data)
                data = f.read(1024)
        except Exception as e:
            print(e)

    print('전송완료[%s], 전송량[%d]' % (filename, data_transferred))
    await writer.drain()

    print("Close the client socket")
    writer.close()


loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 8888, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()