import os
from queue import Queue

class FolderHierarchy:
    def __init__(self, workspace):
        self.workspace = workspace
        self.data = {}
        def dfs(data, path):
            for item in os.scandir(path):
                if item.is_dir():
                    data[item.name] = {}
                    dfs(data[item.name], item.path)
                else:
                    data[item.name] = None
        dfs(self.data, workspace)
