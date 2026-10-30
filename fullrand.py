import random
import json
from bs4 import BeautifulSoup


def rawAF():
  character = {}
  print("Yoloing new character...")
  print("Selecting Ancestry... ")
  character["ancestry"] = ancSelect()
  print("Selecting Class... ")
  character["class"] = classSelect()
  return character


def ancSelect():
  with open("json-assets/packs/ancestries.json", "r", encoding="utf-8") as f:
    ancestries = json.load(f)
    an = ancestries[random.randrange(len(ancestries))]
    print("You're a (probably disgusting)", an["name"], "\n")
    print(BeautifulSoup(an["system"]["description"]["value"], "html.parser").find("p").get_text(strip=True))
    return an

def classSelect():
  with open("json-assets/packs/classes.json", "r", encoding="utf-8") as f:
    classes = json.load(f)
    cl = classes[random.randrange(len(classes))]
#    lvl = random.rand(1, 20)
    print(f"You're a level {cl['name']}.  Of course you filthy casual.\n")
    return cl
if __name__ == "__main__":
  rawAF()