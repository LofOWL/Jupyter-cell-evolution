import os
import sys

def getRepoPath(name):
    _,last = name.split("#")
    return f'{REPO_PATH}/{name}/{last}'

REPO_PATH = '/media/lofowl/My Passport/1353_notebook_projects'

REPOS = os.listdir(REPO_PATH)

TEST_REPO = getRepoPath(REPOS[0])

if __name__ == "__main__":
    repo = REPOS[0]

    repo_path  = getRepoPath(repo)