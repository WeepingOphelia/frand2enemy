import random

SYMBOLS = {
    "v": list("aeiou"),
    "V": ["a", "e", "i", "o", "u", "ee", "ie", "ai", "ou", "ea"],
    "c": list("bcdfghjklmnprstvwz"),
    "B": list("bcdfghjklmnprstvwz") + ["br", "cr", "dr", "gr", "tr", "bl", "pl", "sl", "sh", "ch", "th"],
    "C": list("bcdfgklmnprstvz") + ["ck", "ld", "mp", "nd", "ng", "rd", "rk", "rn", "st", "sk", "th"],
    "D": ["gr", "gl", "bl", "dr", "kr", "z", "g"],            # "dumb-sounding" consonants
    
    "i": ["Stinky", "Grumbly", "Smelly", "Lumpy", "Soggy", "Doofy", "Poopy", "Grimy", "Fuggly", "Numpy"],    # insults
    "m": ["Fluffy", "Cuddle", "Snuggle", "Sweetie", "Wiggle", "Floofy", "Fuzzy", "Nuzzle", "Honey"],   # mushy
    "M": ["kins", "bear", "pie", "bun", "toes", "cakes", "poo", "noodle", "chonk"],               # mushy endings
    "k": ["Pickle", "Bucket", "Turnip", "Sock", "Biscuit", "Gravy", "Noodle", "Crumpet"],

    # surname parts
    "P": ["Ash", "Black", "Gray", "Raven", "Stone", "Thorn", "Winter", "Grave",
          "Ember", "Hollow", "Mourn", "Wither", "Dusk", "Cinder", "Iron"],
    "S": ["son", "sen", "ford", "wood", "ham", "ley", "ton", "well", "wick",
          "stead", "mere", "wyn", "moor", "shaw"],
    "O": ["skull", "bone", "blood", "iron", "gut", "tusk"],
    "F": ["fist", "rend", "maw", "bane", "gash", "breaker"],

    # soft endings and maudlin words
    "L": ["ia", "ara", "ora", "ene", "ael", "eth", "ienne", "elle", "wyn"],
    "W": ["Ashes", "Sorrow", "Regret", "Lament", "Vigil", "Dirge", "Quiet Graves",
          "Fading Embers", "the Hollow Bell", "Unlit Candles"],
    "A": ["Grieving", "Hollow", "Forsaken", "Last", "Quiet", "Faded", "Weeping",
          "Unremembered", "Pale"],

    # string values are patterns (literal mode), so symbols can nest
    "s": "<B><v>|<v><C>|<B><v><C>",
    "d": "<D><v>|<D><v><c>",
}

PATTERNS = {
    # first + last name
    "human":    "!<B><v><c>(a|o|en|ric|na) <P><S>",
    "elf":      "!<B><V><c><v>(l|th|riel|wen) !<B><V><c><v>(nor|thir|las|vel)",
    "dwarf":    "!<B><v><C>(in|ur|gar|dok) !(iron|stone|deep|ember|gold|coal)(hammer|beard|forge|anvil|delve)",
    "orc":      "!<D><v><C> !<O><F>",
    "gnome":    "!<B><v><c>(kle|ggle|bin) <k>(wick|sprocket|bottom|cog)",
    "halfling": "!<B><v><c>(o|y|ie) <k>(foot|bottom|brook|barrow)",

    # serious / maudlin
    "mourner":  "!<B><v><c><L> of <W>",
    "epithet":  "!<B><v><c><L> the <A>",
    "widow":    "!<B><V><c>(a|ie|elle) <P><S>",
    "grave":    "!<B><v><C>(an|us|ric|mund) <P><S>",

    # silly
    "cuddly":   "!<m><M> the <i>",
    "stinky":   "<i> <k>",
    "goblin":   "!<d><d> <i>",
}

class NameGen:
    def __init__(self, pattern, symbols=None):
        self.symbols = {**SYMBOLS, **(symbols or {})}
        self._compiled = {k: self._parse(v, 0, True, None)[0]
                          for k, v in self.symbols.items() if isinstance(v, str)}
        self.tree = self._parse(pattern, 0, True, None)[0]

    # --- parsing ---
    def _parse(self, p, i, literal, close):
        alts, seq = [], []
        while i < len(p) and p[i] != close:
            c = p[i]
            if c == "|":
                alts.append(seq)
                seq = []
                i += 1
            elif c in "<(":
                node, i = self._parse(p, i + 1, c == "(", ">" if c == "<" else ")")
                seq.append(node)
            elif c in "!~":
                seq.append(("mod", c))
                i += 1
            else:
                seq.append(("lit" if literal else "sym", c))
                i += 1
        alts.append(seq)
        return ("alt", alts), i + 1  # skip the closing char

    # --- generation ---
    def _seq(self, seq):
        out, pending = [], []
        for item in seq:
            if item[0] == "mod":
                pending.append(item[1])
                continue
            s = self._gen(item)
            for m in reversed(pending):
                s = s[:1].upper() + s[1:] if m == "!" else s[::-1]
            pending = []
            out.append(s)
        return "".join(out)

    def _gen(self, node):
        kind = node[0]
        if kind == "lit":
            return node[1]
        if kind == "sym":
            opt = self.symbols.get(node[1])
            if opt is None:
                return node[1]
            if isinstance(opt, list):
                return random.choice(opt)
            return self._gen(self._compiled[node[1]])
        return self._seq(random.choice(node[1]))

    def generate(self):
        return self._gen(self.tree)

GENERATORS = {name: NameGen(pat) for name, pat in PATTERNS.items()}