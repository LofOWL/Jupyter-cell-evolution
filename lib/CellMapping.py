import os

class CellMapping:

    def __init__(self,path):
        mappings = []
        with open(path,'r') as file:
            mappings = file.read().split("\n")[:-1]
        self.mappings = [i.split(",") for i in mappings] 
        self.old_cells = [i[0] for i in self.mappings if i[0] != "None"]
        self.insert_cells = [i[1] for i in self.mappings if i[0] == "None"]

    def show(self):
        for mapping in self.mappings:
            print(mapping)

    def convert2int(self,astr):
        return int(astr) if str(astr)[-1] != "m" else int(str(astr)[:-1])

    def map(self,old_cell):
        old_cell = str(old_cell) if str(old_cell)[-1] != 'm' else str(old_cell)[:-1]
        assert str(old_cell) in self.old_cells, "Old cell out of range"
        for oc in self.mappings:
            if old_cell == oc[0]:
                return oc[1:]
        return 'None'


    def mapNew(self,new_cell):
        for oc in self.mappings:
            if any(new_cell in nc for nc in oc[1:]):
                return oc[0]
        return 'None'

    def identical(self):
        return [mapping for mapping in self.mappings if mapping[0] != "None" and len(mapping[1:]) == 1 and 'm' not in mapping[1]]

    def modified(self):
        return [mapping for mapping in self.mappings if mapping[0] != "None" and len(mapping[1:]) == 1 and 'm' in mapping[1]]

    def add(self):
        return [mapping for mapping in self.mappings if mapping[0] == "None"] 

    def deleted(self):
        return [mapping for mapping in self.mappings if mapping[1] == "None"] 

    def split(self):
        return [mapping for mapping in self.mappings if mapping[0] != "None" and len(mapping[1:]) >= 2] 

    def merge(self):
        convert = lambda x: (str(x) if 'm' not in x[-1] else str(x[:-1]))
        merge_list,cache = list(),list()
        for mapping in self.mappings:
            old_cell,new_cells = mapping[0],mapping[1:]
            for new_cell in new_cells:
                if new_cell != "None":
                    if not any(convert(new_cell) == convert(i) for i in cache):
                        cache.append(new_cell)
                    else:
                        merge_list.append(new_cell)
        return [i for i in self.mappings if any(convert(i) == convert(j) for i in i[1:] for j in merge_list)]

    def move(self):
        move_list = list()
        for old_cell in self.old_cells:
            old_cell = int(old_cell)
            new_cells = self.map(old_cell) 
            for new_cell in new_cells:
                if new_cell != "None":
                    new_cell = int(new_cell) if str(new_cell)[-1] != 'm' else int(new_cell[:-1])
                    pre_new_cells = [str(i) for i in range(new_cell)]
                    pre_new_cells_map = [int(self.mapNew(i)) for i in pre_new_cells if self.mapNew(i) != "None"]
                    if not all(old_cell > i for i in pre_new_cells_map):
                        move_list.append([old_cell]+new_cells)
        return move_list
                


if __name__ == "__main__":
    from Config import SAVE_FOLDER
    mapping_path = SAVE_FOLDER + '/mapping_cache'
    cm = CellMapping(f'{mapping_path}/15@$61a830c36bd1e8c69697a57ae614c9b6900598b7_examples#reflectometry@$302e717b05b54ebe3bebc9966b80a4ca977efa32_examples#reflectometry.txt')
    cm.show()
    print(cm.merge())