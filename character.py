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







