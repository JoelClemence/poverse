class LockFileException(BaseException):
    def __init__(self, msg):
        self.msg = msg
