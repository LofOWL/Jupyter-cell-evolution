from sys import meta_path
from lib.CellEvolution import all_names,group,cell_evolution_main
from lib.Config import CURRENT_FILE
from lib.CellEvolutionAnalyser import CellEvolutionAnalyser
import os


def show(output):
    for i in output:
        print('{} {:<5} {:<5} {:<5} {:<5} {:<5} {:<5}\n'.format(*i))
        
if __name__ == "__main__":
    print("Research Question 3")
    mapping_cache_path = f'{CURRENT_FILE}/mapping_cache'
    path = os.listdir(f'{mapping_cache_path}')

    names = all_names(path)
    names_group = group(path,names)

    print(names_group)
    example = [i for i in list(names_group.items()) if i[0] == 'graphics#graphics'][0]
    print(example)
    output = cell_evolution_main(example[0],example[1],mapping_cache_path)
    ce = CellEvolutionAnalyser(output)
    output = ce.cell_dependents() 
    show(output)
 