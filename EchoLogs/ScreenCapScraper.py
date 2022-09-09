import PILUtil as Image # for image manipulation
import TesseractUtility as tessUtil # for AI Optical Character Recognition
import Util # for helper functions
import re # for RegEx string manipulation
import os # for directory, file deletion

# INPUT:
#   A filename or path for a screenshot
#   A Dictionary containing a hierarchy of how a screenshot should be split up
#       Each tuple contains an array of percentages indicating how much should be cropped to yield the desired area.
# OUTPUT:
#   A Dictionary in the same hierarchy, with OCR strings
# PROCESSING:
#   

# Each section is then further divided down to data pairs.
# The data pairs are then split into keys and values.
# Once the screenshot has been completely divided,
#   Run Optical character recognition on all pieces.
#   Save the results of the OCR into a dictionary that matches the hierarchy described above
#       Screenshot > Section > Data Pair > Key/Value

# NOTES & RESOURCES:
# I used this website to get pixel measurements of the screenshot I was working with:
#   https://www.rapidtables.com/web/tools/pixel-ruler.html
#   Which I then plugged into this calculator I made to get percentage values
#       https://www.desmos.com/calculator/m6jcuklddv
#       This is good for vary display sizes where the ratio of the size of the data in the screenshot stays the same.

class ScreenCapScraper:
    def __init__(self, screenshotPath, hierarchyDict):
        self.screenshotPath = screenshotPath
        self.hierarchyDict = hierarchyDict
        self.img = Image.Open(self.screenshotPath)