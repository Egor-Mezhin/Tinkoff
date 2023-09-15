import py_compile
import os
import sys

my_file = os.path.abspath(sys.argv[0]) 
my_dir = os.path.dirname(my_file)
db_file = os.path.join(my_dir, "main.py") # Ссылка БД
py_compile.compile(db_file, 'mycode.pyc')
print(1)