import os

DATA_FOLDER = 'data/'
FILENAME = 'sql_compiled.sql'
FILE_PATH = DATA_FOLDER + FILENAME

def compile_sql():
    try:
        os.remove(FILE_PATH)
    except OSError:
        pass
    result_file = open(FILE_PATH, 'w+')
    compile_files_in_folder('tables', result_file)
    compile_files_in_folder('procedures', result_file)
    result_file.close()

def compile_files_in_folder(folder_name, result_file):
    folder_path = DATA_FOLDER + folder_name + '/'
    result_file.write('--- ' + folder_name.upper() + ' ---' + '\n\n\n')
    for subdir, dirs, files in os.walk(folder_path):
        for file in files:
            if os.path.join(subdir,file) != FILE_PATH:
                print os.path.join(subdir,file)
                f = open(os.path.join(subdir,file))
                data = f.read()
                result_file.write(data)
                result_file.write('\n\n\n')
                f.close()
