# Copyright (C) 2024-2025 Niritech Labs
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
import sys,os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PySide6.QtWidgets import QMainWindow,QTableView,QTreeView,QSizePolicy,QTableView,QStyle
from PySide6.QtGui import QDrag, QPixmap, QPainter, QFont, QColor
from PySide6.QtCore import QPoint, Qt, QSize
from Modules.FSModel import NL_RFileSystemModel
from PySide6.QtCore import QDir, Qt

class ListView(QTableView):
    def __init__(self,model:NL_RFileSystemModel):
        super().__init__(parent=None)
        self.FSM = model

        self.setModel(self.FSM)
        self.setShowGrid(False)
        self.verticalHeader().setVisible(False)
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding, 
            QSizePolicy.Policy.Expanding
        )
        self.setRootIndex(self.FSM.index(QDir.homePath()))
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDragDropOverwriteMode(False)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setDragDropMode(QTableView.DragDrop)
        self.Setup()
    
    def Setup(self):
        pass

    def startDrag(self, supportedActions):
        indexes = self.selectionModel().selectedIndexes()
        if not indexes:
            return
        
        first_column_indexes = []
        rows = set()
        for index in indexes:
            if index.column() == 0 and index.row() not in rows:
                first_column_indexes.append(index)
                rows.add(index.row())
        
        mime_data = self.model().mimeData(first_column_indexes)
        if not mime_data:
            return
        
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        

        pixmap = self.setupDragPixmap(first_column_indexes)
        drag.setPixmap(pixmap)
        drag.setHotSpot(QPoint(pixmap.width() // 2, pixmap.height() // 2))
        
        drag.exec_(supportedActions, Qt.DropAction.MoveAction)

    def _resizeIcon(self,icon,size):
        iconPixmapRaw = icon.pixmap(size * 2)
        return iconPixmapRaw.scaled(size,Qt.AspectRatioMode.KeepAspectRatio,Qt.SmoothTransformation)
    
    
    def setupDragPixmap(self, indexes):
    
        count = len(indexes)
        if count == 0:
            return QPixmap()
    
        model = self.model()
        index = indexes[0]

        iconSize = QSize(32, 32)
        if count == 1:
            width = iconSize.width() + 40
            height = iconSize.height() + 20
        else:
            width = iconSize.width() + 80
            height = iconSize.height() + 20


        iconPixmap = self._resizeIcon(model.data(index, Qt.ItemDataRole.DecorationRole),iconSize)
        if count > 1:
            iconPixmapTwo = self._resizeIcon(model.data(indexes[1], Qt.ItemDataRole.DecorationRole),iconSize)
        if count > 2:
            iconPixmapThree = self._resizeIcon(model.data(indexes[2], Qt.ItemDataRole.DecorationRole),iconSize)
    

        pixmap = QPixmap(width, height)
        pixmap.fill(Qt.GlobalColor.transparent)
    
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
        if count > 2:
            painter.drawPixmap(10, 10, iconPixmapThree)
        if count > 1:
            painter.drawPixmap(5, 10, iconPixmapTwo)
        painter.drawPixmap(0, 0, iconPixmap)
    
        painter.end()
        return pixmap


