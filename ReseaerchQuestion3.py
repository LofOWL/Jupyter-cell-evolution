from sys import meta_path
from lib.Config import CURRENT_FILE
from lib.CellMapping import CellMapping
import os

def extractId(id):
    id = id.split("$")[-1].split(".")[0]
    return id

def extractName(name):
    name = name.split("$")[1].split("_")[-1]
    return name

def extractIndex(index):
    index = index[0]
    return index

def all_names(name):
    names = [extractName(i) for i in name]
    names = set(names)
    names = list(names)
    return names 

def group(path,names):
    names = {name:[] for name in names}
    # group up the names
    for p in path:
        name = extractName(p)
        if names.get(name):
            names[name] = names[name] + [p]
        else:
            names[name] = [p]

    # sort the commit list
    for _,commits in names.items():
        commits.sort(key=lambda x: x[0])

    return names

def cellmapping(commits,path):
    cellmappings = [CellMapping(f'{path}/{commit}') for commit in commits ] 
    return cellmappings

def cell_evolution_main(name,commits,path):
    mappings = cellmapping(commits,path)
    cell_evolution = []
    input_cells = mappings[0].old_cells
    for i in range(len(mappings)):
        mapping = mappings[i]
        cell_evolution += cell_evolution_get(input_cells,mappings[i:],i,len(mappings))        
        input_cells = mapping.insert_cells

    for i in cell_evolution: print(i)

def cell_evolution_get(cells,mappings,start,end):
    result_path = []
    for cell in cells:
        # expand the missing index
        oc = [-1 for _ in range(start)] + [cell]
        pointer = cell
        for mapping in mappings:
            result = mapping.map(pointer)
            if result[0] != "None":
                oc.append(result[0])
                pointer = result[0]
            else:
                # complete the missing index
                oc = oc + [-1 for _ in range(end - len(oc)+1)]
                break
        result_path.append(oc)
    return result_path

if __name__ == "__main__":
    print("Research Question 3")
    mapping_cache_path = f'{CURRENT_FILE}/mapping_cache'
    path = os.listdir(f'{mapping_cache_path}')

    names = all_names(path)
    names_group = group(path,names)

    print(names_group)
    example = list(names_group.items())[1]
    cell_evolution_main(example[0],example[1],mapping_cache_path)

 