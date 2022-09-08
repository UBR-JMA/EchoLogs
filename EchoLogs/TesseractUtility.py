import cv2, pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\josha\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'

# Simple image to string
def imgToString(filename):
    return pytesseract.image_to_string(cv2.imread(filename))

# Get verbose data including boxes, confidences, line and page numbers
def printData(filename):
    print(pytesseract.image_to_data(cv2.imread(filename)))

# create a searchable PDF
def getPDF(filename):
    pdf = pytesseract.image_to_pdf_or_hocr(filename, extension='pdf')
    with open('test.pdf', 'w+b') as f:
        f.write(pdf) # pdf type is bytes by default