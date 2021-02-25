import yaml

with open("./data.yaml", 'r') as stream:
    try:
        #print(stream)
        data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

elements =[]
for key, v in data.items():
    elements.append(key)
#print(elements)
for el in elements:
    element = data[el]
    #z = element['z']
    name = element['name']
    symbol = el
    print(f'("{el}", "{name}"),')