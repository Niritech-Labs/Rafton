# Copyright (C) 2024-2025 Niritech Labs
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
import sys,os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PySide6.QtWidgets import QLineEdit,QFileSystemModel
#from Modules.Tabs import FileViewer
from queue import LifoQueue
class FileViewer:
    def __init__(self):
        self.FSModel = QFileSystemModel()
    def ChangeDirectory(self,text):
        pass



class PathEntry(QLineEdit):
    def __init__(self,currentTab:FileViewer,):
        super().__init__(parent=None)
        self.CT = currentTab

        self.listQueue = LifoQueue(100)

        self.editingFinished.connect(lambda:self.UpdateTab(self.text()))

    def UpdateTab(self,text:str):
        text = os.path.normpath(text)
        while text and not os.path.exists(text):
            text = os.path.dirname(text)

        self.setText(text)
        self.listQueue.put(text)
        self.CT.ChangeDirectory(text)

