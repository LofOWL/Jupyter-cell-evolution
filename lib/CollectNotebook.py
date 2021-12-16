from NoteBookMapping import mapping
from RepoNotebooks import RepoNotebook
from Data import TEST_REPO

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

    current_file = os.path.dirname(os.path.abspath(__file__))+'/cache'

    for notebook,commits in raw.items():
        for commit in commits:
            target = f'{rpn.path}/{notebook}'
            destination = f'{current_file}/{name(commit,check(clean,commit))}'

            rpn.checkout(commit)
            os.system(f'cp "{target}" "{destination}"')

if __name__ == "__main__":
    rpn = RepoNotebook(TEST_REPO)
    CollectNotebook(rpn)
    