from RepoNotebooks import RepoNotebook
from NoteBookMapping import group
from CollectNotebook import name
from Data import REPOS_PATH,TEST_REPO,REPOS
from Config import SAVE_FOLDER,CURRENT_FILE,SPLIT
from subprocess import getoutput
import pandas as pd
import numpy as np
import re
import os

mapping_name = lambda x,y,index : f'{index}{SPLIT}{x}{SPLIT}{y}.txt'

def get_mappings(output):
    i,j,index = 0,1,0
    result,result_with_names,names = list(),list(),set()
    while j < len(output):
        old_notebook,old_commit = output[i]
        new_notebook,new_commit = output[j]
        mapping_name_text = mapping_name(name(old_commit,old_notebook.split(".")[0])[:63],name(new_commit,new_notebook.split(".")[0])[:63],index)
        result.append(mapping_name_text)
        result_with_names.append([mapping_name_text,name(old_commit,old_notebook),name(new_commit,new_notebook)])
        names.update([old_notebook.split(".")[0],new_notebook.split(".")[0]])
        i += 1
        j += 1
        index += 1
    return result,names,result_with_names

def total_all_mapping_with_name():
    from tqdm import tqdm
    with open(f'{CURRENT_FILE}/log_correct.txt','r') as file:
        file = file.read().split("\n")[:-1]
        results = list()
        for i in tqdm(file):
            try:
                rc = RepoCheck(i)
                results += rc.all_mapping_with_name()
            except:
                pass
    
    with open(f'{CURRENT_FILE}/mapping_with_name.txt','w') as file:
        for i in results:
            file.write(f'{i[0]},{i[1]},{i[2]}\n')

notebook_cache_path = SAVE_FOLDER + "/notebook_cache"
notebook_cache = os.listdir(notebook_cache_path)

mapping_cache_path = SAVE_FOLDER + "/mapping_cache"
mapping_cache = os.listdir(mapping_cache_path)

class RepoCheck:
    
    def __init__(self,repo_name=None):
        self.repo_name = repo_name
        self.data_path = '/media/lofowl/My Passport/1353_file_data'
        self.notebook_cache_path = SAVE_FOLDER + "/notebook_cache"
        self.mapping_cache_path = SAVE_FOLDER + "/mapping_cache"

    def data(self):
        data = pd.read_csv(f'{self.data_path}/{self.repo_name}/{self.repo_name}.csv')
        return data

    def group(self):
        clean,raw,alist = group(self.data())
        return clean,raw,alist

    def is_exist(self,name):
        result = getoutput(f'find -name {name}')
        return len(result) > 1

    def all_mapping_with_name(self):
        _,_,outputs = self.group()
        results = list()
        for output in outputs:
            _,_,result = get_mappings(output)
            results += result
        return results

    def check_mapping(self):
        _,_,outputs = self.group()
        all_mappings = list()
        for output in outputs:
            all_mappings += get_mappings(output)[0]
        return [mapping in mapping_cache for mapping in all_mappings]
        
    def check_notebook(self):
        collect = list()
        data = np.array(self.data()[['commit','file_name','file_rname','file_status']])
        for commit,notebook,rnotebook,type in data:
            if type != "D":
                notebook_n = notebook if not re.match('R\d+',type) else rnotebook
                collect.append(name(commit,notebook_n))

        return [i in notebook_cache for i in collect]

    def run(self):
        from tqdm import tqdm
        log = list()
        for repo in tqdm(REPOS_PATH):
            try:
                rp = RepoNotebook(repo)
                result = self.check(rp)
                if not result:
                    log.append(repo)
            except:
                log.append(repo)

def save(log):
    with open(f'{CURRENT_FILE}/log_correct.txt','w') as file:
        for i in log:
            file.write(f'{i}\n')


if __name__ == "__main__":
    rc = RepoCheck('18F#tech-talks')
    output = rc.check_notebook()
    print(output)
    output = rc.check_mapping()
    print(output)
    print(rc.all_mapping_with_name())

    total_all_mapping_with_name()