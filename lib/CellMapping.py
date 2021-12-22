import os
from Data import IDENTICAL,MERGE,MODIFIED,MOVE,SPLIT
from Utils import convert

class CellMapping:

    def __init__(self,path):
        mappings = []
        with open(path,'r') as file:
            mappings = file.read().split("\n")[:-1]
        self.mappings = [i.split(",") for i in mappings] 
        self.old_cells = [i[0] for i in self.mappings if i[0] != "None"]
        self.new_cells = [j for i in self.mappings if i[1] != "None" for j in i[1:]]
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
        return [mapping for mapping in self.mappings if len(mapping) == 2 and 'm' not in mapping[1][-1] and mapping[1] != "None" and mapping[0] != "None"]

    def modified(self):
        return [mapping for mapping in self.mappings if len(mapping) == 2 and 'm' in mapping[1][-1] and mapping[1] != "None"]

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

    def cell_change_type(self):
        cct = {i:None for i in self.old_cells}

        identical = [i[0] for i in self.identical()]
        modified = [i[0] for i in self.modified()]
        move = [i[0] for i in self.move()]
        merge = [i[0] for i in self.merge()]
        split = [i[0] for i in self.split()]
        for i in self.old_cells:
            if i in merge: cct[i] = MERGE
            elif i in split: cct[i] = SPLIT
            elif i in move: cct[i] = MOVE
            elif i in modified: cct[i] = MODIFIED
            elif i in identical: cct[i] = IDENTICAL

        return cct 

    def modified_position(self):
        old_cells_len = max([int(i) for i in self.old_cells]) + 1
        new_cells_len = max([int(convert(i)) for i in self.new_cells]) + 1

        identical = [int(i[0]) for i in self.identical()]
        identical_position = [i/old_cells_len for i in identical]
        
        change = self.modified() + self.split() + self.merge() + self.move()
        change = list(set([int(i[0]) for i in change]))
        change_position = [i/old_cells_len for i in change]

        modified = [int(i[0]) for i in self.modified()]
        modified_position = [i/old_cells_len for i in modified]

        split = [int(i[0]) for i in self.split()]
        split_position = [i/old_cells_len for i in split]

        merge = [int(i[0]) for i in self.merge()]
        merge_position = [i/old_cells_len for i in merge]

        move = [int(i[0]) for i in self.move()]
        move_position = [i/old_cells_len for i in move]

        add = [int(i[1]) for i in self.add()]
        add_position = [i/new_cells_len for i in add]

        delete = [int(i[0]) for i in self.deleted()]
        delete_position = [i/old_cells_len for i in delete]

        return identical_position,modified_position,split_position,merge_position,move_position,add_position,delete_position 


if __name__ == "__main__":
    from Config import SAVE_FOLDER,CURRENT_FILE
    mapping_path = CURRENT_FILE + '/mapping_cache'
    cm = CellMapping(f'{mapping_path}/1@$376b094aa6a3f4572774e15e7659af9eb82981b3_graphics#graphics@$8336e016614e784c0ca8820574798ab3e8606732_graphics#graphics.txt')
    cm.show()
    cm.cell_change_type()
    cm.modified_position()

    