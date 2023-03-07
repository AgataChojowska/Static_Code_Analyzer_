import ast
from analyzer.style_errors.style_error_abc import StyleError
from analyzer.file_handler import PythonFiles


class DefaultArgument(StyleError):

    def __init__(self):
        self._error_code = 'S012'
        super().__init__()

    def check(self, file, tree):
        blank_lines_mistakes = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                for def_arg in node.args.defaults:
                    if type(def_arg) in (ast.List, ast.Set, ast.Dict):
                        line_number = node.lineno
                        error_message = self.error_messages[self._error_code].format(file, line_number,
                                                                                     self._error_code)
                        blank_lines_mistakes[error_message] = (
                            PythonFiles.file_name(file), line_number, self._error_code)
        return blank_lines_mistakes

