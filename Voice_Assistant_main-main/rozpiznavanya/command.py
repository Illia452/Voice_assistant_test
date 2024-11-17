# Select current python file in explorer
import os, sys, subprocess, inspect
from PIL import ImageGrab


def selectFile():
  #subprocess.Popen(r'explorer /select,%s' % os.path.abspath(inspect.getfile(inspect.currentframe())))

  ## or...

  pFileName = os.path.abspath(inspect.getfile(inspect.currentframe()))
  pFileDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
  print ( 'pFileName = %s\n' % pFileName)
  print ('pFileDir = %s' % pFileDir)
  subprocess.Popen(r'explorer /select,%s' % pFileName)
  if (pFileName.endswith(".png") or pFileName.endswith(".py") or pFileName.endswith(".txt")):
     subprocess.call([r'C:\Program Files\Notepad++\notepad++.exe',  pFileName])


def takeScreenShot():
    # Capture the entire screen
    screenshot = ImageGrab.grab()

    # Save the screenshot to a file
    screenshot.save("screenshot.png")

    # Close the screenshot
    screenshot.close()