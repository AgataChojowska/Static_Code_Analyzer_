import re
from analyzer.style_errors.style_error_abc import StyleError
from analyzer.file_handler import PythonFiles


class ConstructionName(StyleError):

    def __init__(self):
        self._error_code = 'S007'
        super().__init__()

    def check(self, file, lines):
        line_number = 0
        blank_lines_mistakes = {}
        incorrect_name = r' *def {1,}\W|class {1,}\W'
        for line in lines:
            line_number += 1
            if re.match(incorrect_name, line):
                error_message = self.error_messages[self._error_code].format(file, line_number, self._error_code)
                blank_lines_mistakes[error_message] = (PythonFiles.file_name(file), line_number, self._error_code)
        return blank_lines_mistakes

