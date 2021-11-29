from os import listdir
from os.path import isfile, join, isdir

cFiles = []
cLinks = {}

def getAllFilesRecursive(root):
    files = [join(root,f) for f in listdir(root) if isfile(join(root,f))] 
    dirs = [ d for d in listdir(root) if isdir(join(root,d))]
    for d in dirs:
        files_in_d = getAllFilesRecursive(join(root,d))
        if files_in_d:
            for f in files_in_d:
                # if file has a .c or .h extension we should add it
                file_ext = f[-2:]
                files.append(join(root,f))
                if (file_ext == '.c' or file_ext == '.h'):
                   cFiles.append(f)
                   print('$INSTANCE',f[2:],'cFile')
    return files

def getIncludeDependencies(source_files):
    for source_file in source_files:
        try:
            temp_file = open(source_file, 'r')
            try:
                for line in temp_file:
                    if "#include" in line:
                        parts = line.split(" ")
                        dependency = parts[1].strip().split('\t')[0]
                        cLinks[source_file] = dependency[1:-1]
                        print(source_file[2:], dependency[2:-1], 'cLinks')
            except UnicodeDecodeError:
                pass
        except FileNotFoundError:
            pass


getAllFilesRecursive('./postgresql-13.4')

getIncludeDependencies(cFiles)

# print(cLinks)

