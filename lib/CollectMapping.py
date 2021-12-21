from NoteBookMapping import mapping,group
from CheckRepo import RepoCheck
from RepoNotebooks import RepoNotebook
from Data import TEST_REPO,REPOS
from CollectNotebook import name
from Config import CURRENT_FILE,Notebook,CellMapping,SPLIT,SAVE_FOLDER

mapping_name = lambda x,y,index : f'{index}{SPLIT}{x}{SPLIT}{y}.txt'

class CollectMapping:

    def __init__(self,repo_check:RepoCheck):
        self.repo_check = repo_check

    def saveMapping(self,output,old_path,new_path,index):
        name = lambda x: x.split("/")[-1].split(".")[0][:63]
        mname = mapping_name(name(old_path),name(new_path),index)
        with open(f'{CURRENT_FILE}/mapping_cache/{mname}','w') as file:
            for i in output:
                if type(i[1]) != list:
                    file.write(f'{i[0]},{i[1]}\n')
                else:
                    if len(i[1]) == 1:
                        file.write(f'{i[0]},{i[1][0]}m\n')
                    else:
                        file.write(f'{i[0]},{",".join([str(j) for j in i[1]])}\n')

    def getMapping(self,version):
        i,j = 0,1
        index = 0
        while j < len(version):
            old_path = f'{self.repo_check.notebook_cache_path}/{name(version[i][1],version[i][0])}'
            new_path = f'{self.repo_check.notebook_cache_path}/{name(version[j][1],version[j][0])}'
            old,new = Notebook(old_path),Notebook(new_path)
            output = CellMapping(old,new)
            self.saveMapping(output,old_path,new_path,index)
            i += 1
            j += 1
            index += 1

    def run(self):
        _,_,output = group(self.repo_check.data())
        for i in output:
            self.getMapping(i)
            
if __name__ == "__main__":
    rpn = RepoCheck('frnsys#ai_notes')
    cm = CollectMapping(rpn)
    cm.run()
