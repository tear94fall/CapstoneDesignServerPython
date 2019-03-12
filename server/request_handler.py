from server.async_server import *
from server.server_logger import a_log
from asyncio import StreamReader as reader, StreamWriter as writer

BUFFER_SIZE = 1024


class DataReadAndWriteRequest:
    def __init__(self):
        pass

    async def main(self):
        pass


class DataReadRequest:
    def __init__(self, client_ip:str):
        self.client_ip_addr = client_ip

    async def main(self):
        print(self.client_ip_addr)

        data = await reader.read(BUFFER_SIZE)
        message = data.decode()
        a_log('클라이언트 %s 로부터 데이터를 받아옴 : %s ' % (self.client_ip_addr, message), L_CRITICAL_EVENT)

        # 데이터를 보냄
        writer.write(data)
        await writer.drain()

        # 소켓 종료
        a_log('소켓 종료', L_CRITICAL_EVENT)
        writer.close()
        return None


class DataWriteRequest:
    def __init__(self):
        pass

    async def main(self):
        message = str(input("전송할 데이터를 입력해주세요"))
        message = message.encode()

        writer.write(message)
        await writer.drain()

        writer.close()

        # 데이터를 보냄
        a_log('클라이언트에게 데이터를  : %s ' % message, L_CRITICAL_EVENT)


async def request_handler(request_number: int, client_ip_addr):
    request_class = None
    if request_number == 1:
        request_class = DataReadRequest(client_ip_addr)

    return await request_class.main()
