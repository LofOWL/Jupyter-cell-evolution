from NoteBookMapping import mapping
from RepoNotebooks import RepoNotebook
from Data import TEST_REPO
from CollectNotebook import name

import os
import sys
sys.path.insert(1,'/home/lofowl/Desktop/CISC834/project/Jupyter-code-tracker/other_tools')
from tool import CellMapping,OLD_PATH,NEW_PATH
from notebook import Notebook

current_file = os.path.dirname(os.path.abspath(__file__))

mapping_name = lambda x,y : f'{x}${y}.txt'

def saveMapping(output,old_path,new_path):
    name = lambda x: x.split("/")[-1].split(".")[0]
    mname = mapping_name(name(old_path),name(new_path))
    with open(f'{current_file}/mapping_cache/{mname}','w') as file:
        for i in output:
            if type(i[1]) != list:
                file.write(f'{i[0]},{i[1]}\n')
            else:
                if len(i[1]) == 1:
                    file.write(f'{i[0]},{i[1][0]}m\n')
                else:
                    file.write(f'{i[0]},{",".join(i[1])}\n')



def getMapping(notebook_name,commits):
    i,j = 0,1
    mapping_output = list()
    while j < len(commits):
        old_path = f'{current_file}/cache/{name(commits[i],notebook_name)}'
        new_path = f'{current_file}/cache/{name(commits[j],notebook_name)}'
        print(old_path)
        print(new_path)
        old,new = Notebook(old_path),Notebook(new_path)
        output = CellMapping(old,new)
        mapping_output.append(output)
        saveMapping(output,old_path,new_path)
        i += 1
        j += 1
    return mapping_output

def main(output):
    print(output)
    mapping_output = list()
    for notebook_name,commits in output.items():
        if notebook_name == 'graphics/graphics.ipynb':
            mapping_output += getMapping(notebook_name,commits)
    for i in mapping_output:
        for j in i:
            print(j)

if __name__ == "__main__":
    rpn = RepoNotebook(TEST_REPO)
    output = rpn.all_notebooks()
    clean,_ = mapping(output)
    print(clean)

    main(clean)

    