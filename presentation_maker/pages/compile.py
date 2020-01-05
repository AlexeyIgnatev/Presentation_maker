import os

path = os.getcwd()
path_ui = os.path.join(path, 'ui')
path_py = os.path.join(path, 'py')
for i in os.listdir(path_ui):
    py_file = i[:-2]
    py_file += 'py'
    i = os.path.join(path_ui, i)
    py_file = os.path.join(path_py, py_file)
    os.system('pyuic5 {} -o {}'.format(i, py_file))
