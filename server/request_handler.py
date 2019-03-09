from server.async_server import *
from server.server_logger import a_log
from asyncio import StreamReader as reader, StreamWriter as writer


class QQQ:
    def __init__(self, client_ip):
        self.client_ip_addr = client_ip

    async def main(self):
        result = await request_handler(1, self.client_ip_addr)
        result.main()
        # =====================

        data = await reader.read(BUFFER_SIZE)
        message = data.decode()
        a_log('클라이언트 %s 로부터 데이터를 받아옴 : %s ' % (self.client_ip_addr, message), L_CRITICAL_EVENT)

        # 데이터를 보냄
        writer.write(data)
        await writer.drain()

        # 소켓 종료
        a_log('소켓 종료', L_CRITICAL_EVENT)
        writer.close()


async def request_handler(request_number: int, client_ip_addr):
    # a_log('클라이언트 {0} 의 요청 ID {1} 수행.'.format(client_ip_addr, request_number), L_CRITICAL_EVENT)
    request_list_class = {
        1: QQQ(client_ip_addr)
    }

    request_list_name = {
        1: 'AAA'
    }

    request_class = request_list_class[request_number]
    request_name = request_list_name[request_number]

    #a_log('클라이언트 {0} 의 요청 명령 {1} 수행.'.format(client_ip_addr, request_name), L_CRITICAL_EVENT)
    return await request_class.main()
