from collections import defaultdict
from dataclasses import dataclass, field
import json
import numpy as np
import random
import string

from bs4 import BeautifulSoup

SKILL_RANKS = {1: "Trained", 2: "Expert", 3: "Master", 4: "Legendary"}
STAT_IDS = ["str", "dex", "con", "int", "wis", "cha"]

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

  def amod(self, a):
    return np.floor((self.stat[a] - 10) / 2)

  def abBoost(self):
    bs = [self.ka]
    abb = self.stat.keys()
    abb.remove(self.ka)
    bs.append(random.sample(abb, k=3))
    for s in bs:
      self.stat[s] += 2
  
  def calcHP(self):
    self.hp = self.anchp + (self.lvl * (self.clhp + self.amod["con"]))

  def calcSaves(self):
    self.saves["fort"] = (self.basesaves["fortitude"] * 2) + self.amod["con"] + self.lvl
    self.saves["ref"] = (self.basesaves["reflex"] * 2) + self.amod["dex"] + self.lvl
    self.saves["will"] = (self.basesaves["will"] * 2) + self.amod["wis"] + self.lvl


  def printChar(self):
    # NAME LVL CLASS
    print(f"{self.name} Lvl {self.lvl} {self.cl}")
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
    print(f"Per: ")

    # STATS (ABILITY/SAVE)
    print(f"""
STR: {self.stat['str']:<7} FORT: {self.saves['fort']}
DEX: {self.stat['dex']:<7} REF:  {self.saves['ref']}
CON: {self.stat['con']:<7} WILL: {self.saves['will']}
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







