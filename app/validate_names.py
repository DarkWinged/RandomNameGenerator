import random
import yaml

# Load race and gender-specific names from YAML file
with open('racegendernames.yaml', 'r') as file:
    race_names = yaml.safe_load(file)

# Function to generate a random name based on race and gender
def generate_name(race, gender):
    return random.choice(race_names[race][gender])

# List of core races
core_races = ['Human', 'Elf', 'Dwarf', 'Halfling', 'Gnome', 'Half-Elf', 'Half-Orc', 'Dragonborn']

# Generate and print a name for each race and gender combination
for race in core_races:
    for gender in ['male', 'female']:
        name = generate_name(race, gender)
        print(f"{race} ({gender}): {name}")

