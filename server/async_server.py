

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
from server.data_buffer import *

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
        self.DataBuffer = None
        a_log('서버 설정 완료', L_SPECIFIC)

    def start(self):
        async_start = asyncio.start_server(self.loop_handler, self.address, self.port, loop=self.event_loop)
        server = self.event_loop.run_until_complete(async_start)
        socket_info = server.sockets[0].getsockname()
        ip_addr = socket_info[0]
        port_number = socket_info[1]
        a_log('서버 서비스 시작 중. IP 주소: %s, 포트 번호: %s ' %(ip_addr, port_number), L_CRITICAL_EVENT)
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
        data_buffer = DataBuffer()

        '''
        클라이언트의 처리는 다음과 같이 처리 할것

        1. 클라이언트에서 서버에데이터를 보냄 (데이터 구조는 요청번호와 해당 데이터로 구성 되어있음)
        2. 서버에서 클라이언트의데이터를 받음 (받은 데이터를 요청번호와 처리 데이터로 나눈후 해당 요청 번호에 따라 처리)
        3. 서버에서 클라이언트에게 요청에대한 결과 값을 보냄


        데이터 버퍼 객체에 받은 데이터를 저장한뒤 요청 핸드러에서 클라이언트가 보낸 데이터를 받는다
        '''

        client_ip_addr = writer.get_extra_info('peername')
        a_log('클라이언트 {0}의 요청 처리 시작'.format(client_ip_addr), L_NORMAL)

        try:
            data = await reader.read(SERVER_IO_BUFFER_SIZE)
            if not len(data) > 0:
                a_log('요청 처리 종료. 잘못 된 요청. 요청 클라이언트 {0}'.format(client_ip_addr), L_NORMAL)
                writer.close()
                return

            request_number = None
            str_data = data.decode('utf-8')
            str_data = str_data.replace("{", "", 1)
            str_data = str_data.replace("}", "", 1)
            str_data = str_data.replace(" ", "")
            str_data = str_data.split(',')

            a_log('데이터 송신. 송신 내용 <{0}>. 요청 클라이언트 {1}'.format(str_data, client_ip_addr), L_CRITICAL_EVENT)

            for i in str_data:
                i = i.split('=')
                if i[0] == "request_number":
                    request_number = int(i[1])

            a_log('요청 번호 {0}. 요청 클라이언트 {1}'.format(request_number, client_ip_addr), L_CRITICAL_EVENT)
            data_buffer.set_data(str(str_data))

            requestHandler = RequestHandler(data_buffer)
            result = await requestHandler.Request_Binding(int(request_number))
            result = str(result)
            # 데이터를 보냄
            writer.write(result.encode())

            a_log('데이터 전송. 전송 내용 <{0}>. 요청 클라이언트 {1}'.format(result, client_ip_addr), L_CRITICAL_EVENT)

            # 요청 완료 로그
            a_log('요청처리 완료. 처리 요청 번호 {0}. 요청 클라이언트 {1}'.format(request_number, client_ip_addr), L_CRITICAL_EVENT)

        except ConnectionError as connection_err:
            a_log('요청 처리 실패. 연결 에러. {0}, 요청 클라이언트 {1}'.format(connection_err, client_ip_addr), L_NORMAL)
            writer.close()
        except Exception as unknown_err:
            a_log('요청 처리 실패. 알 수 없는 에러. {0}, 요청 클라이언트 {1}'.format(unknown_err, client_ip_addr), L_NORMAL)

    def get_server_config(self):
        return 'server address :' + str(self.address) + ' port :' + str(self.port)