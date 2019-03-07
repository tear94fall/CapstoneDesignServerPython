

'''
 @ File : async_server.py
 @ Name : lim joonsub
 @ Date : 2019.03.04
 @ Brief : server class declaration
 @ Warning :
'''


import asyncio
from asyncio import StreamReader, StreamWriter
from server.server_logger import a_log, L_CRITICAL_EVENT, L_SPECIFIC, L_NORMAL
from server.request_handler import *

BUFFER_SIZE = 512


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
        async_start = asyncio.start_server(self.io_handle, self.address, self.port, loop=self.event_loop)
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

    async def io_handle(self, reader: StreamReader, writer: StreamWriter):
        client_ip_addr = writer.get_extra_info('peername')

        a_log('클라이언트 {0}의 요청 처리 시작'.format(client_ip_addr), L_NORMAL)

        result = await request_handler(1, client_ip_addr)
        result.main()

'''
        # request_handler 연동 테스트 코드
        result = await request_handler(1, client_ip_addr)
        result.main()
        # =====================

        data = await reader.read(BUFFER_SIZE)
        message = data.decode()
        a_log('클라이언트 %r 로부터 데이터를 받아옴 : %s ' % (client_ip_addr, message), L_CRITICAL_EVENT)

        # 데이터를 보냄
        writer.write(data)
        await writer.drain()

        # 소켓 종료
        a_log('소켓 종료', L_CRITICAL_EVENT)
        writer.close()
'''