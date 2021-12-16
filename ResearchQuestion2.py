from lib.Config import CURRENT_FILE
import os

def count_missing(path):
    with open(path,'r') as file:
        mapping = file.read().split("\n")[:-1]
        mapping = [i.split(',') for i in mapping]

    all_new_cells = [int(j) if j[-1] != 'm' else int(j[:-1]) for i in mapping for j in i[1:] if j != 'None']  
    total = max(all_new_cells) + 1
    new_cell = len([i for i in mapping if i[0] == "None"])

    return total,new_cell, new_cell / total 

if __name__ == "__main__":
    print("Research Question 2")
    mapping_cache = f'{CURRENT_FILE}/mapping_cache'
    all_mapping = os.listdir(mapping_cache)

    a,b,c = count_missing(f'{mapping_cache}/{all_mapping[0]}')
    print(f'{a} {b} {c}')