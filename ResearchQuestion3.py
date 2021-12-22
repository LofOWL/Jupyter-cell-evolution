'''
Research Question 3
How frequently each type of cell-level change happens in the notebook file history?
'''
import os
import sys
sys.path.insert(1,"/home/lofowl/Desktop/CISC834/project/Jupyter-cell-evoluation/lib")

from CheckRepo import RepoCheck
from Config import CURRENT_FILE
from Utils import get_mappings
from CellMapping import CellMapping
from CellTypeSequence import CellSequence


if __name__ == "__main__":
    print("Research Question 3")
    rc = RepoCheck('frnsys#ai_notes')
    _,_,output = rc.group()

    mapping_cache_path = f'{CURRENT_FILE}/mapping_cache'
    mappings = os.listdir(f'{mapping_cache_path}')

    mapping_names,names = get_mappings(output[0])
    mappings = [CellMapping(f'{mapping_cache_path}/{mapping_name}') for mapping_name in mapping_names] 
    output = CellSequence(mappings)
    for i in output: print(i)