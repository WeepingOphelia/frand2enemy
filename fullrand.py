import json
import numpy as np
import name

import character as char

from bs4 import BeautifulSoup

rng = np.random.default_rng()
newc = char.Character()

def rawAF():
  print("Yoloing new character...")
  rollStats()
  print("Rolling name... ")
  newc.name = name.randName()
  print("Selecting Ancestry... ")
  newc.anc = ancSelect()
  print("Selecting Background... ")
  newc.bg = bgSelect()
  print("Selecting Class... ")
  newc.cl, newc.lvl = classSelect()
  print(newc)
  return newc


def ancSelect():
  an = randSelect("ancestries")
  print("You're a (probably disgusting)", an["name"], "\n")
#    print(BeautifulSoup(an["system"]["description"]["value"], "html.parser").find("p").get_text(strip=True))
  boosts = an["system"]["boosts"]
  if len(boosts["0"]["value"]) != 1:
    newc.stat[boosts["0"]["value"][rng.integers(0, 6)]] += 2
  else:
    newc.stat[boosts["0"]["value"][0]] += 2
  if len(boosts["1"]["value"]) == 1:
    newc.stat[boosts["1"]["value"][0]] += 2
  for f in an["system"]["flaws"].values():
    if len(f["value"]) == 1:
      newc.stat[f["value"][0]] -= 2
  return an["name"]

def bgSelect():
  bg = randSelect("backgrounds")
  print("You're a lowly", bg["name"], "\n")
  for b in bg["system"]["boosts"].values():
    if len(b["value"]) == 1:
      newc.stat[b["value"][0]] += 2
  return bg["name"]

def classSelect():
  cl = randSelect("classes")
  lvl = int(np.clip(np.round(rng.lognormal(mean=1.45, sigma=0.85) - 0.4), 1, 20))
  print(f"You're a level {lvl} {cl['name']}.  Of course you are, you filthy casual.\n")
  return cl["name"], lvl

def randSelect(pack):
  with open(f"json-assets/packs/{pack}.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    return data[rng.integers(0, len(data))]

def rollStats():
  print("Rolling stats...")
  rolls = []
  for i in range(6):
    roll = sorted(rng.integers(1, 7, size=4))
    rolls.append(int(sum(roll[1:])))
  newc.stat = {
    "str": rolls[0],
    "dex": rolls[1],
    "con": rolls[2],
    "int": rolls[3],
    "wis": rolls[4],
    "cha": rolls[5]
  }
  print("Your base stats are:")
  for stat, value in newc.stat.items():
    print(f"{stat.upper()}: {value}")

if __name__ == "__main__":
  rawAF()