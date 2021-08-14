#!/usr/bin/python3

class HexGrid:
    def __init__(self):
        self.__grid = {}
        
    def set_data(self, data, key):
        self.__grid[key] = data
        
    def get_data(self, key):
        if key in self.__grid:
            return self.__grid[key]
        else:
            return None