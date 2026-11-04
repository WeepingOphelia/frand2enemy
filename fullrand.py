import json
import numpy as np
import name
import math

import character as char

from bs4 import BeautifulSoup

rng = np.random.default_rng()
newc = char.Character()

def rawAF():
  print("Yoloing new character...")
  print("Rolling name... ")
  newc.name = name.randName()
  print("Selecting Ancestry... ")
  an = ancSelect()
  newc.anc = an["name"]
  print("Selecting Background... ")
  bg = bgSelect()
  newc.bg = bg["name"]
  print("Selecting Class... ")
  cl, newc.lvl = classSelect()
  newc.cl = cl["name"]
  initStats(an, bg, cl)
  print(newc)
  return newc


def ancSelect():
  an = randSelect("ancestries")
  print("You're a (probably disgusting)", an["name"], "\n")
#    print(BeautifulSoup(an["system"]["description"]["value"], "html.parser").find("p").get_text(strip=True))
  if an["system"]["vision"] != "normal":
    newc.senses.append(an["system"]["vision"])
  return an

def bgSelect():
  bg = randSelect("backgrounds")
  print("You're a lowly", bg["name"], "\n")
  return bg

def classSelect():
  cl = randSelect("classes")
  lvl = int(np.clip(np.round(rng.lognormal(mean=1.45, sigma=0.85) - 0.4), 1, 20))
  print(f"You're a level {lvl} {cl['name']}.  Of course you are, you filthy casual.\n")
  return cl, lvl

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
  return rolls

def initStats(an, bg, cl):

  stat_ids = ["str", "dex", "con", "int", "wis", "cha"]
  ka = rng.choice(cl["system"]["keyAbility"]["value"])

  rolls = rollStats()
  newc.stat[ka] = max(rolls)
  rolls.remove(max(rolls))

  for s in stat_ids:
    if s != ka:
      newc.stat[s] = rolls.pop()

  print("Your base stats are:")
  for stat, value in newc.stat.items():
    print(f"{stat.upper()}: {value}")
  print("")

  boosts = an["system"]["boosts"]
  if len(boosts["0"]["value"]) != 1:
    if rng.choice(10) > 8:
      newc.stat[ka] += 2
    else:
      newc.stat[boosts["0"]["value"][rng.integers(0, 6)]] += 2
  else:
    newc.stat[boosts["0"]["value"][0]] += 2
  if len(boosts["1"]["value"]) == 1:
    newc.stat[boosts["1"]["value"][0]] += 2
  for f in an["system"]["flaws"].values():
    if len(f["value"]) == 1:
      newc.stat[f["value"][0]] -= 2

  for b in bg["system"]["boosts"].values():
    if len(b["value"]) == 1:
      newc.stat[b["value"][0]] += 2

  amod = {}
  for s in newc.stat:
    amod[s] = math.floor((newc.stat[s] - 10) / 2)

  saves = cl["system"]["savingThrows"]
  newc.saves["fort"] = (saves["fortitude"] * 2) + amod["con"] + newc.lvl
  newc.saves["ref"] = (saves["reflex"] * 2) + amod["dex"] + newc.lvl
  newc.saves["will"] = (saves["will"] * 2) + amod["wis"] + newc.lvl




if __name__ == "__main__":
  rawAF()