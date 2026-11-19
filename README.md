### frand2enemy

A random character generator for Pathfinder 2E.

This will (try to) generate a random character and level it to a random level, applying ability boosts, feats, skill increases as appropriate.  The level randomization uses a log normal distribution such that lvls ~3-5 are most likely.  The intended use case is a random unplanned NPC interaction where a stat sheet is necessary so this is meant to represent the average joe in the street.  That being said, there is always a chance that the town crier might be a hidden Lvl 20 Necromancer.

It uses the json-assets provided by Foundry Virtual Tabletop for relevant game data.

###### What this does NOT do:

Create detailed character descriptions, intricate feat synergies, beautiful character sheets with automated interfaces, ask the DM for permission etc.

###### Current Version:

Random name, ancestry, background, class, level - feat and skill assignments per class description.  Character will generate and print to console.  Saves, skills, HP, senses, perception relatively accurate.  Ability score uses rolling method (4d6, drop lowest)

###### Future Improvements:

- AC, Weapon/Armor Proficiency, 
- Fine-tuning generation/reorganization
- Ability boost from base 10 (non-roll/normal method)
- Ability to generate a character of a specified level (very likely)
- Full Cook Generation Mode - prompts for everything (improbable)

##### Install/Requirements

1. Python 3 - Recommended to run in python virtual evironment (pip install requirements.txt)

2. You will need the json-assets folder from the Foundry VTT github (this version uses 8.7.1).  Place this (un-zipped) in the top level directory.

3. **(Optional) The random name generator uses a variety of methods (at random) to generate a name.  Should all of these methods fail, the generator falls back to a hardcoded list of names stored in a json list at json-assets/name/names.json which you can source or create yourself.  

**This should never be needed, even if all API calls for random name generation fail as a python version of the Skeeto Fantasy Name Generator (which is based on the RinkWorks fantasy name generator) is hardcoded (skeetorink.py).

###### Comments/Disclaimers

This is intended as a fun project, I do not own nor wish to own or profit from anything used here.  Use at your own risk/discretion.

Name Generator APIs/Relevant Links:

IronArachne - https://names.ironarachne.com
RandomAPI - https://randomapi.dev
Skeeto Fantasy Name Generator - https://github.com/skeeto/fantasyname/
RinkWorks Fantasy Name Generator - http://rinkworks.com/namegen/

