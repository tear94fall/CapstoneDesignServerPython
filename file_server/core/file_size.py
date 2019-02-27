class FileSize:
    def __init__(self, file_size=None):
        self.file_size = file_size

    def file_size_calculate(self, file_size:int):
        file_sign_cnt = 0
        while file_size >= 0:
            if file_size > 1024:
                file_size /= 1024
                file_sign_cnt += 1
            else:
                break

        file_sign = self.file_sign_calculate(file_sign_cnt)
        file_size_list = []
        file_size_list.append(int(file_size))
        file_size_list.append(file_sign)
        return file_size_list

    def file_sign_calculate(self, file_sign_cnt):
        return {
            0: 'Bytes',
            1: 'KB',
            2: 'MB',
            3: 'GB',
            4: 'TB'
        }.get(file_sign_cnt, 0)


if __name__ == "__main__":
    file = FileSize()

    file_size = 1025
    file_size_list = file.file_size_calculate(file_size)
    print(file_size_list[0])
    print(file_size_list[1])