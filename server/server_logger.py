import codecs
from datetime import datetime

L_NONE = 0
L_CRITICAL_EVENT = 1
L_NORMAL = 2
L_SPECIFIC = 3


class StdLogger:
    __instance = None

    # 싱글톤
    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance

    # 싱글톤 끝

    def __init__(self, verbose_level: int = 0):
        self.verbose = verbose_level
        self.print_silent = False

    def verbose_check(self, verbose_level: int):
        if verbose_level <= self.verbose:
            return True
        else:
            return False

    def silent(self, toggle: bool):
        self.print_silent = toggle

    def log(self, message: str, verbose_level: int):
        if not self.verbose_check(verbose_level):
            return

        output = '서버 로그 ' + datetime.today().strftime("%Y-%m-%d %H:%M:%S") + ' >> ' + message

        if not self.print_silent:
            print(output)
        return output


class FileLogger(StdLogger):
    __instance = None

    # 싱글톤
    @classmethod
    def __getInstance(cls):
        return cls.__instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance

    # 싱글톤 끝

    def __init__(self, verbose_level: int, buffer_len: int):
        super().__init__(verbose_level)
        super().silent(True)
        self.logfile = 'async_server_log.log'
        self.log_queue = list()
        self.buffer_len = buffer_len

    def push_msg(self, msg: str):
        if len(self.log_queue) + 1 > self.buffer_len:
            self.flush()
            self.log_queue.append(msg)
        else:
            self.log_queue.append(msg)

    def flush(self):
        with codecs.open(self.logfile, 'a', encoding='utf8') as logfile:
            while len(self.log_queue) > 0:
                logfile.write(self.log_queue.pop(0) + '\n')

    def reset(self):
        with open(self.logfile, 'w') as fp:
            fp.seek(0)
            fp.truncate()

    def log(self, message: str, verbose_level: int):
        super_msg = super().log(message, verbose_level)

        if not self.verbose_check(verbose_level):
            return

        self.push_msg(super_msg)

    def get_latest_log(self, num_of_logs: int) -> list:
        result = list()
        for i, log in enumerate(self.log_queue):
            if len(result) > num_of_logs:
                break
            result.append(log)
        return result


def init_std_logger(verbose_level: int = L_NONE):
    StdLogger.instance(verbose_level)


def init_f_logger(verbose_level: int, buffer_len: int):
    FileLogger.instance(verbose_level, buffer_len)


def a_log(msg: str, verbose_level: int = L_NONE):
    std_log(msg, verbose_level)
    f_log(msg, verbose_level)


def std_log(msg: str, verbose_level: int):
    StdLogger.instance().log(msg, verbose_level)


def f_log(msg: str, verbose_level: int):
    FileLogger.instance().log(msg, verbose_level)
