import Repo
from Data import *
import subprocess
import re
from datetime import datetime

MERGE = lambda notebooks,time,commit: [[commit,time]+notebook for notebook in notebooks]

class RepoNotebook(Repo.Repo):

    def __init__(self,path):
        super().__init__(path)
        self.id = str(hash(self.path))[1:13]

    def all_notebooks_commits(self):
        output = subprocess.getoutput('git log --pretty=%H --follow *.ipynb')
        return output.split("\n")

    def get_notebook_commit_details(self,commit):
        output = subprocess.getoutput(f'git show --name-status --pretty="" {commit}')
        output = output.split("\n")
        output = list(filter(lambda x:'.ipynb' in x,output))
        output = list(map(lambda x: x.split('\t'),output))
        return output

    def get_commit_time(self,commit):
        output = subprocess.getoutput(f'git show -s --format=%ci {commit}')
        output = output[:-6]
        #output = datetime.strptime(output,"%Y-%m-%d %H:%M:%S")
        return output 


    def all_notebooks(self):
        notebook_commits = self.all_notebooks_commits()
        output = list()
        for commit in notebook_commits:
            notebooks = self.get_notebook_commit_details(commit)
            time = self.get_commit_time(commit)
            output += MERGE(notebooks,time,commit)
        return output
 
if __name__ == "__main__":
    rpn = RepoNotebook(TEST_REPO)
    rpn.all_notebooks()
    print(rpn.id)
    

    