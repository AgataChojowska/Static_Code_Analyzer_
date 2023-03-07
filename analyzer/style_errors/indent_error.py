from analyzer.style_errors.style_error_abc import StyleError
from analyzer.file_handler import PythonFiles


class Indent(StyleError):

    def __init__(self):
        self._error_code = 'S002'
        super().__init__()

    def check(self, file, lines):
        line_number = 0
        indent_mistakes = {}
        for line in lines:
            line_number += 1
            indents = len(line) - len(line.lstrip(' '))
            if indents % 4 != 0:
                error_message = self.error_messages[self._error_code].format(file, line_number, self._error_code)
                indent_mistakes[error_message] = (PythonFiles.file_name(file), line_number, self._error_code)
        return indent_mistakes