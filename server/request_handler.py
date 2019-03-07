from server.async_server import *
from server.server_logger import a_log
from asyncio import StreamReader, StreamWriter

class Request:
    def __init__(self):
        self.data = None

    def set_data(self, data):
        self.data = data

    def get_data(self):
        return self.data

    async def main(self):
        raise NotImplementedError('Command.main() is must be override.')


class RequestHandler:
    def __init__(self):
        pass

    async def __call__(self):
        pass

# ============================================================
    # 요청 처리를 하는 객체들
# ============================================================


class AAA:
    def __init__(self):
        pass

    async def __call__(self):
        pass

    async def main(self):
        await print("aaaaaa")


class BBB:
    def __init__(self):
        pass

    async def __call__(self):
        pass

    async def main(self):
        print("BBB instance")


class DataReaderRequest:
    def __init__(self):
        pass

    async def main(self):
        pass


# 요청 객체 추가시 리스트에 반드시 추가해 주어야함

async def request_handler(request_number: int, client_ip_addr):
    a_log('클라이언트 {0} 의 요청 ID {1} 수행.'.format(client_ip_addr, request_number), L_CRITICAL_EVENT)
    request_list_class = {
        1: AAA(),
        2: BBB(),
        3: DataReaderRequest()
    }

    request_list_name = {
        1: 'AAA',
        2: 'BBB',
        3: 'DataReaderRequest'
    }

    request_class = request_list_class[request_number]
    request_name = request_list_name[request_number]

    a_log('클라이언트 {0} 의 요청 명령 {1} 수행.'.format(client_ip_addr, request_name), L_CRITICAL_EVENT)
    return request_class
