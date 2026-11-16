from dataclasses import dataclass, field
import json
import numpy as np

from bs4 import BeautifulSoup

@dataclass
class Character:
    name: str = ""
    lvl: int = None
    hp: int = None
    anc: str = ""
    bg: str = ""
    cl: str = ""
    stat: dict = field(default_factory=lambda: {
        "str": 10,
        "dex": 10,
        "con": 10,
        "int": 10,
        "wis": 10,
        "cha": 10
    })
    skills: list = field(default_factory=list)
    feats: list = field(default_factory=list)
    saves: dict = field(default_factory=lambda: {
        "fort": 0,
        "ref": 0,
        "will": 0
    })
    senses: list = field(default_factory=list)

    def boostStats(self, boosts):
        for b in boosts:
            self.stat[b] += 2


    def printChar(self):
        print(f"{self.name} Lvl {self.lvl} {self.cl}")
        print(f"{self.anc} Background: {self.bg}\n")

        print(f"Languages: ")
        if len(self.senses) > 0:
          print(f"Senses: {", ".join(s.capitalize() for s in self.senses)}\n")
        else:
          print(f"Senses: Normal")
        print(f"""  STR: {self.stat['str']:<7} FORT: {self.saves['fort']}
  DEX: {self.stat['dex']:<7} REF:  {self.saves['ref']}
  CON: {self.stat['con']:<7} WILL: {self.saves['will']}
  INT: {self.stat['int']:<7}
  WIS: {self.stat['wis']:<7}
  CHA: {self.stat['cha']:<7}
        """)

        ls = []
        sks = self.skills
        for sk in self.skills:
           if "Lore" in sk:
              ls.append(sk)
              sks.remove(sk)

        for sk in sorted(sks):
           print(f"{sk}")
        for l in sorted(ls):
           print(f"{l}")
        







