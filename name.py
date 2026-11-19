import json
import requests as req
import random
from skeetorink import GENERATORS


NAME_METHODS = []
TITLES = ["Sir", "Madam", "Mr.", "Mrs.", "Ms.", "Miss", "Mister", "Lord", "Lady", "Duke", "Duchess", "M'lord", "Milady", "Mx.", "Dr.", "Rev.", "Dame", "Baron", "Baroness"]
SUFFIXES = ["Jr.", "Sr.", "Esq.", "III", "IV", "VII", "II"]

def name_method(func):
    NAME_METHODS.append(func)
    return func

@name_method
def from_ironarachne():
    races = ["dragonborn", "dwarf", "elf", "gnome", "goblin", "half-elf", "half-orc", "halfling", "human", "orc", "tiefling", "troll"]
    url = "https://names.ironarachne.com/race/" + random.choice(races)
    res = req.get(url + "/given/1", timeout=5)
    res.raise_for_status()
    n = res.json()["names"][0]
    if random.random() < 0.5:
        res = req.get(url + "/family/1", timeout=5)
        res.raise_for_status()
        n += " " + res.json()["names"][0]
    if random.random() < 0.2:
        n = (random.choice(TITLES) + " " + n)
    if random.random() < 0.1:
        n += (" " + random.choice(SUFFIXES))
    return n

# @name_method
# def from_randomapi():
#     baseUrl = "https://randomapi.dev/api/"
#     format = []
#     if random.random() < 0.1:
#         format.append("t")
#     if random.random() < .5:
#         format.append("f")
#         if random.random() < .5:
#             format.append("l")
#     else:
#         format.append("w")
#     if random.random() 
# 
# 
#     method = random.choice([
#         "firstlast",
#         "first",
#         "titlename",
#         "word",
#         "titleword",
# 
#         ("names?count=1", lambda d: d[0]["firstName"] + " " + d[0]["lastName"]),
#         ("words?type=noun&count=1", lambda d: d[0]["word"][:1].upper()),
#     ])
#     res = req.get(baseUrl + url, timeout=5)
#     res.raise_for_status()
#     return parse(res.json()["data"])

@name_method
def from_skeetorink():
    return random.choice(list(GENERATORS.values())).generate()

def from_file():
    with open("json-assets/name/names.json", 'r') as f:
        names = json.load(f)
    return random.choice(names)

def randName():
    for method in random.sample(NAME_METHODS, len(NAME_METHODS)):
        try:
            name = method()
            if name:
                return name
            raise ValueError(f"Name generation method {method.__name__} returned an empty name.")
        except Exception as e:
            print(f"Name generation method {method.__name__} failed: {e}")
    try:
        name = from_file()
        if name:
            return name
        raise ValueError("Fallback name generation from file returned an empty name.")
    except Exception as e:
        print(f"Fallback name generation from file failed: {e}")
    raise RuntimeError("All name generation methods failed.")
