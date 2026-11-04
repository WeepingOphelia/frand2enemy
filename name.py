import json
import requests as req
import random
from skeetorink import GENERATORS


NAME_METHODS = []

def name_method(func):
    NAME_METHODS.append(func)
    return func

@name_method
def from_randomapi():
    url, parse = random.choice([
        ("https://randomapi.dev/api/names?count=1", lambda d: d[0]["firstName"] + " " + d[0]["lastName"]),
        ("https://randomapi.dev/api/words?type=noun&count=1", lambda d: d[0]["word"][:1].upper() + d[0]["word"][1:]),
    ])
    res = req.get(url, timeout=5)
    res.raise_for_status()
    return parse(res.json()["data"])

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
