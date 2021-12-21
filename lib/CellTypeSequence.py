from CellMapping import CellMapping
from CellEvolution import cell_evolution_main
from CheckRepo import RepoCheck
from Config import CURRENT_FILE
from Utils import get_mappings
from Data import NONE
import os


def CellSequence(mappings):
    output = cell_evolution_main('test',mappings)
    c2t = [mapping.cell_change_type() for mapping in mappings]

    sequence_list = list()
    x,y = len(output[0]),len(output)
    for j in range(y):
        row = list()
        for i in range(x-1):
            if type(output[j][i]) != int:
                value = output[j][i] if 'm' not in output[j][i][-1] else output[j][i][:-1]
            else:
                value = str(output[j][i])
            ct = c2t[i].get(value) 
            ct = ct if ct != None else NONE
            row.append(ct)
        sequence_list.append(row)
    return sequence_list

if __name__ == "__main__":
    rc = RepoCheck('frnsys#ai_notes')
    _,_,output = rc.group()

    mapping_cache_path = f'{CURRENT_FILE}/mapping_cache'
    mappings = os.listdir(f'{mapping_cache_path}')

    mapping_names,names = get_mappings(output[0])
    mappings = [CellMapping(f'{mapping_cache_path}/{mapping_name}') for mapping_name in mapping_names] 
    output = CellSequence(mappings)
    for i in output: print(i)