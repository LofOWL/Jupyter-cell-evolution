import os

class CellMapping:

    def __init__(self,path):
        mappings = []
        with open(path,'r') as file:
            mappings = file.read().split("\n")[:-1]
        self.mappings = [i.split(",") for i in mappings] 
        self.old_cells = [i[0] for i in self.mappings if i[0] != "None"]
        self.insert_cells = [i[1] for i in self.mappings if i[0] == "None"]

    def map(self,old_cell):
        old_cell = str(old_cell) if str(old_cell)[-1] != 'm' else str(old_cell)[:-1]
        assert str(old_cell) in self.old_cells, "Old cell out of range"
        for oc in self.mappings:
            if old_cell == oc[0]:
                return oc[1:]
        return 'None'
        
if __name__ == "__main__":
    from Config import CURRENT_FILE
    mapping_cache_path = f'{CURRENT_FILE}/mapping_cache'
    mappings = os.listdir(mapping_cache_path)
    mapping = mappings[0]
    cm = CellMapping(f'{mapping_cache_path}/{mapping}')

    print(cm.old_cells)
    print(cm.insert_cells)
