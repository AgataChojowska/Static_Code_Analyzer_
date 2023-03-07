from analyzer.style_errors.style_error_abc import StyleError
from analyzer.file_handler import PythonFiles


class InlineComment(StyleError):

    def __init__(self):
        self._error_code = 'S004'
        super().__init__()

    def check(self, file, lines):
        line_number = 0
        comment_mistakes = {}
        for line in lines:
            line_number += 1
            if not line.startswith('#') and '#' in line:
                before_comment = line.split('#')[0]
                if len(before_comment) - len(before_comment.rstrip(' ')) < 2:
                    error_message = self.error_messages[self._error_code].format(file, line_number, self._error_code)
                    comment_mistakes[error_message] = (PythonFiles.file_name(file), line_number, self._error_code)
        return comment_mistakes

