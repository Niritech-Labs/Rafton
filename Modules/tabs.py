# Copyright (C) 2024-2025 Niritech Labs
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
import sys,os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PySide6.QtWidgets import QMainWindow, QWidget,QSizePolicy,QHBoxLayout,QFileSystemModel,QListView,QVBoxLayout
from PySide6.QtCore import QDir

class FileViewer(QWidget):
    def __init__(self):
        super().__init__(parent=None)
        self.mainLayout = QVBoxLayout(self)
        self.TabSetup()

    def TabSetup(self):
        self.FSModel = QFileSystemModel()
        self.FSModel.setRootPath(QDir.homePath())
        self.FSModel.setFilter(QDir.AllDirs | QDir.Files)

        self.listView = QListView()
        self.listView.setModel(self.FSModel)
        self.listView.setRootIndex(self.FSModel.index(QDir.homePath()))
        
        self.mainLayout.addWidget(self.listView)