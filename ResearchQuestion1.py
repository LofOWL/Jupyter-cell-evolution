'''
Research Question 1:
How accurate is our proposed cell mapping approach?
'''
from numpy.lib.function_base import delete
from numpy.lib.shape_base import split
from lib.Config import SAVE_FOLDER
from lib.CellMapping import CellMapping
from random import sample
import os
from varname import nameof

path = f'{SAVE_FOLDER}/mapping_cache'

all_mappings = os.listdir(path)

add_name = lambda mapping,lists: [(mapping,i) for i in lists]

def select_20(alist,name):
    alist = sample(alist,20)
    with open(f'./data/{name}.txt','w') as file:
        for i in alist:
            file.write(f'{i[0]},{",".join([str(i) for i in i[1]])}\n')

if __name__ == "__main__":
    from tqdm import tqdm
    added,deleted,modified,moved,splited,merged = list(),list(),list(),list(),list(),list()
    for mapping in tqdm(all_mappings):
        cm = CellMapping(f'{path}/{mapping}')
        added += add_name(mapping,cm.add())
        deleted += add_name(mapping,cm.deleted())
        modified += add_name(mapping,cm.modified())
        moved += add_name(mapping,cm.move())
        splited += add_name(mapping,cm.split())
        merged += add_name(mapping,cm.merge())
    
    print(f'add: {len(added)}\ndelete: {len(deleted)}\nmodified: {len(modified)}\nmoved: {len(moved)}\nsplited: {len(splited)}\nmerged: {len(merged)}')

    for name in ['added','deleted','modified','moved','splited','merged']:
        select_20(eval(name),name)
    