import time
from typing import Optional

class ErrorPrinter:
    @staticmethod
    def print(message: str, ecode: Optional[int]=None, className: Optional[str]=None):
        curtime = time.strftime("%X")
        error_str = "[Error] {}".format(curtime)
        if className:
            error_str += " | Class: {}".format(className)
        if ecode:
            error_str += " | ErrorCode: {}".format(ecode)
        
        error_str += " | Message: {}".format(message)
        print(error_str)

if __name__ == '__main__':
    ErrorPrinter.print('123')
    ErrorPrinter.print('123', 404)
    ErrorPrinter.print('123', 404, "Test")