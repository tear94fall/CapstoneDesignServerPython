import asyncio


async def tcp_echo_client(loop) -> bool:
    try:
        print("전송할 데이터를 입력해주세요>>", end="")
        message = str(input())
        if not message:
            print("아무것도 입력되지 않았습니다.")
            return False
        elif message == 'exit':
            return False
    except ValueError as e:
        print(e)
        return False

    try:
        reader, writer = await asyncio.open_connection('localhost', 8888, loop=loop)
        print('데이터를 보냄 : %s ' % message)
        writer.write(message.encode())

        data = await reader.read(100)
        print('데이터를 받아옴 : %s ' % data.decode())
        writer.close()
        return True
    except ConnectionError as error:
        print(error)
        return False


# 비동기 함수를 반복 수행하는 함수
async def main():
    while True:
        checker = await tcp_echo_client(loop)
        if not checker:
            break
    print('socket close')


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
loop.run_forever()