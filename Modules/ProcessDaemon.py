# Copyright (C) 2024-2025 Niritech Labs
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
import sys,os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PySide6.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout
from PySide6.QtCore import Qt
from Utils.NLUtils import NLLogger,ConColors
from Modules.Notifyer import Notifyer

class ProcessDaemon:
    def __init__(self,NotifyerLayout:QVBoxLayout,production:bool):
        self.Logger = NLLogger(False,"Process Daemon")
        self.Logger.Info('Started',ConColors.G,production)

        self.notifyer = Notifyer(production)

        NotifyerLayout.addWidget(self.notifyer)

    def AddInQueue(self,action:Qt.DropAction,src:str,target:str=None):
        self.Logger.Info(f'operation {str(action)}',ConColors.Y,False)
        self.notifyer.cursorFile.setText('bbbbbbbbb')

   
