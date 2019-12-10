import io, json
from sheet.gen.abs_output import AbsNote

"""
Sheet Reader
"""
class SheetReader:
    @staticmethod
    def from_file(filename: str):
        reader = SheetReader()
        reader.file = io.open(filename, "r")
        reader.readinput = reader.file.read()
        reader.read_all()
        return reader
    @staticmethod
    def from_str(info: str):
        reader = SheetReader()
        reader.readinput = info
        reader.read_all()
        return reader
    @staticmethod
    def from_sheets(filename: str) -> list:
        file = io.open(filename, "r")
        sheets: list = [SheetReader.from_str(info) for info in file.read().split("|")]
        return sheets
    def __init__(self):
        pass
    def read_all(self):
        self.read_metadata()
        self.read_notes()

    def read_metadata(self):
        self.data = self.readinput.split("#")
        #print(self.data)
        if len(self.data) != 8:
            raise NotImplementedError
        self.metadata = {
            "author": self.data[0],
            "music_author": self.data[1],
            "version": self.data[2],
            "name": self.data[3],
            "music": self.data[4],
            "offset": float(self.data[5]),
            "level": self.data[6]
        }
    
    def read_notes(self):
        self.note_datas = [[float(i) for i in x.split(",")] for x in self.data[-1].split("\n")]
        self.notes = [AbsNote(*note_data[1:-1], absolutified=True, side=int(note_data[4])) for note_data in self.note_datas]
    def print_sheet(self):
        print(json.dumps(self.metadata))
        print("\n".join([str(x) for x in self.notes]))
        
