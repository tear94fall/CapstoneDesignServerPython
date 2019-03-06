import asyncio


async def tcp_echo_client(filename, loop):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888,
                                                   loop=loop)

    writer.write(filename.encode())

    data = await reader.read(100)
    print('Received: %r' % data.decode())

    print('Close the socket')
    writer.close()

    # =================================== #
    data_transferred = 0
    data = await reader.read(1024)
    if not data:
        print('파일[%s]: 서버에 존재하지 않거나 전송중 오류발생' % filename)
        return

    with open('download/' + filename, 'wb') as f:
        try:
            while data:
                f.write(data)
                data_transferred += len(data)
                data = await reader.read(1024)
        except Exception as e:
            print(e)

        print('파일[%s] 전송종료. 전송량 [%d]' % (filename, data_transferred))




message = 'Hello World!'
filename = input('다운로드 받은 파일이름을 입력하세요:')
loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(filename, loop))
loop.close()