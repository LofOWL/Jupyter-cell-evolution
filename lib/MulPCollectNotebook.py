from CollectNotebook import CollectNotebook
from RepoNotebooks import RepoNotebook
from Data import REPOS_PATH
from Config import CURRENT_FILE
import multiprocessing

def process(repo_path):
    try:
        rpn = RepoNotebook(repo_path)
        CollectNotebook(rpn)
    except Exception as e:
        return [repo_path,e]
    return [repo_path,1] 

if __name__ == "__main__":
    repo = REPOS_PATH[176]
    with multiprocessing.Pool(processes=16) as pool:
        results = pool.map(process,REPOS_PATH[175:])
    
    with open(f'{CURRENT_FILE}/log.txt','w') as file:
        for i,j in results:
            file.write(f'{i},{j}\n')
    print(results)