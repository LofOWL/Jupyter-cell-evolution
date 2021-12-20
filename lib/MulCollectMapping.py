from CollectNotebook import CollectNotebook
from RepoNotebooks import RepoNotebook
from Data import REPOS_PATH
from Config import CURRENT_FILE
import multiprocessing

def process(repo_path):
    try:
        print(f"Start: {repo_path}")
        rpn = RepoNotebook(repo_path)
        CollectNotebook(rpn)
        print(f"Collection Done: {repo_path}")
    except Exception as e:
        print(f"Collection Fail: {repo_path}")
        return [repo_path,e]
    return [repo_path,1] 

def run(repos):
    with multiprocessing.Pool(processes=16) as pool:
        results = pool.map(process,repos)
    
    with open(f'{CURRENT_FILE}/collect_log.txt','w') as file:
        for i,j in results:
            file.write(f'{i},{j}\n')
    print(results)

if __name__ == "__main__":
    with open(f"{CURRENT_FILE}/log.txt") as file:
        repos = file.read().split("\n")[:-1]

    run(repos)