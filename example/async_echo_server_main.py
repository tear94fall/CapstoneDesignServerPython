from example.async_echo_server import *
from file_server.core.logger import init_std_logger, init_f_logger
from file_server.core.server_config import ArgsConfig

if __name__ == '__main__':
    description = "서버 작동"
    print(description)

    args = ArgsConfig.instance()
    args.add_argument('--port', type=int, default=8888)
    args.add_argument('--ip', type=str, default='localhost')
    args.add_argument('--verbose', type=int, default=3)

    config = args.parse_args()

    # 로거 초기화
    init_std_logger(verbose_level=config.verbose)
    init_f_logger(verbose_level=config.verbose, buffer_len=10)

    server = Server(config.port, config.ip)
    server.start()