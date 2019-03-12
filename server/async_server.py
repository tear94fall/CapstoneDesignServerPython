

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
SERVER_IO_BUFFER_SIZE = 512


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
        # 주고 받는 데이터의 구성
        # || 을 기준으로 나눈다
        # 1. 처리해야할 요청의 이름이나 순번
        # 2. 요청할 내용
        # 3. 패딩

        client_ip_addr = writer.get_extra_info('peername')

        a_log('클라이언트 {0}의 요청 처리 시작'.format(client_ip_addr), L_NORMAL)
        
        try:
            data = await reader.read(SERVER_IO_BUFFER_SIZE)
        except ConnectionError as connection_err:
            # a_log('트랜잭션 처리 실패. 연결 에러. {0}, 요청 클라이언트 {1}'.format(connection_err, remote_peer_info), L_NORMAL)
            print("요청 처리 실패. 연걸 에러")
            writer.close()

        if not len(data) > 0:
            # a_log('트랜잭션 처리 종료. 잘못 된 요청. 요청 클라이언트 {0}'.format(remote_peer_info), L_NORMAL)
            print("데이터 없음")
            writer.close()

        message = data.decode()
        message = message.split('||')
        message = message[0]
        a_log('클라이언트 %r 로부터 데이터를 받아옴 : %s ' % (client_ip_addr, message), L_CRITICAL_EVENT)

        # 데이터를 보냄
        writer.write(data)
        await writer.drain()

        # 소켓 종료
        a_log('클라이언트 {0}의 요청 처리 완료'.format(client_ip_addr), L_NORMAL)
        writer.close()