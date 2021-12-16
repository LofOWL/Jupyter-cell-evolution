from Data import TEST_REPO
from RepoNotebooks import RepoNotebook

def mapping(output):
    notebook_mapping = dict()
    rename_notebook = list()
    while output:
        notebook = output.pop(0)
        if notebook[2] != 'R100':
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
    output = list()
    for rename in rename_notebook:
        commits = []
        for i in rename:
            commit  = notebook_mapping.get(i)
            if commit: commits += commit 
        output.append((rename[-1],commits))

    # all the rename notebooks 
    all_rename_notebook = [j for i in rename_notebook for j in i]
    filter_notebook = [i for i in notebook_mapping.items() if i[0] not in all_rename_notebook]

    # merge all the notebooks
    output = filter_notebook + output

    return dict(output),dict(notebook_mapping)

if __name__ == "__main__":
    rpn = RepoNotebook(TEST_REPO)
    TEST_OUTPUT = rpn.all_notebooks()
    print("NoteBookMapping")
    for i in TEST_OUTPUT: print(i)
    result = mapping(TEST_OUTPUT)
    for i in result.items(): print(i)