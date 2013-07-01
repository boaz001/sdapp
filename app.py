import zipfile
from zipfile import ZipFile
import os
import shutil

try:
  import urllib.request as urllib
except ImportError:
  import urllib as urllib

try:
  import tkinter as tk
except ImportError:
  import Tkinter as tk

try:
  from tkinter import messagebox as tkMessageBox
except ImportError:
  import tkMessageBox as tkMessageBox

try:
  from tkinter.filedialog import askopenfilename
except ImportError:
  from tkFileDialog import askopenfilename
try:
  from tkinter.filedialog import askdirectory
except ImportError:
  from tkFileDialog import askdirectory

unzipapp = tk.Tk()
unzipapp.title("unzipapp")


#def callback():
#    print "click!"
#    print var.get()

#var = tk.IntVar()
#c = tk.Checkbutton(unzipapp, text = "Expand", variable = var)
#c.pack()

# class CUnzipApp:

#     def __init__(self, master):

#         mainframe = tk.Frame(master)
#         mainframe.pack()

#         self.button = tk.Button(mainframe, text="QUIT", fg="red", command=mainframe.quit)
#         self.button.pack(side='left')

#         self.hi_there = tk.Button(mainframe, text="Hello", command=self.say_hi)
#         self.hi_there.pack(side='left')

#     def say_hi(self):
#         print "hi there, everyone!"

# root = tk.Tk()

# app = CUnzipApp(root)

# root.mainloop()
# root.destroy() # optional; see description below

def setsourcefile():
  #print("setsourcefile()")
  filepath = askopenfilename(filetypes = [('ZIP-files', '.zip'), ('All files', '.*')], title = "Pick a ZIP-file")
  print(filepath)
  sourcepath.delete(0, last='end')
  sourcepath.insert(0, filepath)

def loadsourcefile():
  #print("loadsourcefile()")
  print("Load from:", sourcepath.get())
  #urllib.urlcleanup() # clear cache
  (source, headers) = urllib.urlretrieve(sourcepath.get(), )
  if ( zipfile.is_zipfile(source) == True ):
    print("file is valid ZIP file")
    sourcepath.delete(0, last='end')
    sourcepath.insert(0, source)
    print("New source file", source)
  else:
    print("ERROR: File is NOT a valid ZIP file")

def setdestinationpath():
  #print("setdestinationpath()")
  path = askdirectory(initialdir="/", title="Select a drive or folder")
  print(path)
  destinationpath.delete(0, last='end')
  destinationpath.insert(0, path)

def erasepathcontent():
  #print("erasepathcontent()")
  for files in os.listdir(destinationpath.get()):
    path = os.path.join(destinationpath.get(), files)
    try:
      if os.path.isfile(path):
        print("Deleted entry:", path)
        os.unlink(path)
      else:
        shutil.rmtree(path)
        print("Deleted entry:", path)
    except Exception as e:
      print("Exception caught:", e)

def extracttopath():
  #print("extracttopath()")
  if (sourcepath.get() != ""):
    if (os.path.isdir(destinationpath.get())):
      if (overwrite.get() == True):
        question = "Are you sure you want to ! ERASE ! contents of " + str(destinationpath.get()) + " ?"
        print("WARNING: no check for illegal content of zip-file!")
        areyousure = tkMessageBox.askyesno(message=question, icon='question', title='ERASE ALL!?')
        if (areyousure == True):
          print("Overwrite enabled! Erasing contents of:", destinationpath.get())
          erasepathcontent()
          print("Unpacking files...")
          myfile = ZipFile(sourcepath.get())
          myfile.extractall(destinationpath.get())
          print("Done!")
      else:
        print("Overwrite disabled! Appending to:", destinationpath.get())
        print("Unpacking files...")
        myfile = ZipFile(sourcepath.get())
        myfile.extractall(destinationpath.get())
        print("Done!")
    else:
      print("destinationpath is not a directory")
  else:
    print("sourcepath is empty")

print("App is running")

window = tk.Frame(unzipapp)
inputframe = tk.Frame(window, width = 200, height = 100)
outputframe = tk.Frame(window, width = 200, height = 100)
messageframe = tk.Frame(window, width = 200, height = 20)

sourcetext = tk.Label(inputframe, text='input file: ')
sourcepath = tk.Entry(inputframe)
browsesourcefile = tk.Button(inputframe, text = 'browse...', command=setsourcefile)
loadfile = tk.Button(inputframe, text = 'load file', command=loadsourcefile)

destinationtext = tk.Label(outputframe, text='output path: ')
destinationpath = tk.Entry(outputframe)

overwrite = tk.IntVar()
overwritecontent = tk.Checkbutton(outputframe, text = 'overwrite', variable=overwrite, onvalue=True, offvalue=False)

browsedestinationfile = tk.Button(outputframe, text = 'browse...', command=setdestinationpath)
writecontent = tk.Button(outputframe, text = 'write!', command=extracttopath)

processmessages = tk.Message(messageframe, text = 'important message!')

window.grid(column=0, row=0)
inputframe.grid(column=0, row=0)
outputframe.grid(column=0, row=1)
messageframe.grid(column=0, row=2)

sourcetext.grid(column=0, row=0)
sourcepath.grid(column=1, row=0)
browsesourcefile.grid(column=3, row=0)
loadfile.grid(column=4, row=0)

destinationtext.grid(column=0, row=1)
destinationpath.grid(column=1, row=1)
overwritecontent.grid(column=2, row=1)
browsedestinationfile.grid(column=3, row=1)
writecontent.grid(column=4, row=1)

processmessages.grid(column=0, row=2)

unzipapp.mainloop()
