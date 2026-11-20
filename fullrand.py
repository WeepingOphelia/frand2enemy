import json
import numpy as np
import name


import character as char

SKILL_IDS = ["acrobatics", "arcana", "athletics", "crafting", "deception", "diplomacy", "intimidation", "medicine", "nature", "occultism", "performance", "religion", "society", "stealth", "survival", "thievery"]
RANKS = {"trained": 1, "expert": 2, "master": 3, "legendary": 4}
STAT_IDS = ["str", "dex", "con", "int", "wis", "cha"]

rng = np.random.default_rng()
newc = char.Character()

def rawAF(lvl):
  newc = char.Character()
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
  if lvl == 0:
    lvl = lvlSelect()
  cl = classSelect(lvl)
  newc.cl = cl
  initStats(an, bg, cl)
  if newc.amod("int") > 0:
    for _ in range(newc.amod("int")):
      newc.skIncrease()
  lvlChar(cl, lvl)
  newc.printChar()
#  print(newc)
  return newc


def ancSelect():
  an = randSelect("ancestries")
  newc.anchp = an["system"]["hp"]
  newc.size = an["system"]["size"]
  newc.speed = an["system"]["speed"]
  print(f"You're a (probably disgusting) {an["name"]}\n")

  # ADD ANC SENSES
  if an["system"]["vision"] != "normal":
    newc.senses.append(an["system"]["vision"])

  # ADD ANC FEATS
  for v in an["system"]["items"].values():
    if "ancestryfeatures" in v["uuid"]:
      newc.addFeat(wikiFeat(v["uuid"].split(".")[-1], "an"))
  
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

  # ADD BG FEATS

  for k, v in bg["system"]["items"].items():
    if "feat" in v["uuid"]:
      newc.addFeat(wikiFeat(v["uuid"].split(".")[-1], "bg"))
  
  return bg

def classSelect(lvl):
  cl = randSelect("classes")
  newc.clhp = cl["system"]["hp"]
  newc.per = cl["system"]["perception"]
  print(f"You're a level {lvl} {cl['name']}.  Of course you are, you filthy casual.\n")

  # CLASS SKILLS
  cs = cl["system"]["trainedSkills"]["additional"]
  for sk in cl["system"]["trainedSkills"]["value"]:
    if newc.skills[sk] > 0:
      cs += 1
    else:
      newc.skills[sk] = 1
  vs = [s for s, v in newc.skills.items() if v == 0]
  si = rng.choice(vs, size=cs, replace=False)
  for s in si:
    newc.skills[s] = 1


  return cl

def lvlSelect():
  return int(np.clip(np.round(rng.lognormal(mean=1.45, sigma=0.85) - 0.4), 1, 20))

def randSelect(pack):
  with open(f"json-assets/packs/{pack}.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    return data[rng.integers(0, len(data))]

def selectFeat(type):
  vfs = []
  with open(f"json-assets/packs/feats.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    for feat in data:

      # CHECK FEAT TYPE
      if feat["system"]["category"] != type:
        continue

      # CHECK IF KNOWN FEAT
      if feat["name"] in newc.feats:
        continue

      # CHECK IF FEAT IN CLASS FEATURES
      if feat["name"] in [i["name"] for i in newc.cl["system"]["items"].values()]:
        continue

      # CHECK ANCESTRY
      if type == "ancestry" and newc.anc.lower() not in feat["system"]["traits"]["value"]:
        continue

      # CHECK LEVEL REQ
      if feat["system"]["level"]["value"] > newc.lvl:
        continue

      # CHECK FOR PREREQS
      reqs = feat["system"]["prerequisites"]["value"]
      if len(reqs) == 0:
        vfs.append(feat)

      else:
        ok = []
        for req in reqs:

          # CHECK IF SKILL REQ

          words = req["value"].lower().split()
          if len(words) == 3 and words[2] in SKILL_IDS and words[0] in RANKS.keys():
            sk = words[2]
            r = words[0]
            if newc.skills[sk] >= RANKS[r]:
              ok.append("pass")

          # CHECK IF FEAT REQ
          elif req["value"] in newc.feats:
            ok.append("pass")

        if len(ok) == len(reqs):
          vfs.append(feat)
          
    return vfs[rng.integers(len(vfs))]

def wikiFeat(uuid, type):
  d = "feats"
  if type == "cl":
    d = "class-features"
  if type == "an":
    d = "ancestry-features"
  with open(f"json-assets/packs/{d}.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    for feat in data:
      if feat["_id"] == uuid:
        return feat

def rollStats():
  print("Rolling stats...")
  rolls = []
  for i in range(6):
    roll = sorted(rng.integers(1, 7, size=4))
    rolls.append(int(sum(roll[1:])))
  return rolls

def initStats(an, bg, cl):

  # TEMP PSYCHIC FIX

  if cl["name"] == "Psychic":
    newc.ka = str(rng.choice(["int", "cha"]))
  else:

  # SET KEY ABILITY

    newc.ka = str(rng.choice(cl["system"]["keyAbility"]["value"]))

  # INITIAL STAT ROLL

  rolls = rollStats()
  print(rolls, "\n")
  newc.stat[newc.ka] = max(rolls)
  rolls.remove(max(rolls))

  for s in STAT_IDS:
    if s != newc.ka:
      newc.stat[s] = rolls.pop()


  bs = "Your base stats are: "
  for stat, value in newc.stat.items():
    bs += f"{stat.upper()}: {value} "
  print(bs + "\n")

  # ANC BOOSTS

  boosts = an["system"]["boosts"]
  if len(boosts["0"]["value"]) != 1:
    if rng.choice(10) < 8:
      newc.stat[newc.ka] += 2
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

  # SAVES

  newc.basesaves = cl["system"]["savingThrows"]
  
def lvlChar(cl, lvl):
  while newc.lvl < lvl:
    newc.lvl += 1
    print(f"Leveling {newc.name} to {newc.lvl}...")
    if newc.lvl == 1 or newc.lvl % 5 == 0:
      newc.abBoost()
    if newc.lvl in cl["system"]["skillIncreaseLevels"]["value"]:
      newc.skIncrease()
    for v in cl["system"]["items"].values():
      if v["level"] == newc.lvl:
        newc.addFeat(wikiFeat(v["uuid"].split(".")[-1], "cl"))
    if newc.lvl in cl["system"]["ancestryFeatLevels"]["value"]:
      newc.addFeat(selectFeat("ancestry"))
    if newc.lvl in cl["system"]["classFeatLevels"]["value"]:
      newc.addFeat(selectFeat("class"))
    if newc.lvl in cl["system"]["generalFeatLevels"]["value"]:
      newc.addFeat(selectFeat("general"))
    if newc.lvl in cl["system"]["skillFeatLevels"]["value"]:
      newc.addFeat(selectFeat("skill"))
  newc.calcHP()
  newc.calcSaves()

if __name__ == "__main__":
  rawAF()