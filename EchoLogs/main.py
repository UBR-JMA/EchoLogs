from OWMatchResult import OWMatchResult

isDebug = True
folder = 'TestData/' if isDebug else 'RawScreenshot/'
filename = folder + 'Test38.jpg'

# OWMatchResult class Implementation
result = OWMatchResult(filename, isDebug)
result.runOCR(isDebug)
result.formatAllOCR(isDebug)
print(result)

