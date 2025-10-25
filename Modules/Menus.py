# Copyright (C) 2024-2025 Niritech Labs
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
import sys,os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PySide6.QtWidgets import QMenu,QWidget
from Utils.NLUtils import NLTranslator

class ActionMenu(QMenu):
    def __init__(self,parent:QWidget,translator:NLTranslator):
        super().__init__(parent=parent)
        self.TR = translator
        #self.TR.writemode = True
        self.addAction(self.TR.Translate('ActionMenu_OpenWith'))
        self.addSeparator()
        self.addAction(self.TR.Translate('ActionMenu_Cut'))
        self.addAction(self.TR.Translate('ActionMenu_Copy'))
        self.addAction(self.TR.Translate('ActionMenu_Paste'))
        self.addAction(self.TR.Translate('ActionMenu_CopyTo'))
        self.addAction(self.TR.Translate('ActionMenu_MoveTo'))
        self.addSeparator()
        self.addAction(self.TR.Translate('ActionMenu_Rename'))
        self.addAction(self.TR.Translate('ActionMenu_MoveToTrash'))
        self.addAction(self.TR.Translate('ActionMenu_RemovePermamently'))
        self.addSeparator()
        self.addAction(self.TR.Translate('ActionMenu_OpenWithTerminal'))
        self.addAction(self.TR.Translate('ActionMenu_Pack'))
        self.addSeparator()
        self.addAction(self.TR.Translate('ActionMenu_Params'))
        #self.TR.CM.SaveRestricted(self.TR.rootpath+'/Translations/'+self.TR.language+'.ntrl',self.TR.Translation)