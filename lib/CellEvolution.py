from sys import meta_path
print(__name__)
if __name__ == "__main__":
    from CellMapping import CellMapping
    from Config import SPLIT
else:
    from lib.CellMapping import CellMapping
    from lib.Config import SPLIT
import os

def extractName(name):
    name = name.split(SPLIT)[1].split("_")[-1]
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

expand_start = lambda x: [-1 for _ in range(x)]

def cell_evolution_main(name,commits,path):
    mappings = cellmapping(commits,path)
    cell_evolution = list()
    input_cells = mappings[0].old_cells
    for i in range(len(mappings)):
        for cell in input_cells:
            tmp_cell_evolution = list()
            for output in cell_evolution_all(cell,mappings[i:],len(mappings),i):
                tmp_cell_evolution.append(expand_start(i) + [cell]+output)
            cell_evolution += tmp_cell_evolution
        input_cells = mappings[i].insert_cells

    return cell_evolution    

def cell_evolution_all(pointer,mappings,end,count):
    output = list()
    if not mappings: return [[-1 for _ in range(end-count)]]
    result = mappings[0].map(pointer)
    if result[0] == 'None': return [[-1 for _ in range(end-count)]] 
    for re in result:
        re_output = cell_evolution_all(re,mappings[1:],end,count+1)
        re_output = [[re]+i for i in re_output] if re_output else [[re]]
        output += re_output
    return output

def show(output):
    for i in output:
        print('{} {:<5} {:<5} {:<5} {:<5} {:<5}\n'.format(*i))
        
if __name__ == "__main__":
    from Config import CURRENT_FILE,SAVE_FOLDER
    from CellEvolutionAnalyser import CellEvolutionAnalyser
    mapping_cache_path = f'{SAVE_FOLDER}/mapping_cache'
    path = os.listdir(f'{mapping_cache_path}')

    names = all_names(path)
    names_group = group(path,names)

    example = [i for i in list(names_group.items()) if i[0] == 'graphics#graphics'][0]
    output = cell_evolution_main(example[0],example[1],mapping_cache_path)
    show(output)
    ce = CellEvolutionAnalyser(output)
    output = ce.cell_dependents() 
    show(output)
 