from pathlib import Path
import xml.etree.ElementTree as ET
import infoTracking
import subprocess
import shutil
import sys
import configparser

def getQdbus():
  for cmd in ['qdbus6', 'qdbus-qt5', 'qdbus']:
    if shutil.which(cmd):
      return cmd
  return None

def setKvantumColor():
  loadedTheme = infoTracking.getInfo().get("LoadedTheme")
  if not loadedTheme.get("ChangeKvantum", True):
    return

  color = infoTracking.getInfo()["Color"]

  ET.register_namespace('inkscape', "http://www.inkscape.org/namespaces/inkscape")
  ET.register_namespace('sodipodi', "http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd")

  svg = Path.home() / ".config" / "Kvantum" / "Glassy" / "Glassy.svg"

  tree = ET.parse(svg)
  root = tree.getroot()

  window = root.find(".//{http://www.w3.org/2000/svg}g[@id='window-normal']")
  if window is None:
    sys.exit("Kvantum theme window wasn't found in the SVG")
  window.set("style", f"fill-opacity:0.70588237;opacity:0.7;fill:{color}")

  windowRect = window.find("{http://www.w3.org/2000/svg}rect")
  if windowRect is None:
    sys.exit("Kvantum theme rect wasn't found in the SVG")
  windowRect.set("style", f"fill-opacity:0.70588237;stroke:none;fill:{color}")

  tree.write(svg, encoding='utf-8', xml_declaration=True)

  setKvantumText()

  subprocess.run(f"{getQdbus()} org.kde.KWin /KWin reconfigure", shell=True)

  cache_path = Path.home() / ".cache" / "kvantum"
  if cache_path.exists():
    try:
      shutil.rmtree(cache_path)
    except OSError:
      pass

def setKvantumText():
  textColor = infoTracking.getInfo()["TextColor"]

  kvconfig = Path.home() / ".config" / "Kvantum" / "Glassy" / "Glassy.kvconfig"

  config = configparser.ConfigParser()
  config.optionxform = str
  config.read(kvconfig)

  config.set('GeneralColors', 'text.color', textColor)
  config.set('GeneralColors', 'window.text.color', textColor)
  config.set('GeneralColors', 'button.text.color', textColor)

  with open(kvconfig, 'w') as configfile:
    config.write(configfile) 

setKvantumColor()