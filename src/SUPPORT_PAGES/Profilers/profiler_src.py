# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 17:19:11 2022

@author: valter.gonzaga
"""
import tkinter as tk
from tkinter import ttk

import os
import Utilities.util as util

"""
===============================================================================
PROFILERS
===============================================================================
"""

class profiler():
    def __init__(self,
                 path               
                 ):
        
        file_list = os.listdir(path)
        
        profile_dict = {}
        for file_name in file_list:
                file_name,file_extension = file_name.split('.')

                profile_dict[file_name] = util.fetch_data(f'{path}/{file_name}.cfg')
        
        self.path = path
        self.file_list = file_list
        self.profile_dict = profile_dict
        
        
    def saveAs (self,data_dict,old_file,new_file):
        
        old_file_path = f'{self.path}/{old_file}.cfg'
        new_file_path = f'{self.path}/{new_file}.cfg'
        
        util.store_data(old_file_path, data_dict)
        
        if old_file != new_file:
            os.rename(old_file_path, new_file_path)
            
    def load(self,data_dict:dict,file):
        
        file_path = f'{self.path}/{file}.cfg'
        data_dict.clear()
        new_data = util.fetch_data(file_path)
        data_dict.update(new_data.items())
        
    def add(self,data_dict,name):
        file_path = f'{self.path}/{name}.cfg'
        util.store_data(file_path, data_dict)
        
        file_list = os.listdir(self.path)
        
        profile_dict = {}
        for file_name in file_list:
                file_name,file_extension = file_name.split('.')

                profile_dict[file_name] = util.fetch_data(f'{self.path}/{file_name}.cfg')
        
        self.file_list = file_list
        self.profile_dict = profile_dict
        