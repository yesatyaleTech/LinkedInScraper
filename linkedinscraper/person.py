from typing import List


class Person:
    def __init__(self, name: str, url: str):
        self.name: str = name
        self.url: str = url
        self.jobhist: str = ''
        self.contactinfo: List[str] = []

    def add_jobhistory(self, history: str):
        self.jobhistory += history

    def add_contactinfo(self, contactinfo: str):
        self.contactinfo.append(contactinfo)

    def get_contactinfo(self):
        s: str = ''
        for c in self.contactinfo:
            s += (c + '\n')
