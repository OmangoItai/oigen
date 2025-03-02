import sys
import traceback
class OIError(Exception):
    def __init__(self, message):
        self.message = message.strip()
        self.message = '\t' + self.message
        self.message = '\n\t'.join(self.message.split('\n'))
        super().__init__(self.message)
    def __str__(self):
        return self.message

def OIExcepthook(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, OIError):
        tb_list = traceback.extract_tb(exc_traceback)
        if tb_list:
            error_frame = tb_list[0]
            error_location = f'File "{error_frame.filename}", line {error_frame.lineno}, in {error_frame.name}'
        else:
            error_location = "Unknown location"
        print(f"{error_location}\n{exc_value}", file=sys.stderr)
    else:
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

sys.excepthook = OIExcepthook