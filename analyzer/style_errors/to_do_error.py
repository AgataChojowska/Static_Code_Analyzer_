from analyzer.style_errors.style_error_abc import StyleError
from analyzer.file_handler import PythonFiles


class ToDo(StyleError):

    def __init__(self):
        self._error_code = 'S005'
        super().__init__()

    def check(self, file, lines):
        line_number = 0
        to_do_mistakes = {}
        for line in lines:
            line_number += 1
            if '#' in line and 'todo' in line.lower():
                comment = line.split('#')[1].lower()
                if 'todo' in comment:
                    error_message = self.error_messages[self._error_code].format(file, line_number, self._error_code)
                    to_do_mistakes[error_message] = (PythonFiles.file_name(file), line_number, self._error_code)
        return to_do_mistakes

