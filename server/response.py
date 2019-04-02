

class FailResponse:
    def __init__(self, error_msg):
        self.err_msg = error_msg

    def get_fail_response(self):
        return self.err_msg


class SuccessResponse:
    def __init__(self):
        self.success_response = True

    def get_fail_response(self):
        return self.success_response


class SuccessDataResponse:
    def __init__(self, response_data: str):
        self.data = response_data

    def set_data(self, data):
        self.data = data

    def get_data(self, data):
        return self.data

    def data_size(self):
        return len(self.data)