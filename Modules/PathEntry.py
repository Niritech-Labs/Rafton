# Copyright (C) 2024-2025 Niritech Labs
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
import sys,os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PySide6.QtWidgets import QLineEdit
from Modules.Tabs import FileViewer

class PathEntry(QLineEdit):
    def __init__(self,currentTab:FileViewer):
        super.__init__()
        self.CT = currentTab

        self.textEdited.connect(self.UpdateTab)

    def UpdateTab(self,inf):
        self.CT.ChangeDirectory(self.text())

