import asyncio


async def tcp_echo_client(message, loop):
    reader, writer = await asyncio.open_connection('localhost', 8888, loop=loop)

    print('Send: %r' % message)
    writer.write(message.encode())

    data = await reader.read(100)
    print('Received: %r' % data.decode())

    print('Close the socket')
    writer.close()


# 비동기 함수를 반복 수행하는 함수
async def main():
    while True:
        message = str(input())
        message += "\x04"
        await tcp_echo_client(message, loop)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
