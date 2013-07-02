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

class CUnzipApp:

  def __init__(self, unzipapp):
    self.window = tk.Frame(unzipapp)
    self.inputframe = tk.Frame(self.window, width = 200, height = 100)
    self.outputframe = tk.Frame(self.window, width = 200, height = 100)
    self.messageframe = tk.Frame(self.window, width = 200, height = 20)

    self.sourcetext = tk.Label(self.inputframe, text='input file: ')
    self.sourcepath = tk.Entry(self.inputframe)
    self.browsesourcefile = tk.Button(self.inputframe, text = 'browse...', command=self.setsourcefile)
    self.loadfile = tk.Button(self.inputframe, text = 'load file', command=self.loadsourcefile)

    self.destinationtext = tk.Label(self.outputframe, text='output path: ')
    self.destinationpath = tk.Entry(self.outputframe)

    self.overwrite = tk.IntVar()
    self.overwritecontent = tk.Checkbutton(self.outputframe, text = 'overwrite', variable=self.overwrite, onvalue=True, offvalue=False)

    self.browsedestinationfile = tk.Button(self.outputframe, text = 'browse...', command=self.setdestinationpath)
    self.writecontent = tk.Button(self.outputframe, text = 'write!', command=self.extracttopath)

    self.messages = tk.StringVar()
    self.processmessages = tk.Message(self.messageframe, anchor='nw', justify='left', width=500, textvariable=self.messages)

    self.window.grid(column=0, row=0)
    self.inputframe.grid(column=0, row=0)
    self.outputframe.grid(column=0, row=1)
    self.messageframe.grid(row=2)

    self.sourcetext.grid(column=0, row=0)
    self.sourcepath.grid(column=1, row=0)
    self.browsesourcefile.grid(column=3, row=0)
    self.loadfile.grid(column=4, row=0)

    self.destinationtext.grid(column=0, row=1)
    self.destinationpath.grid(column=1, row=1)
    self.overwritecontent.grid(column=2, row=1)
    self.browsedestinationfile.grid(column=3, row=1)
    self.writecontent.grid(column=4, row=1)

    self.processmessages.grid(row=2)

    tkMessageBox.showwarning(message="WARNING!\n\nThis app can erase all contents of directories with the 'overwrite' checkbox being marked! Do not use it or use with caution!")

  def setsourcefile(self):
    #print("setsourcefile()")
    filepath = askopenfilename(filetypes = [('ZIP-files', '.zip'), ('All files', '.*')], title = "Pick a ZIP-file")
    print(filepath)
    self.sourcepath.delete(0, last='end')
    self.sourcepath.insert(0, filepath)

  def loadsourcefile(self):
    #print("loadsourcefile()")
    print("Load from:", self.sourcepath.get())
    self.processmessage("Load from:" + str(self.sourcepath.get()))
    # not so nice check for if it is probably a url or local file...
    if (self.sourcepath.get().startswith("http") or self.sourcepath.get().startswith("www")):
      sourcefilepath = self.sourcepath.get()
    else:
      sourcefilepath = "file:" + self.sourcepath.get()
    (source, headers) = urllib.urlretrieve(sourcefilepath, )
    if ( zipfile.is_zipfile(source) == True ):
      print("File is valid ZIP file")
      self.processmessage("File is valid ZIP file")
      self.sourcepath.delete(0, last='end')
      self.sourcepath.insert(0, source)
      print("New source file", source)
      self.processmessage("New source file" + str(source))
    else:
      print("ERROR: File is NOT a valid ZIP file")
      self.processmessage("ERROR: File is NOT a valid ZIP file")

  def setdestinationpath(self):
    #print("setdestinationpath()")
    path = askdirectory(initialdir="/", title="Select a drive or folder")
    print(path)
    self.destinationpath.delete(0, last='end')
    self.destinationpath.insert(0, path)

  def erasepathcontent(self):
    #print("erasepathcontent()")
    for files in os.listdir(self.destinationpath.get()):
      path = os.path.join(self.destinationpath.get(), files)
      try:
        if os.path.isfile(path):
          print("Deleted entry:", path)
          os.unlink(path)
        else:
          shutil.rmtree(path)
          print("Deleted entry:", path)
      except Exception as e:
        print("Exception caught:", e)

  def extracttopath(self):
    #print("extracttopath()")
    if (self.sourcepath.get() != ""):
      self.loadsourcefile()
      if (os.path.isdir(self.destinationpath.get())):
        if (self.overwrite.get() == True):
          question = "Are you sure you want to ! ERASE ! contents of " + str(self.destinationpath.get()) + " ?"
          print("WARNING: no check for illegal content of zip-file!")
          self.processmessage("WARNING: no check for illegal content of zip-file!")
          areyousure = tkMessageBox.askyesno(message=question, icon='question', title='ERASE ALL!?')
          if (areyousure == True):
            print("Overwrite enabled! Erasing contents of:", self.destinationpath.get())
            self.processmessage("Overwrite enabled! Erasing contents of:" + str(self.destinationpath.get()))
            self.erasepathcontent()
            print("Unpacking files...")
            self.processmessage("Unpacking files...")
            myfile = ZipFile(self.sourcepath.get())
            myfile.extractall(self.destinationpath.get())
            print("Done!")
            self.processmessage("Done!")
        else:
          print("Overwrite disabled! Appending to:", self.destinationpath.get())
          print("Unpacking files...")
          myfile = ZipFile(self.sourcepath.get())
          myfile.extractall(self.destinationpath.get())
          print("Done!")
      else:
        print("Destinationpath is not a valid directory")
    else:
      print("Sourcepath is empty")
      self.processmessage("Sourcepath is empty!")

  def processmessage(self, message):
    self.messages.set(message)

root = tk.Tk()
root.title("Unzipapp")
CUnzipApp(root)
root.mainloop()
