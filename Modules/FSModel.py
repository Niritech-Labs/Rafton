# Copyright (C) 2024-2025 Niritech Labs
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
import sys,os
sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PySide6.QtWidgets import QFileSystemModel,QMessageBox
from PySide6.QtCore import QModelIndex,Qt,QDir,QUrl
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
        if not index.isValid():
            return default_flags | Qt.ItemFlag.ItemIsDropEnabled
    
        if self.isDir(index):
            return default_flags | Qt.ItemFlag.ItemIsDragEnabled | Qt.ItemFlag.ItemIsDropEnabled
        else:
            return default_flags | Qt.ItemFlag.ItemIsDragEnabled
    
    def mimeTypes(self):
        return ['text/uri-list', 'text/plain', 'application/x-qabstractitemmodeldatalist']

    def mimeData(self, indexes):
        mime_data = super().mimeData(indexes)
        urls = []
        file_paths = []
    
        for index in indexes:
            if index.column() == 0:  
                file_path = self.filePath(index)
                if file_path:
                    file_paths.append(file_path)
                    urls.append(QUrl.fromLocalFile(file_path))

        mime_data.setUrls(urls)
        mime_data.setText('\n'.join(file_paths))
    
        return mime_data

    def canDropMimeData(self, data, action, row, column, parent):
        if data.hasUrls() or data.hasText():
            if parent.isValid() and self.isDir(parent):
                return True
        return False

    def dropMimeData(self, data, action, row, column, parent):
        if not parent.isValid():
            return False
    
        target_path = self.filePath(parent)
        if not self.isDir(parent):
            return False

        src_paths = []

        if data.hasUrls():
            for url in data.urls():
                if url.isLocalFile():
                    src_paths.append(url.toLocalFile())
    
        elif data.hasText():
            paths = data.text().split('\n')
            for path in paths:
                path = path.strip()
                if path and (path.startswith('/') or ':' in path): 
                    src_paths.append(path)
    
        if not src_paths:
            return False
    
        return self.FileOperationManager(src_paths, target_path, action)
    
    def FileOperationManager(self, srcPaths, targetPath, action):
        try:
            for srcPath in srcPaths:
                if not os.path.exists(srcPath):
                    continue
                
                target_file_path = os.path.join(targetPath, os.path.basename(srcPath))
                
                if action == Qt.DropAction.MoveAction:
                    self.MoveFile(srcPath, target_file_path)
                elif action == Qt.DropAction.CopyAction:
                    self.CopyFile(srcPath, target_file_path)
                elif action == Qt.DropAction.LinkAction:
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
        
        self.PD.AddInQueue(action=Qt.DropAction.MoveAction,src=source,target=target)
    
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
        
        self.PD.AddInQueue(action=Qt.DropAction.CopyAction,src=source,target=target)
        
    
    def CreateLink(self, source, target):    
        if os.path.exists(target):
            os.remove(target)
        
        self.PD.AddInQueue(action=Qt.DropAction.LinkAction,src=source,target=target)
            #os.symlink(source, target)
