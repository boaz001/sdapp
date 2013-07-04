# Copyright (C) 2013 Boaz Stolk
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import zipfile
from zipfile import ZipFile
import os
import platform
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
    rClickbinder(self.sourcepath)
    self.browsesourcefile = tk.Button(self.inputframe, text = 'browse...', command=self.setsourcefile)
    self.loadfile = tk.Button(self.inputframe, text = 'download', command=self.loadsourcefile)

    self.destinationtext = tk.Label(self.outputframe, text='output path: ')
    self.destinationpath = tk.Entry(self.outputframe)
    rClickbinder(self.destinationpath)

    self.overwrite = tk.IntVar()
    self.overwritecontent = tk.Checkbutton(self.outputframe, text = 'overwrite', variable=self.overwrite, onvalue=True, offvalue=False)

    self.browsedestinationfile = tk.Button(self.outputframe, text = 'browse...', command=self.setdestinationpath)
    self.writecontent = tk.Button(self.outputframe, text = 'write!', command=self.extracttopath)

    self.messages = tk.StringVar()
    self.appmessages = tk.Message(self.messageframe, anchor='nw', justify='left', width=500, textvariable=self.messages)

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

    self.appmessages.grid(row=2)

    tkMessageBox.showwarning(message="WARNING!\n\nThis app can erase all contents of directories with the 'overwrite' checkbox being marked! Do not use it or use with caution!")
    self.sourcepath.focus_force() # impolite, but works...

  def setsourcefile(self):
    #print("setsourcefile()")
    filepath = askopenfilename(filetypes = [('ZIP-files', '.zip'), ('All files', '.*')], title = "Pick a ZIP-file")
    print("Sourcepath set: ", filepath)
    self.sourcepath.delete(0, last='end')
    self.sourcepath.insert(0, filepath)

  def loadsourcefile(self):
    #print("loadsourcefile()")
    print("Loading from: ", self.sourcepath.get())
    self.printmessage("Loading from: " + str(self.sourcepath.get()))
    # not so nice check for if it is probably a url or local file...
    if (self.sourcepath.get() == ""):
      print("Sourcepath is empty")
      self.printmessage("Sourcepath is empty")
    else:
      if (self.sourcepath.get().startswith("http") or self.sourcepath.get().startswith("www")):
        (source, headers) = urllib.urlretrieve(self.sourcepath.get(), )
        print("File retrieved")
        self.printmessage("File retrieved")
      else:
        (source, headers) = urllib.urlretrieve("file:" + self.sourcepath.get(), )
        print("File retrieved")
        self.printmessage("File retrieved")
      if (zipfile.is_zipfile(source) == True):
        print("File is a valid ZIP file")
        self.printmessage("File is a valid ZIP file")
        self.sourcepath.delete(0, last='end')
        self.sourcepath.insert(0, source)
        print("New source file: ", source)
        return True
      else:
        print("ERROR: File is NOT a valid ZIP file")
        self.printmessage("ERROR: File is NOT a valid ZIP file")
        return False

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
        if (os.path.isfile(path)):
          print("Deleted entry:", path)
          os.unlink(path)
        else:
          shutil.rmtree(path)
          print("Deleted entry:", path)
      except Exception as e:
        print("Exception caught:", e)
        return False
    return True

  def extracttopath(self):
    #print("extracttopath()")
    if (self.loadsourcefile()):
      if (os.path.isdir(self.destinationpath.get())):
        if (self.overwrite.get() == True):
          question = "Are you sure you want to ! ERASE ! contents of " + str(self.destinationpath.get()) + " ?"
          print("WARNING: no check for illegal content of zip-file!") # see: http://docs.python.org/3/library/zipfile.html?highlight=zipfile#zipfile.ZipFile.extractall
          self.printmessage("WARNING: no check for illegal content of zip-file!") # see: http://docs.python.org/3/library/zipfile.html?highlight=zipfile#zipfile.ZipFile.extractall
          areyousure = tkMessageBox.askyesno(message=question, icon='question', title='ERASE ALL!?')
          if (areyousure == True):
            print("Overwrite enabled! Erasing contents of:", self.destinationpath.get())
            self.printmessage("Overwrite enabled! Erasing contents of: " + str(self.destinationpath.get()))
            if(self.erasepathcontent() == True):
              self.printmessage("Unpacking files...")
              print("Unpacking files...")
              myfile = ZipFile(self.sourcepath.get())
              myfile.extractall(self.destinationpath.get())
              print("Done!")
              self.printmessage("Done!")
            else:
              self.printmessage("Erasing failed, didn't unpack")
              print("Erasing failed, didn't unpack")
        else:
          print("Overwrite disabled! Appending to: ", self.destinationpath.get())
          print("Unpacking files...")
          myfile = ZipFile(self.sourcepath.get())
          myfile.extractall(self.destinationpath.get())
          print("Done!")
          self.printmessage("Done!")
      else:
        print("Destinationpath is not a valid directory")
    else:
      print("Loading source failed")
      self.printmessage("Loading source failed")

  def printmessage(self, message):
    self.messages.set(message)

# copied from: http://stackoverflow.com/questions/4266566/stardand-context-menu-in-python-tkinter-text-widget-when-mouse-right-button-is-p
def rClicker(e):
  ''' right click context menu for all Tk Entry and Text widgets
  '''

  try:
    # workaround for different cmd key on mac
    if(platform.system() == 'Darwin'):
      keyname = 'Command'
    else:
      keyname = 'Control'

    def rClick_Copy(e, apnd=0):
      e.widget.event_generate('<' + keyname + '-c>')

    def rClick_Cut(e):
      e.widget.event_generate('<' + keyname + '-x>')

    def rClick_Paste(e):
      e.widget.event_generate('<' + keyname + '-v>')

    e.widget.focus()

    nclst=[
           (' Cut', lambda e=e: rClick_Cut(e)),
           (' Copy', lambda e=e: rClick_Copy(e)),
           (' Paste', lambda e=e: rClick_Paste(e)),
           ]

    rmenu = tk.Menu(None, tearoff=0, takefocus=0)

    for (txt, cmd) in nclst:
      rmenu.add_command(label=txt, command=cmd)

    rmenu.tk_popup(e.x_root+40, e.y_root+10, entry="0")

  except tk.TclError:
    print("rClick menu, something wrong")
    pass

  return "break"

def rClickbinder(r):
  try:
    # workaround for different mouse button on mac
    if(platform.system() == 'Darwin'):
      buttonname = '<Button-2>'
    else:
      buttonname = '<Button-3>'
    r.bind(buttonname, rClicker)
  except tk.TclError:
    print("rClickbinder, something wrong")
    pass

root = tk.Tk()
root.title("Unzipapp")
CUnzipApp(root)
root.mainloop()
