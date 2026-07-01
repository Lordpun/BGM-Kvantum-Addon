from pathlib import Path
import json

infoPath = Path.home() / ".config" / "BgManager" / "info.json"

def makeInfo():
  if infoPath.exists() and infoPath.stat().st_size > 0:
    return
  with open(infoPath, "w") as infoFile:
    json.dump({}, infoFile)

def getInfo():
  with open(infoPath, 'r') as infoFile:
    return json.load(infoFile)

def updateInfo(key, value):
  data = getInfo()
  data[key] = value
  with open(infoPath, "w") as infoFile:
    json.dump(data, infoFile)