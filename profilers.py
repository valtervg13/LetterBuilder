# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 17:19:11 2022

@author: valter.gonzaga
"""
import tkinter as tk
from tkinter import ttk

import os
import util
from cfg import format_data_path,import_data_path
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
        

format_profiler = profiler(path=format_data_path)
import_profiler = profiler(path=import_data_path)
print(import_profiler)
"""
===============================================================================
JANELAS DE PERFIS   
===============================================================================
"""
class profile_save_wd(tk.Toplevel):
    def __init__(self,
                 profiler_obj:profiler,
                 data_dict,
                 title = 'Perfis',
                 size = '650x120',
                 enable_add = False,
                 master = None):
        super().__init__(master = master)
        self.title(title)
        
        self.profiler_obj = profiler_obj
        
        from single_entry import single_entry
        size_x,size_y = map(int,size.split('x'))
        
        x_screen = master.winfo_screenwidth()/2
        y_screen = master.winfo_screenheight()/2
        x_widget,y_widget = map(int,size.split('x'))
        
        x = int(x_screen-x_widget/2)
        y = int(y_screen-y_widget/2)
        
        self.geometry(f'{size}+{x}+{y}')
        self.resizable(False,False)
        self.focus_set()
        master.attributes('-disabled', True)
        self.protocol("WM_DELETE_WINDOW", self.close)
        
        root_frame = ttk.Frame(self)
        root_frame.grid(row=0,column=0,sticky='nsew')
        
        root_canvas = tk.Canvas(root_frame)
        root_canvas.grid(row=0,column=0,sticky='nsw')
        
        item_frame = ttk.Frame(root_frame)
        
        root_canvas.create_window(0,0,window=item_frame,anchor='nw')
        
        self.rowconfigure([0],weight=1)
        self.columnconfigure([0],weight=1)
        
        self.data_dict=data_dict
        self.profiles = self.profiler_obj.profile_dict
        self.profile_names = list(self.profiles.keys())
        self.dir_path = profiler_obj.path
        
        self.popup_out = ''
        
        def update_profiles(self):
            self.profiler_obj.__init__(path=self.dir_path)
            self.profiles = self.profiler_obj.profile_dict
            self.profile_names = list(self.profiles.keys())

        def overwrite(self,
                      profile_name,
                      profiler_obj=self.profiler_obj
                      ):
            
            profiler_obj.saveAs(data_dict, profile_name, profile_name)
            
            update_profiles(self)
            
            master.show_window(profile_save_wd,
                               profiler_obj=self.profiler_obj,
                               data_dict=self.data_dict,
                               title=title,
                               size=size)
            
            
            self.update()
            self.close()
        
        def saveAs(self,
                   popup_output,
                   popup_window,
                   profile_name,
                   profile_dict,
                   profiler_obj=self.profiler_obj,
                   **kwargs
                   ):
            

            
            self.profiler_obj.saveAs(data_dict,
                                profile_name,
                                popup_output)

            update_profiles(self)
                        
            master.show_window(profile_save_wd,
                               profiler_obj=self.profiler_obj,
                               data_dict=self.data_dict,
                               title=title,
                               size=size)
            

            popup_window.destroy()
            
            self.update()
            self.close()
            
        def Add(self,
                popup_output,
                popup_window,
                profile_dict,
                profiler_obj=self.profiler_obj,
                i=0,
                j=0,
                **kwargs
                   ):
            

            self.profiler_obj.Add(data_dict,
                             popup_output)
            
            update_profiles(self)
            
            master.show_window(profile_save_wd,
                               profiler_obj=self.profiler_obj,
                               data_dict=self.data_dict,
                               title=title,
                               size=size)
            
            add_label = ttk.LabelFrame(item_frame,
                                       text='Novo Perfil'
                                       )

            
            if j == 4:
                j = -1
                i += 1
            
            j += 1
            
            add_label.grid(row=i,column=j,padx=10,pady=10,sticky='nsew')
            
            button_save = ttk.Button(add_label,
                                     text='Adicionar',
                                     command=lambda: name_popup(self,
                                                                parent_func=Add
                                                                )
                                     )
            button_save.grid(row=0,column=0,sticky='nsew')
            
            popup_window.destroy()
            self.update()
            self.close()
            
        def name_popup(self,
                       profile_name='',
                       parent_func=saveAs,
                       button_text='Salvar'):
            
            label_text = 'Nome do perfil:'
            default_var = profile_name
            
            master.show_window(single_entry,
                               parent=self,
                               parent_func=parent_func,
                               label_text=label_text,
                               default_var=default_var,
                               button_text=button_text,
                               f_kwargs={'profile_name': profile_name,
                                         'profile_dict': data_dict
                                         }
                               )
            
        
        update_profiles(self)
        
        i = 0
        j = 0
        n = 0
        for profile_name in self.profile_names:
            
            label = ttk.LabelFrame(item_frame,
                                   text=profile_name,
                                   height=size_y-20,
                                   width=size_x/5-25
                                   )
            
            label.grid_propagate(0)
            
            
            button_overwrite = ttk.Button(label,
                                          text='Salvar',
                                          command=lambda profile_instance = self.profile_names[n]: overwrite(self,
                                                                                                             profile_name=profile_instance
                                                                                                             )
                                          )
            
            button_save = ttk.Button(label,
                                     text='Salvar Como',
                                     command=lambda profile_instance = self.profile_names[n]: name_popup(self,
                                                                                                         profile_name=profile_instance
                                                                                                         )
                                     )
                

            label.grid(row=i,column=j,padx=10,pady=10,sticky='nsew')
            button_overwrite.grid(row=0,column=0,padx=5,pady=5,sticky='nsew')
            button_save.grid(row=1,column=0,padx=5,pady=5,sticky='nsew')      
        
            if j >= 4:
                j = 0
                i += 1
            
            else:
                j += 1
                
            n+=1
                
        
        if enable_add == True:
            
            add_label = ttk.LabelFrame(item_frame,
                                       text='Novo Perfil'
                                       )
            
            if j == 4:
                j = -1
                i += 1
            
            j += 1
            
            add_label.grid(row=i,column=j,padx=10,pady=10,sticky='nsew')
            
            button_save = ttk.Button(add_label,
                                     text='Adicionar',
                                     command=lambda: name_popup(self,
                                                                parent_func=Add
                                                                )
                                     )
            button_save.grid(row=0,column=0,sticky='nsew')
        
        if i!=0:
            self.scroll = ttk.Scrollbar(self,orient=tk.VERTICAL)
            self.scroll.grid(row=0,column=1,sticky='nse')
            
            root_frame.update()
            
            root_canvas.configure(scrollregion=[0,0,size_x,size_y*(i+1)+20],
                                  yscrollcommand=self.scroll.set
                                  )
            self.scroll.configure(command=root_canvas.yview)
        
        self_col,self_row=item_frame.size()

        item_frame.rowconfigure([i for i in range(self_row)], weight=1) #Faz com que a fileria de root expanda até a borda 
        item_frame.columnconfigure([i for i in range(self_col)], weight=1) #Faz com que a coluna de root expanda até a borda
        

    def close(self, event=None):
        #re-enable the main window
        self.master.attributes('-disabled', False)
        #destroy this window
        self.destroy()
            
class profile_load_wd(tk.Toplevel):
    def __init__(self,
                 parent,
                 parent_class,
                 profiler_obj:profiler,
                 data_dict,
                 title = 'Perfis',
                 size = '600x120',
                 master = None):
        
        self.profiler_obj = profiler_obj
        
        super().__init__(master = master)
        self.title(title)
        size_x,size_y = map(int,size.split('x'))
        
        x_screen = master.winfo_screenwidth()/2
        y_screen = master.winfo_screenheight()/2
        x_widget,y_widget = map(int,size.split('x'))
        
        x = int(x_screen-x_widget/2)
        y = int(y_screen-y_widget/2)
        
        self.geometry(f'{size}+{x}+{y}')
        self.resizable(False,False)
        self.focus_set()
        master.attributes('-disabled', True)
        self.protocol("WM_DELETE_WINDOW", self.close)
        
        root_frame = ttk.Frame(self)
        root_frame.grid(row=0,column=0,sticky='nsew')
        
        root_canvas = tk.Canvas(root_frame)
        root_canvas.grid(row=0,column=0,sticky='nsw')
        
        item_frame = ttk.Frame(root_frame)
        
        root_canvas.create_window(0,0,window=item_frame,anchor='nw')
        
        self.rowconfigure([0],weight=1)
        self.columnconfigure([0],weight=1)
        
        self.data_dict=data_dict
        self.profiles = self.profiler_obj.profile_dict
        self.profile_names = list(self.profiles.keys())
        self.dir_path = profiler_obj.path
        
        self.popup_out = ''
        
        def update_profiles(self):
            self.profiler_obj.__init__(path=self.dir_path)
            self.profiles = self.profiler_obj.profile_dict
            self.profile_names = list(self.profiles.keys())

        def load(self,
                 profile_name,
                 ):
            
            update_profiles(self)
            
            self.profiler_obj.load(data_dict,profile_name)
            
            if parent_class[0] =='window':
                parent.destroy()
                master.show_window(parent_class[1])
                
            else:
                parent.destroy()
                master.show_frame(parent,parent_class[1])

            
            
            self.close()

            
        update_profiles(self)
        
        i = 0
        j = 0
        for profile_name in self.profile_names:
            
            label = ttk.LabelFrame(item_frame,
                                   text=profile_name,
                                   height=size_y-20,
                                   width=(size_x/5)-25)
            
            label.grid_propagate(0)
            
            
            button_load = ttk.Button(label,
                                     text='Carregar',
                                     command=lambda profile_instance = self.profile_names[j]: load(self,
                                                                                                   profile_name=profile_instance
                                                                                                   )
                                    )
                

            label.grid(row=i,column=j,padx=10,pady=10)
            button_load.grid(row=0,column=0,padx=5,pady=5,sticky='nsew')     
            
            if j >= 4:
                j = 0
                i += 1
            
            else:
                j += 1
            
        
        if i!=0:
            self.scroll = ttk.Scrollbar(self,orient=tk.VERTICAL)
            self.scroll.grid(row=0,column=1,sticky='nse')
            
            
            root_canvas.configure(scrollregion=[0,0,size_x,size_y*(i+1)+20],
                                  yscrollcommand=self.scroll.set
                                  )
            self.scroll.configure(command=root_canvas.yview)
        
        self_col,self_row=item_frame.size()

        item_frame.rowconfigure([i for i in range(self_row)], weight=1) #Faz com que a fileria de root expanda até a borda 
        item_frame.columnconfigure([i for i in range(self_col)], weight=1) #Faz com que a coluna de root expanda até a borda
        
    def close(self, event=None):
        #re-enable the main window
        self.master.attributes('-disabled', False)
        #destroy this window
        self.destroy()