from Tkinter import *
import zipfile
import urllib
import os

def downloadZipFile():
  #url = "http://download.thinkbroadband.com/1MB.zip"
  url = "localfile.zip"
  print "downloading file from: " + url
  (downloadedFile, headers) = urllib.urlretrieve(url)
  if (zipfile.is_zipfile(downloadedFile) == True):
    print "file is a valid ZIP-file"
    return downloadedFile
  else:
    print "file is NOT a valid ZIP-file"

# source: http://www.techniqal.com/blog/2008/07/31/python-file-read-write-with-urllib2/

def selectZipFile():
  print "select the zip file located locally"

  return file

def chooseOutputDisk():
  print "select output disk from list..."

  return path

def unpackToOutputDisk(file, path):
  print "unpacking files to disk..."

myfile = downloadZipFile()
local = open("myfile.zip", "w")
local.write(myfile)
local.close()

"""
chooseOutputDisk()
unpackToOutputDisk()

root = Tk()

w = Label(root, text="Hello, world!")
w.pack()



root.mainloop()
"""



"""
/////
file downloader / importer
- insert zip
- insert url
- hardcoded

/////
usb drive / sd card checker
- available?
- write protected?
- checkbox : erase disk

/////
unpacker/unzipper
- write access to drive(s)
"""
