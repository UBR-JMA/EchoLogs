from OWMatchResult import OWMatchResult
import tkUtil as tk # let a user save or open files, or choose folders for directory.
import jsonUtil # read and write to files using JSON
import osUtil, os # for getting path data 


isDebug = True
screenshotPathFilename = "ScreenshotPath.json"
path_dict = {}
try:
    path_dict = jsonUtil.DictionaryFromFile(screenshotPathFilename)
    if isDebug: print('Path previously picked:\n' + path_dict["SCREENSHOT DIRECTORY"])
except:
    # let the user pick the directory, defaulting to Documents>Overwatch>Screenshots>Overwatch
    defaultPath = (os.path.expanduser('~/Documents') + '/Overwatch/ScreenShots/Overwatch/').replace('\\', '/')
    if isDebug: print('Default path:' + defaultPath)
    directory = tk.SelectDirectory(defaultPath, "Please select the folder where your Overwatch screenshots appear...") + '\\' 

    # Data to be written
    path_dict = {"SCREENSHOT DIRECTORY": directory.replace('/','\\')}
    # save path to file as JSON
    jsonUtil.DictionaryToFile(path_dict, screenshotPathFilename) 
    if isDebug: print(jsonUtil.DictionaryFromFile(screenshotPathFilename))

# switch directory to test directory if in debug mode
if isDebug: directory = os.getcwd() + '\TestData'

# get the most recent file in the directory
filename = osUtil.GetNewestFile(directory)


# OWMatchResult class Implementation
result = OWMatchResult(filename, isDebug)
result.runOCR(isDebug)
result.formatAllOCR(isDebug)
print(result)

