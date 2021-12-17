

class CellEvolutionAnalyser:

    def __init__(self,alists=[]):
        self.lists = alists

    def cell_dependents(self):
        x,y = len(self.lists[0]),len(self.lists)
        result = list()
        for j in range(y):
            row = list()
            for i in range(x):
                row.append(self.cell_dependent(i,j))
            result.append(row)
        return result

    def cell_dependent(self,version,cell_index):
        if self.lists[cell_index][version] == -1 : return -1
        history = self.lists[cell_index][:version]
        count_n1 = len([i for i in history if i == -1])
        return count_n1

    def is_same_position(self,alist):
        return len(set(alist)) == 1

    def is_identical(self,alist):
        return all('m' not in i for i in alist)

    def is_exist_all(self,alist):
        return len(i for i in alist if i != -1) == 0

    def is_exist_head(self,alist):
        return alist[0] != -1 and alist[-1] == -1

    def is_exist_end(self,alist):
        return alist[0] == -1 and alist[-1] != -1

    def is_exist_mid(self,alist):
        return alist[0] == -1 and alist[-1] == -1

    def len_modified(self,alist):
        return len(i for i in alist if 'm' in i)

    def len_position_change(self,alist):
        return len(set([i if i[-1] != 'm' else i[:-1] for i in alist if type(i) == str]))

    def len_exist(self,alist):
        return len(i for i in alist if i != -1)

if __name__ == "__main__":
    ce = CellEvolutionAnalyser()