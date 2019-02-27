import socketserver
from os.path import exists
from file_server.core.logger import a_log, L_CRITICAL_EVENT, L_SPECIFIC
from file_server.core.file_size import fileSize


class MyTcpHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data_transferred = 0

        a_log('클라이언트 [%s] 연결됨' % self.client_address[0], L_CRITICAL_EVENT)
        filename = self.request.recv(1024)  # 클라이언트로 부터 파일이름을 전달받음
        filename = filename.decode()  # 파일이름 이진 바이트 스트림 데이터를 일반 문자열로 변환

        if not exists(filename):  # 파일이 해당 디렉터리에 존재하지 않으면
            return  # handle()함수를 빠져 나온다.
        a_log('파일 이름 [%s] 전송 시작...' % filename, L_CRITICAL_EVENT)

        with open(filename, 'rb') as f:
            try:
                data = f.read(1024)  # 파일을 1024바이트 읽음
                while data:  # 파일이 빈 문자열일때까지 반복
                    data_transferred += self.request.send(data)
                    data = f.read(1024)
            except Exception as e:
                print(e)

        file = fileSize()
        file_size_list = file.file_size_calculate(data_transferred)

        a_log('파일 이름 [%s] 전송완료, 전송량 [%s]' % (filename, str(file_size_list[0])+file_size_list[1]), L_CRITICAL_EVENT)



class Server:
    def __init__(self, port, host):
        self.__port = port
        self.__host = host

    def runServer(self):
        a_log('서버 초기화 시작', L_SPECIFIC)

        try:
            server = socketserver.TCPServer((self.__host, self.__port), MyTcpHandler)
            server.serve_forever()
        except KeyboardInterrupt:
            a_log('서버 종료 중....', L_CRITICAL_EVENT)