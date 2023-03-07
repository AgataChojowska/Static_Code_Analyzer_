import re
from analyzer.style_errors.style_error_abc import StyleError
from analyzer.file_handler import PythonFiles


class ClassName(StyleError):

    def __init__(self):
        self._error_code = 'S008'
        super().__init__()

    def check(self, file, lines):
        line_number = 0
        blank_lines_mistakes = {}
        incorrect_name = r'class [a-z]|class [A-Z][\w]*[_]'
        for line in lines:
            line_number += 1
            if re.match(incorrect_name, line):
                error_message = self.error_messages[self._error_code].format(file, line_number, self._error_code)
                blank_lines_mistakes[error_message] = (PythonFiles.file_name(file), line_number, self._error_code)
        return blank_lines_mistakes

