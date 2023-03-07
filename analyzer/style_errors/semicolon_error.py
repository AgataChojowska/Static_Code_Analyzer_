from analyzer.style_errors.style_error_abc import StyleError
from analyzer.file_handler import PythonFiles


class Semicolon(StyleError):

    def __init__(self):
        self._error_code = 'S003'
        super().__init__()

    def check(self, file, lines):
        line_number = 0
        semicolon_mistakes = {}
        for line in lines:
            line_number += 1
            if ('#' not in line and (line.endswith(';\n') or line.endswith(';'))) or (
                    '#' in line and ';' in line.split('#')[0]):
                error_message = self.error_messages[self._error_code].format(file, line_number, self._error_code)
                semicolon_mistakes[error_message] = (PythonFiles.file_name(file), line_number, self._error_code)
        return semicolon_mistakes
