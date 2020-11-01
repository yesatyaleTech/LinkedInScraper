from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl.styles import Alignment
from typing import List
from .person import Person

class Spreadsheet:

    def __init__(self, file_path: str):
        self.workbook = Workbook()
        self.path = file_path
        
    def fill_from_people(self, people: List[Person]):
        Everyone = self.workbook.active
        Everyone.title= 'Everyone'
        Everyone['A1'] = 'Names'
        Everyone['B1'] = 'Work Experience'
        Everyone['C1'] = 'URLs'
        Everyone['D1'] = 'Contact'
        for i, person in enumerate(people):
            adex = ('A'+str((i+2)))
            bdex = ('B'+str((i+2)))
            cdex = ('C'+str((i+2)))
            ddex = ('D'+str((i+2)))
            Everyone[adex] = person.name
            Everyone[bdex].alignment = Alignment(wrapText=True) 
            Everyone[bdex] = person.jobtitles
            Everyone[cdex] = person.url
            Everyone[ddex] = person.get_contact_info()
    
    def save(self):
        self.workbook.svae(self.path)