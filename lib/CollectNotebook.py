from NoteBookMapping import mapping
from RepoNotebooks import RepoNotebook
from Data import REPOS_PATH, TEST_REPO,REPOS
from Config import SAVE_FOLDER,CURRENT_FILE
import os

name = lambda commit,notebook_name: f"{commit}_{notebook_name.replace('/','#')}"

def save(rpn,notebook,commit):
    target = f'{rpn.path}/{notebook}'
    destination = f'{SAVE_FOLDER}/notebook_cache/{name(commit,notebook)}'
    rpn.checkout(commit)
    os.system(f'cp "{target}" "{destination}"')

def CollectNotebook(rpn):
    all_commits = rpn.all_notebooks_commits()

    for commit in all_commits:
        notebooks = rpn.get_notebook_commit_details(commit)
        for notebook in notebooks:
            type = notebook[0]
            notebook = notebook[1:]
            notebook = notebook[0] if len(notebook) == 1 else notebook[1]
            save(rpn,notebook,commit) 

if __name__ == "__main__":
    repo = '/media/lofowl/My Passport/1353_notebook_projects/18F#tech-talks/tech-talks'
    repo = REPOS_PATH[1]
    print(repo)
    rpn = RepoNotebook(repo)
    CollectNotebook(rpn)

