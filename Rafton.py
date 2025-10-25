# Copyright (C) 2024-2025 Niritech Labs
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
import sys,os
from PySide6.QtWidgets import QMainWindow, QWidget,QSizePolicy,QHBoxLayout,QTreeView,QApplication,QVBoxLayout,QTabWidget,QLineEdit
from PySide6.QtCore import QDir, Qt
from Utils.NLUtils import ConColors,NLTranslator,NLLogger
from Modules.Tabs import FileViewer
from Modules.PathEntry import PathEntry
from Modules.FSModel import NL_RFileSystemModel
from Modules.ProcessDaemon import ProcessDaemon
os.environ['QT_QPA_PLATFORMTHEME'] = 'gtk3'


class Rafton(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rafton")
        self.resize(1000, 1000)

        self.production = False
        self.currentTab = None

        self.Logger = NLLogger(False,"Rafton main class")
        self.Logger.Info('Started',ConColors.G,self.production)

        self._root = QWidget()

        self.setCentralWidget(self._root)
        self.rootLayout = QVBoxLayout(self._root)
        self.mainLayout = QHBoxLayout()
        self.rootLayout.setContentsMargins(0,0,0,0)
        self.rootLayout.setSpacing(0)
        self.rootLayout.addLayout(self.mainLayout)

        self.PreSetup()
        self.SetupGUI()

    def PreSetup(self):
        self.Translator = NLTranslator(self.production,'Config')

        self.ProcessDaemon = ProcessDaemon(self.rootLayout,self.production)

        self.pathEntry = PathEntry(self.currentTab)

        self.FSModel = NL_RFileSystemModel(self.ProcessDaemon,self.production)
        self.FSModel.setRootPath(QDir.rootPath())

    def SetupGUI(self):
        self._root.setSizePolicy(
            QSizePolicy.Policy.Expanding, 
            QSizePolicy.Policy.Expanding
        )

        self.InitMainPanel()
        self.InitModules()

        self.tabLayout = QVBoxLayout()
        self.mainLayout.addLayout(self.tabLayout)

        
        
        self.tabLayout.addWidget(self.pathEntry)

        self.QTabManager = QTabWidget()
        self.tabLayout.addWidget(self.QTabManager)

        self.QTabManager.addTab(self.fileview,'Filewiew')
        self.currentTab = self.fileview
        self.QTabManager.currentChanged.connect(self.TabChanged)
        self.pathEntry.CT = self.currentTab

        

    def InitMainPanel(self):
        self.LeftIerarchPanel = QWidget() 
        self.LeftIerarchPanel.setObjectName('TreeViewBackground')
        self.LeftIerarchPanel.setFixedWidth(300)
        self.mainLayout.addWidget(self.LeftIerarchPanel)

        self.LeftIerarchPanelLayout = QVBoxLayout(self.LeftIerarchPanel)

        self.treeView = QTreeView()
        self.treeView.setModel(self.FSModel)
        self.treeView.setSortingEnabled(True)

        self.treeView.hideColumn(1)
        self.treeView.hideColumn(2)
        self.treeView.hideColumn(3)
        self.treeView.setRootIndex(self.FSModel.index(QDir.rootPath()))
        self.treeView.clicked.connect(self.FolderChoosed)
        self.treeView.setDragEnabled(True)
        self.treeView.setAcceptDrops(True)
        self.treeView.setDropIndicatorShown(True)
        self.treeView.setDragDropMode(QTreeView.DragDrop)
        self.treeView.setDragDropOverwriteMode(False)
        self.treeView.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.LeftIerarchPanelLayout.addWidget(self.treeView)



    def InitModules(self):
        self.fileview = FileViewer(self.production,'main',self.FSModel,self.pathEntry,self.Translator)

    def TabChanged(self,index):
        self.currentTab = self.QTabManager.widget(index)
        self.currentTab.Update()

    def FolderChoosed(self,index):
        self.currentTab._changeDirectory(index)

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Rafton()
    window.show()
    sys.exit(app.exec())