from CellMapping import CellMapping
from Config import SPLIT
from Utils import get_mappings
import os

def extractName(name):
    name = name.split(SPLIT)[1].split("_")[-1]
    return name

def extractIndex(index):
    index = index[0]
    return index

expand_start = lambda x: [-1 for _ in range(x)]

def cell_evolution_main(name,mappings):
    mappings = mappings
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

if __name__ == "__main__":
    from Config import CURRENT_FILE,SAVE_FOLDER
    from CheckRepo import RepoCheck
    from CellEvolutionAnalyser import CellEvolutionAnalyser
    rc = RepoCheck('frnsys#ai_notes')
    _,_,output = rc.group()

    mapping_cache_path = f'{CURRENT_FILE}/mapping_cache'
    mappings = os.listdir(f'{mapping_cache_path}')

    mapping_names,names = get_mappings(output[0])
    '''
    graphics#graphics
    ['1@$376b094aa6a3f4572774e15e7659af9eb82981b3_graphics#graphics@$8336e016614e784c0ca8820574798ab3e8606732_graphics#graphics.txt', '2@$8336e016614e784c0ca8820574798ab3e8606732_graphics#graphics@$5d3bd8305653daca3ece76a60d3162bf70da0bb2_graphics#graphics.txt', '3@$5d3bd8305653daca3ece76a60d3162bf70da0bb2_graphics#graphics@$759f9bb740cfbb272f1b35dfc78f918f89b68674_graphics#graphics.txt', '4@$759f9bb740cfbb272f1b35dfc78f918f89b68674_graphics#graphics@$ac60e19a29d7fddd38418441f110d1437a7cb0e4_graphics#graphics.txt', '5@$ac60e19a29d7fddd38418441f110d1437a7cb0e4_graphics#graphics@$87d848d425ed907e85b194b5c0f896e4a153bee9_graphics#graphics.txt']
    '''
    mappings = [CellMapping(f'{mapping_cache_path}/{mapping_name}') for mapping_name in mapping_names] 
    output = cell_evolution_main(names,mappings)
    for i in output: print(i) 
    ce = CellEvolutionAnalyser(output)
    output = ce.cell_dependents() 
 