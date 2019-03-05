

'''
 @ File : async_echo_server.py
 @ Name : lim joonsub
 @ Date : 2019.03.04
 @ Brief : server class declaration
 @ Warning :
'''


import asyncio
import ipaddress
from asyncio import StreamReader, StreamWriter
from file_server.core.logger import a_log, L_CRITICAL_EVENT, L_NORMAL, L_SPECIFIC

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
        # =============================================== #
        # 데이터를 연속적으로 받을 거면 루프에 넣어주고
        # 연속적인 전송이 필요없으면 밖으로 빼줄것

        # while True:
        data = await reader.read(BUFFER_SIZE)
        message = data.decode()

        addr = writer.get_extra_info('peername')
        a_log('데이터를 받아옴 : %s ' % message, L_CRITICAL_EVENT)

        # 데이터를 보냄
        writer.write(data)
        await writer.drain()

        # 소켓 종료
        a_log('소켓 종료', L_CRITICAL_EVENT)
        writer.close()