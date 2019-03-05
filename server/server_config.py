from argparse import ArgumentParser


class ArgsConfig(ArgumentParser):
    __instance = None

    def __init__(self, *args, **kargs):
        ArgumentParser.__init__(self, *args, **kargs)

    @classmethod
    def __getInstance(cls):
        return cls.__instance

    # 직접 instance 메소드를 실행하는 방법
    @classmethod
    def instance(cls, *args, **kargs):
        cls.__instance = cls(*args, **kargs)
        cls.instance = cls.__getInstance
        return cls.__instance


