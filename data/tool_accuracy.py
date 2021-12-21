
import os
import sys

sys.path.insert(1,'/home/lofowl/Desktop/CISC834/project/Jupyter-code-tracker/mapping/notebook/')
from notebook import Notebook

with open('/home/lofowl/Desktop/CISC834/project/Jupyter-cell-evoluation/lib/mapping_with_name.txt','r') as file:
    mappings = file.read().split("\n")[:-1]
    mappings = [i.split(",") for i in mappings]

def get_name(mapping):
    for mapp in mappings:
        if mapp[0] == mapping:
            return mapp[1:]
    return None


notebook_cache_path = '/media/lofowl/My Passport/CISC834/notebook_cache'
notebook_cache = os.listdir(notebook_cache_path)

def read(path):
    with open(path,'r') as file:
        file = file.read().split("\n")[:-1]
    return file

if __name__ == "__main__":
    print("test")
    all_datas = [i for i in os.listdir('/home/lofowl/Desktop/CISC834/project/Jupyter-cell-evoluation/data') if '.txt' in i and i not in ['merged.txt','splited.txt']]
    data = {i.split(".")[0]:read(f'/home/lofowl/Desktop/CISC834/project/Jupyter-cell-evoluation/data/{i}') for i in all_datas}
    evaluates = {i.split(".")[0]:[] for i in all_datas}

    for name,paths in data.items():
        evaluate = list()
        for value in paths:
            value = value.split(",")
            print(value)
            old_notebook,new_notebook = get_name(value[0])

            old_notebook_path = f'{notebook_cache_path}/{old_notebook}'
      
            new_notebook_path = f'{notebook_cache_path}/{new_notebook}'

            print(f'{old_notebook_path}\n{new_notebook_path}')
            print("#"*100)
            old_index = value[1]
            o_notebook = Notebook(old_notebook_path)
            o_notebook.show_with_index(old_index)
            print("#"*100)
            new_indexs = value[2:]
            n_notebook = Notebook(new_notebook_path)
            for new_index in new_indexs:
                new_index = new_index if 'm' not in new_index[-1] else new_index[:-1]
                n_notebook.show_with_index(new_index)
            print(value[1:])            

            evaluate.append(input("Enter value: "))
        evaluates[name] = evaluate
    
    with open('/home/lofowl/Desktop/CISC834/project/Jupyter-cell-evoluation/log_evaluate.txt','w') as file:
        for name,paths in evaluates.items():
            file.write(f'{name}:{",".join([str(i) for i in paths])}\n')
        



