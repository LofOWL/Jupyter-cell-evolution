from NoteBookMapping import mapping
from RepoNotebooks import RepoNotebook
from Data import REPOS_PATH, TEST_REPO,REPOS
from Config import SAVE_FOLDER,CURRENT_FILE
import os

name = lambda commit,notebook_name: f"{commit}_{notebook_name.replace('/','#')}"

def check(clean,commit):
    for notebook,commits in clean.items():
        if commit in commits:
            return notebook
    raise Exception("commit not exists")

def CollectNotebook(rpn):
    output = rpn.all_notebooks()
    clean,raw = mapping(output)

    for notebook,commits in raw.items():
        for commit in commits:
            target = f'{rpn.path}/{notebook}'
            destination = f'{SAVE_FOLDER}/notebook_cache/{name(commit,check(clean,commit))}'
            print(commit)
            rpn.checkout(commit)
            os.system(f'cp "{target}" "{destination}"')

if __name__ == "__main__":
    repo = '/media/lofowl/My Passport/1353_notebook_projects/chengsoonong#crowdastro/crowdastro'
    rpn = RepoNotebook(repo)
    CollectNotebook(rpn)

