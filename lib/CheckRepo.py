from RepoNotebooks import RepoNotebook
from CollectMapping import mapping
from CollectNotebook import name
from Data import REPOS_PATH
from Config import SAVE_FOLDER,CURRENT_FILE
from subprocess import getoutput
import os

notebook_cache_path = SAVE_FOLDER + "/notebook_cache"

cache = os.listdir(notebook_cache_path)

def find(name):
    os.chdir(notebook_cache_path)
    result = getoutput(f'find -name {name}')
    return len(result) > 1

def check(rpn,cache):
    collect = list()
    all_commits = rpn.all_notebooks_commits()
    for commit in all_commits:
        rpn.set_environment()
        notebooks = rpn.get_notebook_commit_details(commit)
        for notebook in notebooks:
            type = notebook[0]
            if type != "D":
                notebook = notebook[1:]
                notebook = notebook[0] if len(notebook) == 1 else notebook[1]
                collect.append([type,notebook,find(name(commit,notebook))])
    return all(i[2] for i in collect)

from tqdm import tqdm
log = list()
for repo in tqdm(REPOS_PATH):
    try:
        rp = RepoNotebook(repo)
        result = check(rp,cache)
        if not result:
            log.append(repo)
    except:
        log.append(repo)
        
with open(f'{CURRENT_FILE}/log.txt','w') as file:
    for i in log:
        file.write(f'{i}\n')

