import os

class CellMapping:

    def __init__(self,path):
        mappings = []
        with open(path,'r') as file:
            mappings = file.read().split("\n")[:-1]
        self.mappings = [i.split(",") for i in mappings] 
        self.old_cells = [i[0] for i in self.mappings if i[0] != "None"]
        self.insert_cells = [i[1] for i in self.mappings if i[0] == "None"]

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

    def merge(self):
        return [mapping for mapping in self.mappings if mapping[0] != "None" and len(mapping[1:]) >= 2] 

    def split(self):
        split_list,cache = list(),list()
        for mapping in self.mappings:
            old_cell,new_cell = mapping[0],mapping[1:]
            if len(new_cell) == 1 and new_cell[0] != "None":
                if new_cell[0] not in cache:
                    cache.append(new_cell[0])
                else:
                    split_list.append(new_cell[0])
        return [i for i in self.mappings if len(i[1:]) == 1 and i[1] in split_list]

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
    from Config import CURRENT_FILE
    mapping_cache_path = f'{CURRENT_FILE}/mapping_cache'
    mappings = os.listdir(mapping_cache_path)
    mapping = mappings[0]
    cm = CellMapping(f'{mapping_cache_path}/{mapping}')

    id,mo,add,dele,merge,split,move = cm.identical(),cm.modified(),cm.add(),cm.deleted(),cm.merge(),cm.split(),cm.move()
    print(f'{id}\n{mo}\n{add}\n{dele}\n{merge}\n{split}\n{move}')