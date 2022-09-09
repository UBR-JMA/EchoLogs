# The goal of this program is to take an array of pixel lengths representing a box
#   Ex: [left, top, right, bottom] or [0,0,1920,1080]
# and turn it into percentages based on a max width/height.

def ratioAsPercent(dimension, maxDimension):
    return round((dimension/maxDimension)*100,2)

def pxToPercent(maxWidth, maxHeight, boxArray):
    return [
        ratioAsPercent(boxArray[0], maxWidth),
        ratioAsPercent(boxArray[1], maxHeight),
        ratioAsPercent(boxArray[2], maxWidth),
        ratioAsPercent(boxArray[3], maxHeight),
    ]

print(pxToPercent(1920, 1980, [61, 53, 155, 69]))