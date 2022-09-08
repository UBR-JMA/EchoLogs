import Util # for helper functions
import PILUtil as Image # for image manipulation
import TesseractUtility as tessUtil # for AI Optical Character Recognition
import OWMetaData as owMeta # for Overwatch hero data
import re # for RegEx string manipulation
import os # for directory, file deletion

# Uses Optical Character Recognition on a screenshot of the tab screen of Overwatch
# Scrapes stats into dictionaries for the purpose of being inserted into a spreadsheet
class OWMatchResult:
    cwd = os.getcwd()
    img = 0
    dimensions = {}
    areas = [
        {'AREA': 'INITIAL'}, 
        {'AREA': 'GENERAL'}, 
        {'AREA': 'HERO'},
        {'AREA': 'UNIQUE'},
    ]


    def __init__(self, filename, isDebug = False):
        self.filename = filename
        if isDebug:
            print('OWMatchResult Object Created with filename: ' + filename)
        # use PIL and the filename to save the image to a local variable
        self.img = Image.Open(self.filename)
        # use PIL to get the image dimensions
        dimensions = Image.GetDimensions(self.img, isDebug)
        self.img = {
            'IMAGE' : self.img,
            'EXTENSION': '.' + filename.split('.')[1], 
            'WIDTH': dimensions['WIDTH'],
            'HEIGHT': dimensions['HEIGHT'],
        }
        if isDebug: print(self.img)
    
    
    # clear out old images before beginning.
    def deleteExistingCropped(self, isDebug):
        # get all the file names to be deleted.
        # the variables for filenames may not be present, so here is a list of expected filenames.
        filenames = ['INITIAL','GENERAL','UNIQUE','HERO','GENERAL0','GENERAL1','GENERAL2']
        for index in range(len(filenames)): 
            filenames[index] = filenames[index] + self.img['EXTENSION']
            try:
                os.remove(filenames[index])
            except:
                if isDebug: print('{0} not found.'.format(filenames[index]))
                continue
        if isDebug: print('Cropped images removed.')

    # save a cropped image object as a file
    def saveCropped(self, index, image, isDebug = False):
        # skip over hero area for OCR.
        index = 3 if index == 2 else index
        newFilename = self.areas[index]['AREA'] + self.img['EXTENSION']
        self.areas[index].update({'FILENAME': newFilename})
        self.areas[index].update({'IMAGE': image})
        image.save(newFilename)
        self.areas[index].update({'OCR': tessUtil.imgToString(newFilename)})
        if isDebug: print(newFilename + ' saved.')

    # awarded medals can mess up OCR, so split the general image into it's parts.
    def granulateGeneralStats(self, generalImage, isDebug = False):
        w = Image.GetDimensions(generalImage)['WIDTH']
        h = Image.GetDimensions(generalImage)['HEIGHT']
        granulatedGeneral = []
        # for each granulated image
        for index in range(0, 3):
            # divide the image into thirds
            img = Image.PercentageCrop(generalImage, [(33.3*index+5), 0, (100-(33.3*(index+1)-2)), 0])
            newFilename = 'GENERAL' + str(index) + self.img['EXTENSION']
            granulatedImage = {}
            granulatedImage.update({'FILENAME': newFilename})
            granulatedImage.update({'IMAGE': img})
            img.save(newFilename)
            granulatedImage.update({'OCR': tessUtil.imgToString(newFilename)})
            granulatedGeneral.append(granulatedImage)
        self.areas[1].update({'GRANULATED IMAGES': granulatedGeneral})

    # crops images into granulated files, then runs OCR on those files.
    def runOCR(self, isDebug = False):
        if isDebug: print('Cropping Images...')
        img = self.img['IMAGE']
        areaImages = [
            #image to crop, [left%, top%, right%, bottom%]
            Image.PercentageCrop(img, [2.5, 2, 70, 92]),  # Map, Mode, and Time
            Image.PercentageCrop(img, [4.5, 82, 56, 6.5]),  # General Scoreboard
            Image.PercentageCrop(img, [48, 76, 35, 18]),  # Hero Name (may not be present)
            Image.PercentageCrop(img, [52, 81, 5, 6]),  # Unique Hero Scoreboard
        ]
        for index in range(len(areaImages)):
            self.saveCropped(index, areaImages[index], isDebug)
        self.granulateGeneralStats(areaImages[1], isDebug)


    # format inital area OCR string into a dictionary
    def formatInitialOCR(self, isDebug):
        # replace new lines with commas
        formatted = self.areas[0]['OCR'].replace('\n', ',')
        # Replace pipe with comma
        formatted = re.sub(r' \| ', ',', formatted)
        # Remove trailing comma
        formatted = re.sub(r',$', '', formatted)
        # Remove 'Time' label
        formatted = re.sub(r'TIME: ', '', formatted)
        
        initialList = formatted.split(',')
        
        #Match the info into a dictionary.
        info = {}
        info.update({'MAP':initialList[0]})
        info.update({'GAME MODE':initialList[1]})
        info.update({'TIME':initialList[2]})
        # Add it to the area dictionary.
        self.areas[0].update({'INFO':info})
        if isDebug: print(self.areas[0]['INFO'])


    # format general area OCR string into a dictionary
    def formatGeneralOCR(self, isDebug):
        formatted = ''
        for image in self.areas[1]['GRANULATED IMAGES']:
            formatted = formatted + image['OCR']
        #remove any commas and any non alphanumeric characters at beginning and end of string
        formatted = re.sub(r'^[^A-Z0-9]+|,+|[^A-Z0-9]+$', '', formatted)
        # replace new lines with commas
        formatted = re.sub(r'\n+', ',', formatted)
        # sometimes Tesseract confuses overwatch zeroes as 'x)' or 'xx)',
        # where x is a couple of random alphanumeric characters. Replace those with 0.
        formatted = re.sub(r'\w+\)(?=,)', '0', formatted)
        # split the formatted string into a last, then swap the keys and values to prep for dictionary.
        formatted = Util.listKeyValueSwap(formatted.split(','))
        # we can't use a for-loop here because the the general images come in top-to-bottom pairs.
        info = {}
        info.update({formatted[0]:formatted[1]})
        info.update({formatted[4]:formatted[5]})
        info.update({formatted[8]:formatted[9]})
        info.update({formatted[2]:formatted[3]})
        info.update({formatted[6]:formatted[7]})
        info.update({formatted[10]:formatted[11]})
        self.areas[1].update({'INFO': info})
        if isDebug: print(self.areas[1]['INFO'])


    # format unique hero scoreboard area OCR string into a dictionary
    def formatUniqueOCR(self, isDebug):
        #remove any commas and any non alphanumeric characters at beginning and end of string
        formatted = re.sub(r'^[^A-Z0-9]+|,|[^A-Z0-9]+$', '', self.areas[3]['OCR'])
        # replace new lines with spaces
        formatted = formatted.replace('\n', ' ')
        # sometimes Tesseract confuses overwatch zeroes as 'x)',
        # where x is a couple of random alphanumeric characters. Replace those with 0.
        formatted = re.sub(r'\S*\)', '0', formatted)
        # replace all don digits with commas
        numbers = re.sub(r'\D+', ',', formatted)
        # remove any non-numbers at the beginning and end of the string.
        numbers = re.sub(r'^\D*|\D*$', '', numbers)
        # its ready to be a dictionary.
        uniqueNumbers = numbers.split(',')

        # find the hero if not provided
        # if self.areas[3]['OCR'] != r'[A-Z]+\n':
        # replace new lines with spaces
        keywords = re.sub(r'\n', ' ', formatted)
        # remove any non ' ', '-', or white space character
        keywords = re.sub(r'[^A-Z- ]+', '', keywords)
        #remove any commas and any non alphanumeric characters at beginning and end of string
        keywords = re.sub(r'^[^A-Z]+|[^A-Z]+$', '', keywords)
        # uniquify spaces
        keywords = re.sub(r'\s+', ' ', keywords)
        # convert keyword string to list of keywords
        keywords = keywords.split(' ')
        # for each hero in meta data
        for hero in owMeta.heroes:
            metaKeywords = []
            # for every stat in their scoreboard
            for index in range(len(hero['SCOREBOARD'])):
                # split it into keywords and add it to a keyword list.
                statKeywords = hero['SCOREBOARD'][index].split()
                for keyword in statKeywords:
                    metaKeywords.append(keyword)
            # for every keyword in the OCR, compare it to the meta data
            numKeywords = len(keywords) if len(keywords) < len(metaKeywords) else len(metaKeywords)
            matches = 0
            for index in range(numKeywords):
                # if there is a match (allowing for plurals 😠): increase the number of matches
                if (
                    metaKeywords[index] == keywords[index] or
                    metaKeywords[index][0:-1] == keywords[index] or 
                    metaKeywords[index] == keywords[index][0:-1]
                ):
                    matches = matches + 1
            # if the number of keywords is equal to the matches
            # we have our hero
            if  matches >= index - 1:
                self.areas[2].update({'INFO': hero})
                break

        # now we have the unique hero stats and the hero, save the data to a dictionary
        info = {}
        scoreboard = []
        try:
            scoreboard = self.areas[2]['INFO']['SCOREBOARD']
        except:
            print('Hero not found')
        for index in range(len(scoreboard)):
            info.update({scoreboard[index]: uniqueNumbers[index]})
        self.areas[3].update({'INFO':info})
        if isDebug: print(self.areas[3]['INFO'])


    # format all the OCR strings into something usable.
    def formatAllOCR(self, isDebug = False):
        # the images aren't needed after OCR has run.
        keepCropped = True
        if not keepCropped: self.deleteExistingCropped(isDebug)
        for area in range(len(self.areas)):
            if area == 0:
                self.formatInitialOCR(isDebug)
            elif area == 1:
                self.formatGeneralOCR(isDebug)
            elif area == 2:
                continue
            elif area == 3:
                self.formatUniqueOCR(isDebug)
            else:
                print('Something went wrong.')
                raise IndexError

    # print override
    def __str__(self):
        result = ''
        for index in range(len(self.areas)):
            try:
                dict = self.areas[index]['INFO']
                for info in dict:
                    result = result + (info.ljust(35, '_') + ':').ljust(37) + dict[info] + '\n'
            except: 
                continue
        return result

