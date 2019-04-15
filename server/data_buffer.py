import hashlib


class DataBuffer:
    def __init__(self):
        self.data_buffer = None

    def set_data(self, data: str):
        self.data_buffer = data

    def get_data(self):
        return self.data_buffer

    def crypt_data(self):
        self.data_buffer = self.data_buffer.encode('utf-8')
        sha256 = hashlib.sha256()
        sha256.update(self.data_buffer)
        self.data_buffer = sha256.hexdigest()

    def valid_check(sel)->bool:

        return True


if __name__ == "__main__":
    buffer = DataBuffer()
    buffer.set_data("123123123123")
    buffer.crypt_data()
    print("=== end ===")