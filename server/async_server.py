

'''
 @ File : async_server.py
 @ Name : lim joonsub
 @ Date : 2019.03.04
 @ Brief : server class declaration
 @ Warning :
'''


import asyncio
from asyncio import StreamReader, StreamWriter
from server.request_handler import *
from server.server_logger import a_log, L_CRITICAL_EVENT, L_SPECIFIC, L_NORMAL
from server.request_handler import *

BUFFER_SIZE = 512
SERVER_IO_BUFFER_SIZE = 512


def _get_transaction_id(data) -> int:
    if not len(data) > 4:
        raise ValueError('invalid data input.')
    header_data = data[0:4]
    return int.from_bytes(header_data, byteorder='little')


class Server:
    def __init__(self, port: int, address: str):
        a_log('서버 설정 시작', L_SPECIFIC)
        self.port = port
        self.address = address
        self.server = None
        self.event_loop = asyncio.get_event_loop()
        self.client_addr = ''
        self.is_server_on = False
        a_log('서버 설정 완료', L_SPECIFIC)

    def start(self):
        async_start = asyncio.start_server(self.loop_handler, self.address, self.port, loop=self.event_loop)
        server = self.event_loop.run_until_complete(async_start)
        addr = server.sockets[0].getsockname()
        a_log('서버 서비스 시작 중 %s ' % str(addr), L_CRITICAL_EVENT)
        self.event_loop.run_forever()
        self.is_server_on = True

    async def stop(self):
        a_log('서버 종료 중', L_CRITICAL_EVENT)
        if not self.is_server_on:
            a_log('서버가 이미 종료 되었습니다.', L_CRITICAL_EVENT)
            raise RuntimeError('server already stopped.')
        self.server.close()
        self.is_server_on = False
        a_log('서버 종료 완료', L_CRITICAL_EVENT)
        await self.server.wait_closed()

    async def loop_handler(self, reader: StreamReader, writer: StreamWriter):
        client_ip_addr = writer.get_extra_info('peername')
        a_log('클라이언트 {0}의 요청 처리 시작'.format(client_ip_addr), L_NORMAL)

        try:
            data = await reader.read(SERVER_IO_BUFFER_SIZE)
        except ConnectionError as connection_err:
            a_log('요청 처리 실패. 연결 에러. {0}, 요청 클라이언트 {1}'.format(connection_err, client_ip_addr), L_NORMAL)
            writer.close()
        except Exception as unknown_err:
            a_log('요청 처리 실패. 알 수 없는 에러. {0}, 요청 클라이언트 {1}'.format(unknown_err, client_ip_addr), L_NORMAL)

        if not len(data) > 0:
            a_log('요청 처리 종료. 잘못 된 요청. 요청 클라이언트 {0}'.format(client_ip_addr), L_NORMAL)
            writer.close()
            return

        request_number = data.decode()
        a_log('요청 번호 {0}. 요청 클라이언트 {1}'.format(request_number, client_ip_addr), L_CRITICAL_EVENT)
        # 데이터를 주고 받는 순서를 확실하게 구분하여
        # 로직을 짤것
        # 로직 추가
        request_number = 8
        requestHandler = RequestHandler()
        result = await requestHandler.Request_Binding(int(request_number))
        a_log('요청처리 완료. 처리 요청 번호 {0}. 요청 클라이언트 {1}'.format(request_number, client_ip_addr), L_CRITICAL_EVENT)
        writer.write(str(result).encode())

    def get_server_config(self):
        return 'server address :' + str(self.address) + ' port :' + str(self.port)