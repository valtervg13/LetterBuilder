import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from cfg import format_data_path,import_data_path

from Utilities.util import fetch_data,store_data

from SUPPORT_PAGES.Profilers.profiler_src import profiler
            
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