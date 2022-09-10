from email import message
import tkinter as tk
from tkinter import filedialog
# from https://code.activestate.com/recipes/438123-file-tkinter-dialogs/
# ======== Select a directory:
def SelectDirectory(defaultDirectory="/", defaultTitle='Please select a directory'):
    root = tk.Tk()
    dirname = filedialog.askdirectory(parent=root,initialdir=defaultDirectory,title=defaultTitle)
    if len(dirname ) > 0:
        print (f"You chose {0}", dirname)
    return dirname


# ======== Select a file for opening:
def SelectFileForOpening():
    root = tk.Tk()
    file = filedialog.askopenfile(parent=root,mode='rb',title='Choose a file')
    if file != None:
        data = file.read()
        file.close()
        print (f"I got {0} bytes from this file.", len(data))
    return file


# ======== "Save as" dialog:
def SaveAs():
    myFormats = [
        ('Windows Bitmap','*.bmp'),
        ('Portable Network Graphics','*.png'),
        ('JPEG / JFIF','*.jpg'),
        ('CompuServer GIF','*.gif'),
        ]

    root = tk.Tk()
    fileName = filedialog.asksaveasfilename(parent=root,filetypes=myFormats ,title="Save the image as...")
    if len(fileName ) > 0:
        print ("Saving...")
        return True
    print("File not saved.")
    return False