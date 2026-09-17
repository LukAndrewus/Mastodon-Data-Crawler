import json

with open('HashtagData.json', 'r') as file:
    data = json.load(file)

# Prints the number of items in the top-level array or object
print(len(data)) 