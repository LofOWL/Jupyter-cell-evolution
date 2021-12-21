from CollectMapping import mapping_name
from CollectNotebook import name

def get_mappings(output):
    i,j,index = 0,1,0
    result,names = list(),set()
    while j < len(output):
        old_notebook,old_commit = output[i]
        new_notebook,new_commit = output[j]
        result.append(mapping_name(name(old_commit,old_notebook.split(".")[0]),name(new_commit,new_notebook.split(".")[0]),index))
        names.update([old_notebook.split(".")[0],new_notebook.split(".")[0]])
        i += 1
        j += 1
        index += 1
    return result,names