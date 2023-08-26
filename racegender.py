import random
import yaml

with open('racegendernames.yaml', 'r') as file:
    race_names = yaml.safe_load(file)

def generate_name(race, gender):
    return random.choice(race_names[race][gender])

core_races = ['Human', 'Elf', 'Dwarf', 'Halfling', 'Gnome', 'Half-Elf', 'Half-Orc', 'Dragonborn']

for race in core_races:
    for gender in ['male', 'female']:
        name = generate_name(race, gender)
        print(f"{race} ({gender}): {name}")

