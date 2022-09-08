from PIL import Image

# get the pixel dimensions of an image.
# Returns a dictionary with height and width keys.

def Open(filename):
    try:
        return Image.open(filename)
    except:
        raise FileNotFoundError(filename)

def GetDimensions(img, isDebug = False):
    width, height = img.size
    dimensions = {'HEIGHT': height, 'WIDTH': width}

    if isDebug:
        print('Image Dimensions: '+ str(width) + 'x' + str(height))

    return dimensions

# TODO: change right and bottom parameters to be addititive rather than inclusive.
# img is of the type that is yielded from the PIL .open() method
# ratios is an array of percentages expressed as integers, not decimals.
#   the percentages in 'ratios' need to be in the following sequence:
#       left, top, right, bottom 
# if isDebug is passed in as 'True',
#   previews of the cropped images will pop up after they have been cropped
def PercentageCrop(img, ratios, isDebug = False):
    # convert integer percents to decimals.
    for index in range(len(ratios)):
        ratios[index] = ratios[index]/100
    # the PIL image.crop functions uses subtractive values to crop for the right and bottom section.
    # convert the right and bottom percents to subtractive.
    ratios[2] = 1 - ratios[2]
    ratios[3] = 1 - ratios[3]
    # use the final ratios to calculate how many pixels to crop.
    w, h = img.size
    ratios[0] = ratios[0]*w
    ratios[1] = ratios[1]*h
    ratios[2] = ratios[2]*w
    ratios[3] = ratios[3]*h
    croppedResultsImg = img.crop((ratios[0], ratios[1], ratios[2], ratios[3]))
    
    if isDebug:
        croppedResultsImg.show()

    return croppedResultsImg