import io, json
from sheet.gen.abs_output import AbsNote

"""
Sheet Reader
"""
class SheetReader:
    def __init__(self, file):
        self.file = io.open(file, "r")
    def read(self):
        readinput = self.file.read()
        self.data = readinput.split("/")
        #print(self.data)
        if len(self.data) != 7:
            raise NotImplementedError
    def read_all(self):
        self.read()
        self.read_metadata()
        self.read_notes()

    def read_metadata(self):
        self.metadata = {
            "author": self.data[0],
            "music_author": self.data[1],
            "version": self.data[2],
            "name": self.data[3],
            "music": self.data[4],
            "offset": float(self.data[5])
        }
    
    def read_notes(self):
        self.note_datas = [[float(i) for i in x.split(",")] for x in self.data[6].split("\n")]
        self.notes = [AbsNote(*note_data[1:-1], absolutified=True, side=int(note_data[4])) for note_data in self.note_datas]
    def print_sheet(self):
        print(json.dumps(self.metadata))
        print("\n".join([str(x) for x in self.notes]))
        
