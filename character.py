from collections import defaultdict
from dataclasses import dataclass, field
import json
import numpy as np
import random
import string

SKILL_RANKS = {1: "Trained", 2: "Expert", 3: "Master", 4: "Legendary"}
STAT_IDS = ["str", "dex", "con", "int", "wis", "cha"]
SKILL_TYPES = {
  "str": ["athletics"],
  "dex": ["acrobatics", "stealth", "thievery"],
  "con": [],
  "int": ["arcana", "crafting", "occultism", "society"],
  "wis": ["medicine", "nature", "religion", "survival"],
  "cha": ["deception", "diplomacy", "intimidation", "performance"]
}

def format_skills(skills):
  groups = defaultdict(list)
  for n, r in skills.items():
    if r > 0:
      groups[r].append(string.capwords(n))
  return [
    f"{l}: {', '.join(sorted(groups[r]))}"
    for r, l in SKILL_RANKS.items()
    if groups[r]
  ]


@dataclass
class Character:
  name: str = ""
  cl: str = ""
  clhp: int = None
  per: int = 0
  lvl: int = 0
  ka: str = ""
  anc: str = ""
  anchp: int = None
  bg: str = ""
  size: str = ""
  speed: int = None
  hp: int = None
  ac: int = None
  stat: dict = field(default_factory=lambda: {
    "str": 10,
    "dex": 10,
    "con": 10,
    "int": 10,
    "wis": 10,
    "cha": 10
  })
  skills: dict = field(default_factory=dict)
  lore: dict = field(default_factory=dict)
  feats: list = field(default_factory=list)
  arch: dict = field(default_factory=dict)
  basesaves: dict = field(default_factory=lambda: {
    "fort": 0,
    "ref": 0,
    "will": 0
  })
  saves: dict = field(default_factory=lambda: {
    "fort": 0,
    "ref": 0,
    "will": 0
  })
  senses: list = field(default_factory=list)

  def addFeat(self, f):
    if f["name"] in self.feats:
      print(f"{f["name"]} already known.")
      return
    self.feats.append(f["name"])
    print(f"Added feat - {f["name"]}")
    for r in f["system"]["rules"]:
      if r["key"] == "GrantItem" and "feat" in r["uuid"]:
        fid = r["uuid"].split(".")[-1]
        with open(f"json-assets/packs/feats.json", "r", encoding="utf-8") as j:
          data = json.load(j)
          for feat in data:
            if feat["_id"] == fid:
              self.addFeat(feat)


  def amod(self, a):
    return int(np.floor((self.stat[a] - 10) / 2))

  def abBoost(self):
    bs = [self.ka]
    abb = list(self.stat.keys())
    abb.remove(self.ka)
    bs += random.sample(abb, k=3)
    print(f"Level {self.lvl} ability boosts - {(", ".join(bs)).upper()}")
    for s in bs:
      om = self.amod(s)
      if self.stat[s] < 18:
        self.stat[s] += 2
      else:
        self.stat[s] += 1
      if s == "int" and self.amod(s) > om >= 0:
        self.skIncrease()

  
  def calcHP(self):
    self.hp = int(self.anchp + (self.lvl * (self.clhp + self.amod("con"))))

  def calcSaves(self):
    self.saves["fort"] = int((self.basesaves["fortitude"] * 2) + self.amod("con") + self.lvl)
    self.saves["ref"] = int((self.basesaves["reflex"] * 2) + self.amod("dex") + self.lvl)
    self.saves["will"] = int((self.basesaves["will"] * 2) + self.amod("wis") + self.lvl)

  def selectFeat(self, type):
    print(f"Placeholder {type} feat selection (Lvl {self.lvl})")

  def skIncrease(self):
    if self.lvl == 1:
      skmax = 1
    elif self.lvl < 7:
      skmax = 2
    elif self.lvl < 15:
      skmax = 3
    else:
      skmax = 4
    skchoice = []
    for sk in SKILL_TYPES[self.ka]:
      if self.skills[sk] < skmax:
        skchoice.append(sk)
    if len(skchoice) == 0:
      order = sorted(STAT_IDS, key=lambda s: self.amod(s), reverse=True)
      for stat in order:
        skchoice = [sk for sk in SKILL_TYPES[stat] if self.skills[sk] < skmax]
        if skchoice:
          break
    skin = random.choice(skchoice)
    self.skills[skin] += 1
    print(f"Level {self.lvl} skill increase - {skin}")

  def printChar(self):
    print("")
    # NAME LVL CLASS
    print(f"{self.name} Lvl {self.lvl} {self.cl["name"]}")
    # ANC BG
    print(f"{self.anc} {self.bg}\n")
    # LANG
    print(f"Languages: ")
    # SENSE
    if len(self.senses) > 0:
      print(f"Senses: {", ".join(s.capitalize() for s in self.senses)}\n")
    else:
      print(f"Senses: Normal")

    # HP / AC

    print(f"HP: {self.hp:<3} AC: ")
    print(f"Per: {(self.per * 2) + self.lvl + self.amod("wis"):+}")

    # STATS (ABILITY/SAVE)
    print(f"""
STR: {self.stat['str']:<7} FORT: {self.saves['fort']:+}
DEX: {self.stat['dex']:<7} REF:  {self.saves['ref']:+}
CON: {self.stat['con']:<7} WILL: {self.saves['will']:+}
INT: {self.stat['int']:<7}
WIS: {self.stat['wis']:<7}
CHA: {self.stat['cha']:<7}
      """)

    # SKILLS (ADD COLUMN SUPPORT?)
    
    print("\n".join(format_skills(self.skills | self.lore)))

    # FEATS

    print("Known Feats:")
    for f in self.feats:
      print(f)







