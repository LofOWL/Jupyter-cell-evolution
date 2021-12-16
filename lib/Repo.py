from Data import *
import os
import sys
import subprocess

class Repo:

    def __init__(self,path):
        self.path = path
        self.set_environment()
        self.set_master()

    def checkout(self,commit):
        os.system(f'git checkout -f {commit}')        

    def set_master(self):
        assert self.current_path() == self.path, 'Is not in the repo'
        os.system('git checkout -f master')
    
    def set_environment(self):
        assert self.path, "Path not exist"      
        os.chdir(self.path)
    
    def current_path(self):
        os.system('pwd')
        return subprocess.getoutput('pwd')

if __name__ == "__main__":

    rp = Repo(TEST_REPO)
    print(rp.path)
    rp.set_environment()
    rp.set_master()