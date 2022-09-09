import tkinter as tk
from tkinter import filedialog
# from https://code.activestate.com/recipes/438123-file-tkinter-dialogs/

# ======== Select a directory:
def tkSelectDirectory(initialdir="/",title='Please select a directory'):
    root = tk.Tk()
    dirname = filedialog.askdirectory(root,initialdir,title)
    if len(dirname ) > 0:
        print (f"You chose {0}", dirname)
    return dirname


# ======== Select a file for opening:
def tkSelectFileForOpening(mode='rb',title='Choose a file'):
    root = tk.Tk()
    file = filedialog.askopenfile(root,mode,title)
    if file != None:
        data = file.read()
        file.close()
        print (f"I got {0} bytes from this file.", len(data))
    return file


# ======== "Save as" dialog:
def tkSaveAs(
    myFormats = [
        ('Windows Bitmap','*.bmp'),
        ('Portable Network Graphics','*.png'),
        ('JPEG / JFIF','*.jpg'),
        ('CompuServer GIF','*.gif'),
    ],
    title="Save the image as..."
):

    root = tk.Tk()
    fileName = filedialog.asksaveasfilename(root,myFormats,title)
    if len(fileName ) > 0:
        print ("Saving...")
        return True
    print("File not saved.")
    return False