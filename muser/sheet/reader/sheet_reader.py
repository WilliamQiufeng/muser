import io, json
from sheet.gen.abs_output import AbsNote
from sheet.actions import *

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
    def from_obj(info: dict):
        reader = SheetReader()
        reader.data = info
        reader.read_notes()
        return reader
    @staticmethod
    def from_sheets(filename: str) -> list:
        file = io.open(filename, "r")
        sheets: list = [SheetReader.from_obj(info) for info in json.loads(file.read())]
        return sheets
    def __init__(self):
        pass
    def read_all(self):
        self.read_metadata()
        self.read_notes()

    def read_metadata(self):
        self.data = json.loads(self.readinput)
    
    def read_notes(self):
        self.notes = [Actions.fromArgs(note_data) for note_data in self.data["notes"]]
        # self.print_sheet()
    def print_sheet(self):
        print(json.dumps(self.data, indent=4))
        
