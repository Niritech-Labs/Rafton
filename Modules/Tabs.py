# Copyright (C) 2024-2025 Niritech Labs
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
import sys,os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PySide6.QtWidgets import QMainWindow, QWidget,QSizePolicy,QHBoxLayout,QFileSystemModel,QListView,QVBoxLayout,QTableView,QLineEdit
from PySide6.QtCore import QDir, Qt
from Utils.NLUtils import ConColors,NLLogger,NLTranslator
from Modules.PathEntry import PathEntry
from Modules.Menus import ActionMenu
from Modules.Views import ListView

class FileViewer(QWidget):
    def __init__(self,production,name:str,FSM:QFileSystemModel,PathEntry:PathEntry,translator:NLTranslator):
        super().__init__(parent=None)
        self.Logger = NLLogger(production,'FileTab'+name)
        self.Logger.Info('Started',ConColors.G,False)

        self.AM = ActionMenu(self,translator)

        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.setSpacing(0)
        self.PE = PathEntry
        self.FSModel = FSM
        self.TabSetup()

    def ExecMenu(self,pos):
        self.AM.exec_(self.mapToGlobal(pos))

    def TabSetup(self):
        self.listView = ListView(self.FSModel)
        self.mainLayout.addWidget(self.listView)
        self.listView.doubleClicked.connect(self.Update)
        self.listView.customContextMenuRequested.connect(self.ExecMenu)
        
        

    def Update(self, index):
        path = self.FSModel.filePath(index)
        self.PE.UpdateTab(path)
        print(path)

    def ChangeDirectory(self,path):
        self._changeDirectory(self.FSModel.index(path))

    def _changeDirectory(self,index):
        if self.FSModel.isDir(index):
            self.listView.setRootIndex(index)
        
