# Copyright (C) 2024-2025 Niritech Labs
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
import sys,os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PySide6.QtWidgets import QFileSystemModel,QMessageBox
from PySide6.QtCore import QModelIndex,Qt,QDir
from Modules.ProcessDaemon import ProcessDaemon
from Utils.NLUtils import NLLogger,ConColors
class NL_RFileSystemModel(QFileSystemModel):
    def __init__(self,processDaemon:ProcessDaemon,production:bool):
        super().__init__()
        self.Logger = NLLogger(False,"FSModel")
        self.Logger.Info('Started',ConColors.G,production)
        self.PD = processDaemon
        self.setFilter(QDir.Filter.AllEntries | QDir.Filter.Files | QDir.Filter.Hidden | QDir.Filter.NoDotAndDotDot)
    
    def flags(self, index):
        default_flags = super().flags(index)
        if index.isValid():
            return default_flags | Qt.ItemIsDragEnabled
        else:
            return default_flags | Qt.ItemIsDropEnabled
    
    def mimeTypes(self):
        return ['text/uri-list', 'application/x-qabstractitemmodeldatalist']
    
    def mimeData(self, indexes):
        mimeData = super().mimeData(indexes)
        
        # Добавляем пути файлов в MIME данные
        urls = []
        for index in indexes:
            if index.column() == 0:  # Только первый столбец
                file_path = self.filePath(index)
                urls.append(file_path)
        
        # Сохраняем пути как текст
        mimeData.setText('\n'.join(urls))
        return mimeData
    
    def canDropMimeData(self, data, action, row, column, parent):
        if not parent.isValid():
            return False
        return data.hasText() or data.hasUrls()
    
    def dropMimeData(self, data, action, row, column, parent):
        if not parent.isValid():
            return False
        
        targetPath = self.filePath(parent)
        if not os.path.isdir(targetPath):
            return False
        
        # Получаем список исходных файлов
        srcPaths = []
        if data.hasText():
            srcPaths = data.text().split('\n')
        elif data.hasUrls():
            srcPaths = [url.toLocalFile() for url in data.urls()]
        
        srcPaths = [path for path in srcPaths if path.strip()]
        return self.FileOperationManager(srcPaths, targetPath, action)
    
    def FileOperationManager(self, srcPaths, targetPath, action):
        try:
            for srcPath in srcPaths:
                if not os.path.exists(srcPath):
                    continue
                
                target_file_path = os.path.join(targetPath, os.path.basename(srcPath))
                
                if action == Qt.MoveAction:
                    self.MoveFile(srcPath, target_file_path)
                elif action == Qt.CopyAction:
                    self.CopyFile(srcPath, target_file_path)
                elif action == Qt.LinkAction:
                    self.CreateLink(srcPath, target_file_path)
            
            # Обновляем модель
            self.layoutChanged.emit()
            return True
            
        except Exception as e:
            print(f"Error during file operation: {e}")
            return False
    
    def MoveFile(self, source, target):
        
        if os.path.exists(target):
            # Здесь можно добавить диалог подтверждения перезаписи
            response = QMessageBox.question(
                None,
                "Confirm Overwrite",
                f"File {os.path.basename(target)} already exists. Overwrite?",
                QMessageBox.Yes | QMessageBox.No
            )
            if response == QMessageBox.No:
                return
        
        self.PD.AddInQueue(action=Qt.MoveAction,src=source,target=target)
    
    def CopyFile(self, source, target):
        if os.path.exists(target):
            response = QMessageBox.question(
                None,
                "Confirm Overwrite",
                f"File {os.path.basename(target)} already exists. Overwrite?",
                QMessageBox.Yes | QMessageBox.No
            )
            if response == QMessageBox.No:
                return
        
        self.PD.AddInQueue(action=Qt.LinkAction,src=source,target=target)
        
    
    def CreateLink(self, source, target):    
        if os.path.exists(target):
            os.remove(target)
        
        self.PD.AddInQueue(action=Qt.CopyAction,src=source,target=target)
            #os.symlink(source, target)