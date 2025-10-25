# Copyright (C) 2024-2025 Niritech Labs
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
import sys,os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PySide6.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout,QSpacerItem,QSizePolicy,QLabel
from PySide6.QtCore import Qt
from Utils.NLUtils import NLLogger,ConColors

class Notifyer(QWidget):
    def __init__(self,production:bool,):
        super().__init__(parent=None)
        self.Logger = NLLogger(production,'ProccesNotifyer')
        self.Logger.Info('Started',ConColors.G,False)
        self.setFixedHeight(40)
        self.setObjectName('NotifyerPanel')
        self.mainLayout = QHBoxLayout(self)

        self.progressWidget = OperationProgress()
        self.mainLayout.addWidget(self.progressWidget)
        spacer = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.mainLayout.addSpacerItem(spacer)
        
        self.cursorFile = QLabel('aaaaaaaaaaaaaaa')
        self.mainLayout.addWidget(self.cursorFile)
        

    def Setup(self):
        pass

class OperationProgress(QWidget):
    def __init__(self):
        super().__init__(parent=None)