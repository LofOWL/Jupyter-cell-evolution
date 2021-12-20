from RepoNotebooks import RepoNotebook
from NoteBookMapping import group
from CollectNotebook import name
from Data import REPOS_PATH,TEST_REPO,REPOS
from Config import SAVE_FOLDER,CURRENT_FILE
from subprocess import getoutput
import pandas as pd
import numpy as np
import re
import os

notebook_cache_path = SAVE_FOLDER + "/notebook_cache"
notebook_cache = os.listdir(notebook_cache_path)

class RepoCheck:
    
    def __init__(self,repo_name=None):
        self.repo_name = repo_name
        self.data_path = '/media/lofowl/My Passport/1353_file_data'
        self.notebook_cache_path = SAVE_FOLDER + "/notebook_cache"

    def data(self):
        data = pd.read_csv(f'{self.data_path}/{self.repo_name}/{self.repo_name}.csv')
        return data

    def group(self):
        clean,raw = group(self.data())
        return clean,raw

    def is_exist(self,name):
        result = getoutput(f'find -name {name}')
        return len(result) > 1

    def check(self):
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
    from tqdm import tqdm
    #logs = list()
    #for repo in tqdm(REPOS):
    #    try:
    #        rc = RepoCheck(repo)
    #        output = rc.check()
    #        if all(output): logs.append(repo)
    #    except:
    #        pass
    
    rc = RepoCheck('mbernico#CS570')
    output = rc.check()
    print(output)