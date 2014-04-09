# Luis Ramirez
# graphicslib.py
# 12/08/10
# add-on functionality for the graphics module

def checkKeys(keylist, window):
  """
  checks to see if any of the keys in the list have been pressed
  """
  key = window.checkKey()
  if key:
    for item in keylist:
      if key == item: return true

  return False


