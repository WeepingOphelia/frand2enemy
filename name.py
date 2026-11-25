import json
import requests as req
import numpy as np
from skeetorink import GENERATORS


NAME_METHODS = []
TITLES = ["Sir", "Madam", "Mr.", "Mrs.", "Ms.", "Miss", "Mister", "Lord", "Lady", "Duke", "Duchess", "M'lord", "Milady", "Mx.", "Dr.", "Rev.", "Dame", "Baron", "Baroness", "Prof", "Brother", "Sister"]
SUFFIXES = ["Jr.", "Sr.", "Esq.", "III", "IV", "VII", "II"]

rng = np.random.default_rng()

def name_method(func):
    NAME_METHODS.append(func)
    return func

@name_method
def from_ironarachne():
    races = ["dragonborn", "dwarf", "elf", "gnome", "goblin", "half-elf", "half-orc", "halfling", "human", "orc", "tiefling", "troll"]
    url = "https://names.ironarachne.com/race/" + rng.choice(races)
    res = req.get(url + "/given/1", timeout=5)
    res.raise_for_status()
    n = res.json()["names"][0]
    if rng.random() < 0.5:
        res = req.get(url + "/family/1", timeout=5)
        res.raise_for_status()
        n += " " + res.json()["names"][0]
    if rng.random() < 0.2:
        n = (rng.choice(TITLES) + " " + n)
    if rng.random() < 0.1:
        n += (" " + rng.choice(SUFFIXES))
    return n

@name_method
def from_randomapi():
    format = []
    if rng.random() < 0.15:
        format.append("t")
    if rng.random() < 0.6:
        format.append("f")
    else:
        format.append("n")
    if rng.random() < 0.7:
        format[-1] += "l"
        
    if rng.random() < 0.1:
        format.append("s")
    if rng.random() < 0.2:
        format.append("e")

    def apiHelper(w):
        baseUrl = "https://randomapi.dev/api/"
        suf = ""
        match w:
            case "name":
                suf = "names?count=1"
            case "noun":
                suf = "words?type=noun&count=1"
            case "adj":
                suf = "words?type=adjective&count=1"
        res = req.get(baseUrl + suf, timeout=5)
        res.raise_for_status()
        return res.json()["data"][0]

    def nameBuilder(f):
        match f:
            case "t":
                return rng.choice(TITLES)
            case "f":
                return apiHelper("name")["firstName"]
            case "fl":
                d = apiHelper("name")
                return d["firstName"] + " " + d["lastName"]
            case "n":
                return apiHelper("noun")["word"].capitalize()
            case "nl":
                n = apiHelper("noun")["word"].capitalize()
                l = apiHelper("name")["lastName"]
                return n + " " + l
            case "s":
                return rng.choice(SUFFIXES)
            case "e":
                return "the " + apiHelper("adj")["word"].capitalize()

    return " ".join(map(nameBuilder, format))


@name_method
def from_skeetorink():
    return rng.choice(list(GENERATORS.values())).generate()

def from_file():
    with open("json-assets/name/names.json", 'r') as f:
        names = json.load(f)
    return rng.choice(names)

def randName():
    for method in rng.choice(NAME_METHODS, len(NAME_METHODS), replace=False):
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
    print("All name generation methods failed.")
    return rng.choice(["Cleatus", "Bob", "Dave", "poopfeast420", "Tricia", "Lyra", "Carol"])
