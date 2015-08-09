# Scans all images in a folder and reports on their Flash settings
#
# Input: image or folder (recursive) you want to scan
#
# Good site for EXIF tag info: http://www.sno.phy.queensu.ca/~phil/exiftool/TagNames/EXIF.html#Flash
#
import os,sys,glob
from PIL import Image
from PIL.ExifTags import TAGS

VERSION = "v0.2.0"
verbose = False

# Use a dictionary to define or EXIF Flash values in human readable form
FlashValues = {}
FlashValues[0x0]	= "No Flash"
FlashValues[0x1]	= "Fired"
FlashValues[0x5]	= "Fired, Return not detected"
FlashValues[0x7]	= "Fired, Return detected"
FlashValues[0x8]	= "On, Did not fire"
FlashValues[0x9]	= "On, Fired"
FlashValues[0xd]	= "On, Return not detected"
FlashValues[0xf]	= "On, Return detected"
FlashValues[0x10]	= "Off, Did not fire"
FlashValues[0x14]	= "Off, Did not fire, Return not detected"
FlashValues[0x18]	= "Auto, Did not fire"
FlashValues[0x19]	= "Auto, Fired"
FlashValues[0x1d]	= "Auto, Fired, Return not detected"
FlashValues[0x1f]	= "Auto, Fired, Return detected"
FlashValues[0x20]	= "No flash function"
FlashValues[0x30]	= "Off, No flash function"
FlashValues[0x41]	= "Fired, Red-eye reduction"
FlashValues[0x45]	= "Fired, Red-eye reduction, Return not detected"
FlashValues[0x47]	= "Fired, Red-eye reduction, Return detected"
FlashValues[0x49]	= "On, Red-eye reduction"
FlashValues[0x4d]	= "On, Red-eye reduction, Return not detected"
FlashValues[0x4f]	= "On, Red-eye reduction, Return detected"
FlashValues[0x50]	= "Off, Red-eye reduction"
FlashValues[0x58]	= "Auto, Did not fire, Red-eye reduction"
FlashValues[0x59]	= "Auto, Fired, Red-eye reduction"
FlashValues[0x5d]	= "Auto, Fired, Red-eye reduction, Return not detected"
FlashValues[0x5f]	= "Auto, Fired, Red-eye reduction, Return detected"

# Global values used to print the report
FlashReport = {}
totalPhotos = 0
noFlashInfo = 0

# Get specific EXIF field values
#
# Returne: EXIF value for field, or None type
#
def get_field (exif,field) :
  for (k,v) in exif.iteritems():
     if TAGS.get(k) == field:
        return v
        
def getImageEXIFInfo(file) :
  try:
    image = Image.open(file)
    return image._getexif()
  except IOError:
    return None
  except AttributeError:
    return None
    
def getImageFlashInfo(file) :
  exifData = getImageEXIFInfo(file)
  if exifData is not None:
    return get_field(exifData,'Flash')
  else:
    #print "Not an Photo"
    return -1 
    
def handleFile(file) :
  global verbose, totalPhotos, noFlashInfo

  val = getImageFlashInfo(file)

  if val == -1:
    if verbose:
      print "File is not an Photo [\"" + file + "\"]"
    return
  elif val is None:
    print "Flash Value not defined in EXIF for [\"" + file + "\"]"
    noFlashInfo += 1
  else:
    if val in FlashValues: 
      print "[\"" + file + "\", \"" + FlashValues[val] + "\"]"
      if val in FlashReport:
        FlashReport[val] += 1
      else:
        FlashReport[val] = 1
    else:
      print "Unable to find Flash Value [\"{}\", \"{}\"]".format(file, val)
      
  totalPhotos += 1

def processFile(file) :
  if os.path.isfile(file) == False:
    print "Invalid Parameters: Could not find file or folder [" + path + "]"
    return
  handleFile(file)

# Takes a directory and iterates through it recursively
# Passes all files into the handleFile()
#
# If dir is invalid (a file or does not exist) function returns without doing anything
def processDir(dir) :
  if os.path.isdir(dir) == False:
    print "Invalid dir passed into processDir [" + dir + "]"
    return
   
  listing = os.listdir(dir)
  for infile in listing:
    #print "current file is: " + infile
    
    # fullPath needed so that we maintain parent dirs when being recursive
    fullPath = dir
    # Avoid double forward slash if not needed
    if dir.endswith("/") == False:
      fullPath += "/"
    fullPath += infile
    
    if os.path.isdir(fullPath):
      processDir(fullPath)
    else:  
      handleFile(fullPath)
      
def printFlashReport() :
  print ""
  print "Camera Flash Report"
  print "Total Photos Scanned: ", totalPhotos
  print "Photos Without Flash Info: ", noFlashInfo
  print ""
  for key in FlashValues:
    val = 0
    if key in FlashReport:
      val = FlashReport[key]
    print val, FlashValues[key]
  print ""

################# Start Main #########################

print "Launching PyImgScanner " + VERSION

# First check to make sure at least 1 param is passed in (first passed in param is [1] not [0])
if len(sys.argv) < 2:
  print "Invalid Parameters: You must pass in either a file or folder to scan"
  sys.exit()

path = sys.argv[1]

# Now check if param is a file or folder and call correct process
if os.path.isdir(path):
  processDir(path)  
else:
  processFile(path)
  
  
printFlashReport()
