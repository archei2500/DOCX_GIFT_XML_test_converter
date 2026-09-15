import codecs
import os
import errno
import shutil
import tarfile

def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def clear_dir(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def drop_files(root_directory, lib, problems, names, name):
    print("Result recording started")
    directory = root_directory + "\\library" 
    if name != None and name != "":
        directory += "_" + name
    make_sure_path_exists(directory)
    clear_dir(directory)
    lib_file = codecs.open(directory + "\\library.xml", "w+", "UTF-8")
    lib_file.write(lib)
    lib_file.close()
    q_i = 0
    new_dir = directory + "\\problem"
    make_sure_path_exists(new_dir)
    clear_dir(new_dir)
    for problem in problems:
        problem_file = codecs.open(new_dir + "\\" + names[q_i] + ".xml", "w+", "UTF-8")
        problem_file.write(problem)
        problem_file.close()
        q_i += 1
    new_dir = directory + "\\policies"
    make_sure_path_exists(new_dir)
    clear_dir(new_dir)
    assets_file = codecs.open(new_dir + "\\assets.json", "w+", "UTF-8")
    assets_file.write("{}")
    assets_file.close()
    make_tarfile(directory + ".tar.gz", directory)
    print("Result recording completed")

