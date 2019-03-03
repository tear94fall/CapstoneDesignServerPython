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
async def start_transfer():
    message = str(input("내용을 입력하시오."))
    while True:
        await tcp_echo_client(message, loop)


message = 'abcdefghijklmnopqrstuvwxyz'
loop = asyncio.get_event_loop()
loop.run_until_complete(start_transfer())
