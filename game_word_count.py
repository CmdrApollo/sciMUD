import glob
import os
import json

total = 0

for folder in ['locations', 'items']:
    for filename in glob.glob(os.path.join('data', folder, '*.json')):
        with open(filename, 'r') as f:
            data = json.load(f)

            try:
                total += sum([len(r['description'].split(' ')) for r in data['rooms']])
            except KeyError:
                total += sum([len(r['description'].split(' ')) for r in data['items']])

            f.close()
    
print(f"The total word-count for sciMUD is {total} words.")