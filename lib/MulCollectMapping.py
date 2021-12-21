from CheckRepo import RepoCheck
from CollectMapping import CollectMapping
from Config import CURRENT_FILE
import multiprocessing

def process(repo_path):
    try:
        print(f"Start: {repo_path}")
        rpn = RepoCheck(repo_path)
        cm = CollectMapping(rpn)
        cm.run()
        print(f"Collection Done: {repo_path}")
    except Exception as e:
        print(f"Collection Fail: {repo_path}")
        return [repo_path,-1]
    return [repo_path,1] 

def run(repos):
    with multiprocessing.Pool(processes=10) as pool:
        results = pool.map(process,repos)

    with open(f'{CURRENT_FILE}/log_correct_fail.txt','w') as file:
        for i in results:
            file.write(f'{i[0]},{i[1]}\n')

if __name__ == "__main__":
    with open(f"{CURRENT_FILE}/log_correct.txt") as file:
        repos = file.read().split("\n")[:-1]
    run(repos)