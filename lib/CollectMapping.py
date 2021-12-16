from NoteBookMapping import mapping
from RepoNotebooks import RepoNotebook
from Data import TEST_REPO
from CollectNotebook import name

from Config import CURRENT_FILE,Notebook,CellMapping

mapping_name = lambda x,y,index,id : f'{index}${x}${y}${id}.txt'

def saveMapping(output,old_path,new_path,index,id):
    name = lambda x: x.split("/")[-1].split(".")[0]
    mname = mapping_name(name(old_path),name(new_path),index,id)
    with open(f'{CURRENT_FILE}/mapping_cache/{mname}','w') as file:
        for i in output:
            if type(i[1]) != list:
                file.write(f'{i[0]},{i[1]}\n')
            else:
                if len(i[1]) == 1:
                    file.write(f'{i[0]},{i[1][0]}m\n')
                else:
                    file.write(f'{i[0]},{",".join(i[1])}\n')

def getMapping(notebook_name,commits,id):
    i,j = 0,1
    mapping_output = list()
    index = 0
    while j < len(commits):
        old_path = f'{CURRENT_FILE}/cache/{name(commits[i],notebook_name)}'
        new_path = f'{CURRENT_FILE}/cache/{name(commits[j],notebook_name)}'
        old,new = Notebook(old_path),Notebook(new_path)
        output = CellMapping(old,new)
        mapping_output.append(output)
        saveMapping(output,old_path,new_path,index,id)
        i += 1
        j += 1
        index += 1
    return mapping_output

def main(output,id):
    mapping_output = list()
    for notebook_name,commits in output.items():
        mapping_output += getMapping(notebook_name,commits,id)

if __name__ == "__main__":
    rpn = RepoNotebook(TEST_REPO)
    output = rpn.all_notebooks()
    clean,_ = mapping(output)
    print(clean)

    main(clean,rpn.id)

    