# Static_Code_Analyzer_
Python, abc, ast, re, Pytest, GitHub Actions

I created a small static analyzer tool that finds some common stylistic mistakes in Python code. 

Objectives:

1. If a line contains the same stylistic issue several times, the program prints the information only once. 
   However, if a single line has several issues with different types of error codes, they will be printed as a sorted list.
2. The program must obtain input (path to a file or directory to be analyzed) as a command-line argument.
3. If the input path is a directory; the output should contain all Python files from it.
4. Program returns output containing path to the analyzed file, error code and error message, a line number where error occurs.
5. All output lines must be sorted in ascending order according to the file name, line number, and issue code.
6. Non-Python files must be skipped (not analyzed).


Stylistic errors to be addressed:

1. The length of code lines should not exceed a default value of 79 characters or another number if provided by the user.
2. The indentation is not a multiple of four.
3. Unnecessary semicolon after a statement (note that semicolons are acceptable in comments).
4. Less than two spaces before inline comments.
5. TODO found (in comments only and case-insensitive).
6. More than two blank lines preceding a code line (applies to the first non-empty line).
7. Too many spaces after construction_name (def or class).
8. Class name class_name should be written in CamelCase.
9. Function name function_name should be written in snake_case. Functions names may start or end with underscores (__fun, __init__).
10. Argument name arg_name should be written in snake_case.
11. Variable var_name should be written in snake_case.
a) Names of functions, as well as names of variables in the body of a function should be written in snake_case. 
   However, the error message for an invalid function name should be output only when the function is defined. 
   The error message for an invalid variable name should be output only when this variable is assigned a value, 
   not when this variable is used further in the code.
12. The default argument value is mutable.

Example output:

/path/to/file/script.py: Line 5: S010 Argument name 'S' should be snake_case.

/path/to/file/script.py: Line 5: S012 Default argument value is mutable.

/path/to/file/script.py: Line 6: S011 Variable 'VARIABLE' in function should be snake_case.



