import json
import numpy as np
import name
import math
import random


import character as char

from bs4 import BeautifulSoup

STAT_IDS = ["str", "dex", "con", "int", "wis", "cha"]
SKILL_IDS = ["acrobatics", "arcana", "athletics", "crafting", "deception", "diplomacy", "intimidation", "medicine", "nature", "occultism", "performance", "religion", "society", "stealth", "survival", "thievery"]

rng = np.random.default_rng()
newc = char.Character()

def rawAF():
  print("Yoloing new character...\n")
  print("Rolling name... \n")
  newc.name = name.randName()
  print(f"Hello - {newc.name}\n")
  print("Selecting Ancestry... ")
  an = ancSelect()
  newc.anc = an["name"]
  for s in SKILL_IDS:
    newc.skills[s] = 0
  print("Selecting Background... ")
  bg = bgSelect()
  newc.bg = bg["name"]
  print("Selecting Class... ")
  cl, newc.lvl = classSelect()
  newc.cl = cl["name"]
  initStats(an, bg, cl)
  newc.printChar()
#  print(newc)
  return newc


def ancSelect():
  an = randSelect("ancestries")
  print(f"You're a (probably disgusting) {an["name"]}\n")

  # ADD ANC SENSES
  if an["system"]["vision"] != "normal":
    newc.senses.append(an["system"]["vision"])

  # ADD ANC FEATS
  for v in an["system"]["items"].values():
    if "ancestryfeatures" in v["uuid"]:
      newc.feats.append(v["name"])
  
  return an

def bgSelect():
  bg = randSelect("backgrounds")
  print("You're a lowly", bg["name"], "\n")

  # ADD BG SKILLS

  bgs = bg["system"]["trainedSkills"]["value"]
  bgl = bg["system"]["trainedSkills"]["lore"]
  for s in bgs:
    newc.skills[s] = 1
  for l in bgl:
    newc.lore[l] = 1
  
  return bg

def classSelect():
  cl = randSelect("classes")

  # ROLL LVL
  lvl = int(np.clip(np.round(rng.lognormal(mean=1.45, sigma=0.85) - 0.4), 1, 20))
  print(f"You're a level {lvl} {cl['name']}.  Of course you are, you filthy casual.\n")

  # CLASS SKILLS
  cs = cl["system"]["trainedSkills"]["additional"]
  for sk in cl["system"]["trainedSkills"]["value"]:
    if newc.skills[sk] > 0:
      cs += 1
    else:
      newc.skills[sk] = 1
  vs = [s for s, v in newc.skills.items() if v == 0]
  si = random.sample(vs, k=cs)
  for s in si:
    newc.skills[s] = 1


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

  if cl["name"] == "Psychic":
    ka = rng.choice(["int", "char"])
  else:
    ka = rng.choice(cl["system"]["keyAbility"]["value"])

  # INITIAL STAT ROLL

  rolls = rollStats()
  print(rolls, "\n")
  newc.stat[ka] = max(rolls)
  rolls.remove(max(rolls))

  for s in STAT_IDS:
    if s != ka:
      newc.stat[s] = rolls.pop()

#  print("Your base stats are:")
#  for stat, value in newc.stat.items():
#    print(f"{stat.upper()}: {value}")
#  print("")

  # ANC BOOSTS

  boosts = an["system"]["boosts"]
  if len(boosts["0"]["value"]) != 1:
    if rng.choice(10) < 8:
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

  # BG BOOSTS

  for b in bg["system"]["boosts"].values():
    if len(b["value"]) == 1:
      newc.stat[b["value"][0]] += 2

  # LEVEL 1 4xBOOST

  bs = [ka]
  abb = STAT_IDS
  abb.remove(ka)
  bs.append(random.sample(abb, k=3))
  newc.boostStats(abb)

  # ABILITY MODIFIERS AND SAVES

  amod = {}
  for s in newc.stat:
    amod[s] = math.floor((newc.stat[s] - 10) / 2)

  saves = cl["system"]["savingThrows"]
  newc.saves["fort"] = (saves["fortitude"] * 2) + amod["con"] + newc.lvl
  newc.saves["ref"] = (saves["reflex"] * 2) + amod["dex"] + newc.lvl
  newc.saves["will"] = (saves["will"] * 2) + amod["wis"] + newc.lvl

  # Initial HP Calculation

  newc.hp = an["system"]["hp"] + cl["system"]["hp"] + amod["con"]


if __name__ == "__main__":
  rawAF()