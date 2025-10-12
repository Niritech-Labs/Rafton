# Copyright (C) 2024-2025 Niritech Labs
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
import sys
from PySide6.QtWidgets import QMainWindow, QWidget,QSizePolicy,QHBoxLayout,QFileSystemModel,QTreeView,QApplication,QVBoxLayout,QTabWidget,QLabel
from PySide6.QtCore import QDir
from Utils.NLUtils import ConColors,ConfigManager,NLLogger
from Modules.tabs import FileViewer



class Rafton(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rafton")
        self.resize(1000, 1000)

        self._root = QWidget()
        self.setCentralWidget(self._root)
        self.rootLayout = QHBoxLayout(self._root)

        self._root.setSizePolicy(
            QSizePolicy.Policy.Expanding, 
            QSizePolicy.Policy.Expanding
        )
        self.SetupGUI()

    def SetupGUI(self):
        self.InitModules()
        self.InitLeftPanel()


        self.tabLayout = QVBoxLayout()
        self.rootLayout.addLayout(self.tabLayout)

        self.pathEntry = QLabel(str(QDir.homePath()))
        self.tabLayout.addWidget(self.pathEntry)

        self.QTabManager = QTabWidget()
        self.tabLayout.addWidget(self.QTabManager)

        self.QTabManager.addTab(self.fileview,'Filewiew')

    def InitLeftPanel(self):
        self.LeftIerarchPanel = QWidget() 
        self.LeftIerarchPanel.setObjectName('IerarchBackground')
        self.LeftIerarchPanel.setFixedWidth(300)
        self.rootLayout.addWidget(self.LeftIerarchPanel)

        self.LeftIerarchPanelLayout = QVBoxLayout(self.LeftIerarchPanel)

        self.FSModel = QFileSystemModel()
        self.FSModel.setRootPath(QDir.rootPath())
        self.FSModel.setFilter(QDir.AllDirs | QDir.Files)

        self.treeView = QTreeView()
        self.treeView.setModel(self.FSModel)
        self.treeView.setSortingEnabled(True)

        self.treeView.hideColumn(1)
        self.treeView.hideColumn(2)
        self.treeView.hideColumn(3)
        self.treeView.setRootIndex(self.FSModel.index(QDir.homePath()))
        self.LeftIerarchPanelLayout.addWidget(self.treeView)



    def InitModules(self):
        self.fileview = FileViewer()

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Rafton()
    window.show()
    sys.exit(app.exec())