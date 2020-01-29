import ast
import json
import os
import pathlib
import re

recipe_file_path = 'recipes_raw.txt'

def load_recipes():
    with open(recipe_file_path) as infile:

        current_entry = []
        entries = []
        for line in infile:
            if line == '{\n' or line == '}':
                pass

            if line.endswith('{\n'):
                # print('item start')
                entries.append(current_entry)
                current_entry = []

            sline = line.strip()
            sline = sline.replace('{', '[')
            sline = sline.replace('}', ']')
            current_entry.append(sline)

            # print(repr(line))

    recipes = {}
    for entry in entries[2:]:
        recipe_entries = {}
        name = entry[0]
        for char in "'[]=":
            name = name.replace(char, '')

        j = "".join(entry[1:])
        j = j[:-3]

        # print(repr(j))

        # Crafting Station
        pattern = r"\['craftStn'] = (\[).*?(])"
        result = re.search(pattern, j).group()
        crafting_station = result.split('=')[1].strip()
        recipe_entries['crafting_station'] = crafting_station

        # Crafting Time
        pattern = r"\['ctime'] = (').*?(')"
        result = re.search(pattern, j).group()
        crafting_time = result.split('=')[1].strip()
        recipe_entries['crafting_time'] = float(crafting_time.replace("'", ''))

        # Skill Needs
        try:
            pattern = r"\['skillNeeds'] = (\[\[).*?(]])"
            result = re.search(pattern, j).group()
            skill_need_list = ast.literal_eval(result.split('=')[1].strip())
            recipe_entries['skill_needs'] = skill_need_list
        except AttributeError as e:
            recipe_entries['skill_needs'] = []

        # Products
        pattern = r"\['products'] = (\[\[).*?(]])"
        result = re.search(pattern, j).group()
        product_list = ast.literal_eval(result.split('=')[1].strip())
        recipe_entries['products'] = product_list

        # Ingredients
        pattern = r"\['ingredients'] = (\[\[).*?(]])"
        result = re.search(pattern, j).group()
        ingredient_list = ast.literal_eval(result.split('=')[1].strip())
        recipe_entries['ingredients'] = ingredient_list

        recipes[name] = recipe_entries

    return recipes


recipes = load_recipes()

print(recipes)

with open('recipes.json', 'w') as file:
    json.dump(recipes, file, indent=4)
