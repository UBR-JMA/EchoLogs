import os, glob

# get most recent file from a provided folder
# https://stackoverflow.com/a/60113327
def GetNewestFile(pathToFile):
    #format the provided file path
    pathToFile = pathToFile.replace('/', '\\')
    if pathToFile[-1] != '\\':
        pathToFile += '\\'
    #get the list of files.
    list_of_files = glob.glob(pathToFile + '*') # * means all if need specific format then *.csv
    return max(list_of_files, key=os.path.getmtime)