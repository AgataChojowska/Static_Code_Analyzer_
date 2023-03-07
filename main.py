import sys
from analyzer.style_errors.long_line_error import LongLine
from analyzer.style_errors.to_do_error import ToDo
from analyzer.style_errors.indent_error import Indent
from analyzer.style_errors.semicolon_error import Semicolon
from analyzer.style_errors.inline_comment_error import InlineComment
from analyzer.style_errors.blank_lines_error import BlankLines
from analyzer.style_errors.construction_name_error import ConstructionName
from analyzer.style_errors.class_name_error import ClassName
from analyzer.style_errors.function_name_error import FunctionName
from analyzer.style_errors.argument_name_error import ArgumentName
from analyzer.style_errors.variable_name_error import VariableName
from analyzer.style_errors.mutable_default_argument_error import DefaultArgument
from analyzer.file_handler import PythonFiles

if __name__ == '__main__':
    args = sys.argv
    if len(args) > 3:
        print('The script should be called with maximum of three arguments.')
        sys.exit(1)

    rules_lines = {
        "to_do": ToDo(),
        "long_lines": LongLine(),
        "indent": Indent(),
        "semicolon": Semicolon(),
        "inline_comment": InlineComment(),
        "blank_lines": BlankLines(),
        "construction_name": ConstructionName(),
        "class_name": ClassName(),
        "function_name": FunctionName()
    }
    rules_trees = {
        "argument_name": ArgumentName(),
        "variable_name": VariableName(),
        "default_argument": DefaultArgument()
    }

    if len(args) == 3:
        try:
            max_chars = int(args[2])
            rules_lines['long_lines'].max_chars = max_chars
        except ValueError as e:
            print(f'ERROR {e}. Leaving default value of {rules_lines["long_lines"].max_chars} chars.')

    style_errors = {}

    INPUT_PATH = args[1]
    path_list = PythonFiles().get_python_files(INPUT_PATH)
    for path in path_list:
        with open(path, 'r', encoding='UTF-8') as f:
            file_lines = f.readlines()
            f.seek(0)
            try:
                file_tree = ast.parse(f.read())
            except SyntaxError as er:
                print('ERROR: File contains syntactic mistakes.')
                sys.exit(1)
            for name, checker in rules_lines.items():
                style_errors.update(checker.check(path, file_lines))
            for name, checker in rules_trees.items():
                style_errors.update(checker.check(path, file_tree))

    FILENAME = 0
    LINE_NUMBER = 1
    ERROR_CODE = 2
    sorted_style_errors = sorted(style_errors.items(),
                                 key=lambda x: (x[1][FILENAME], x[1][LINE_NUMBER], x[1][ERROR_CODE])
                                 )
    for mistake in sorted_style_errors:
        print(mistake[0])
