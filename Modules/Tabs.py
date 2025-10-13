# Copyright (C) 2024-2025 Niritech Labs
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
import sys,os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PySide6.QtWidgets import QMainWindow, QWidget,QSizePolicy,QHBoxLayout,QFileSystemModel,QListView,QVBoxLayout,QTableView,QLineEdit
from PySide6.QtCore import QDir

class FileViewer(QWidget):
    def __init__(self,FSM:QFileSystemModel,PathEntry:QLineEdit):
        super().__init__(parent=None)
        self.mainLayout = QVBoxLayout(self)
        self.mainLayout.setContentsMargins(0,0,0,0)
        self.mainLayout.setSpacing(0)
        self.PE = PathEntry
        self.FSModel = FSM
        self.TabSetup()

    def TabSetup(self):
        self.listView = QTableView()
        self.listView.setModel(self.FSModel)

        self.listView.setShowGrid(False)
        self.listView.verticalHeader().setVisible(False)

        self.listView.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.listView.setSizePolicy(
            QSizePolicy.Policy.Expanding, 
            QSizePolicy.Policy.Expanding
        )
        self.listView.setRootIndex(self.FSModel.index(QDir.homePath()))
        
        self.mainLayout.addWidget(self.listView)

        self.listView.doubleClicked.connect(self._changeDirectory)

    def Update(self):
        path = self.FSModel.filePath(self.listView.rootIndex())
        self.PE.setText(str(path))
        print(path)

    def ChangeDirectory(self,path):
        self._changeDirectory(self.FSModel.index(path))
    def _changeDirectory(self,index):
        if self.FSModel.isDir(index):
            self.listView.setRootIndex(index)
        self.Update()
        #else:
            #self.
