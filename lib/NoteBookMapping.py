from Data import TEST_REPO
from RepoNotebooks import RepoNotebook
import numpy as np
import re

def mapping(output):
    notebook_mapping = dict()
    rename_notebook = list()
    while output:
        notebook = output.pop(0)
        if not re.match('R\d+',notebook[2]):
            notebook_commits = notebook_mapping.get(notebook[3])
            if notebook_commits:
                notebook_mapping[notebook[3]] = [notebook[0]] + notebook_commits
            else:
                notebook_mapping[notebook[3]] = [notebook[0]] 
        else:
            name,rename = notebook[3],notebook[4]
            isRename = False
            for i in range(len(rename_notebook)):
                if rename_notebook[i][-1] == name:
                    rename_notebook[i] = rename+notebook[i] + [rename]
                    isRename = True
                    break
            if not isRename: rename_notebook.append([name,rename])

    # merge all the notebook with same name
    output,all_mapping = list(),list()
    for rename in rename_notebook:
        commits,mapping = [],[]
        for i in rename:
            commit  = notebook_mapping.get(i)
            if commit: 
                commits += commit 
                mapping += [(i,com) for com in commit]
        output.append((rename[-1],commits))
        all_mapping.append(mapping)

    # all the rename notebooks 
    all_rename_notebook = [j for i in rename_notebook for j in i]
    filter_notebook = [i for i in notebook_mapping.items() if i[0] not in all_rename_notebook]
    all_mapping_remainder = [[(name,commit) for commit in commits] for name,commits in notebook_mapping.items() if name not in all_rename_notebook]

    # merge all the notebooks
    output = filter_notebook + output
    all_mapping = all_mapping + all_mapping_remainder

    return dict(output),dict(notebook_mapping),all_mapping


def group(data):
    convert_data = [[i[0],i[1],i[5],i[3]] if 'R' not in i[5] else [i[0],i[1],i[5],i[3],i[4]] for i in np.array(data) if 'D' not in i[5]]
    return mapping(convert_data)

if __name__ == "__main__":
    rpn = RepoNotebook(TEST_REPO)
    TEST_OUTPUT = rpn.all_notebooks()
    print("NoteBookMapping")
    for i in TEST_OUTPUT: print(i)
    clean,rw = mapping(TEST_OUTPUT)
    for i in clean.items(): print(i)