import re
import ast
from analyzer.style_errors.style_error_abc import StyleError
from analyzer.file_handler import PythonFiles


class ArgumentName(StyleError):

    def __init__(self):
        self._error_code = 'S010'
        super().__init__()

    def check(self, file, tree):
        blank_lines_mistakes = {}
        incorrect_name = r'_?_?[A-Z]+'
        for node in ast.walk(tree):
            if isinstance(node, ast.arg):
                argument_name = node.arg
                if re.match(incorrect_name, argument_name):
                    line_number = node.lineno
                    error_message = self.error_messages[self._error_code].format(file, line_number, self._error_code,
                                                                                 argument_name)
                    blank_lines_mistakes[error_message] = (PythonFiles.file_name(file), line_number, self._error_code)
        return blank_lines_mistakes

