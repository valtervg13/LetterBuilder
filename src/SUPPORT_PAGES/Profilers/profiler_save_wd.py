import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from cfg import format_data_path,import_data_path

from Utilities.util import fetch_data,store_data

from SUPPORT_PAGES.Profilers.profiler_src import profiler

class profile_save_wd(tk.Toplevel):
    """
    A class for creating a Toplevel window to save profiles.
    Takes in a profiler object, data dictionary, title, size, enable_add flag, and master window.
    Provides options to save and overwrite profiles using buttons.
    
    Parameters
    ----------
    profiler_obj : profiler
        A profiler object that contains the profiles to be saved.
    data_dict : dict
        A data dictionary to be passed to the profiler object.
    title : str, optional
        The title of the Toplevel window. Default is 'Perfis'.
    size : str, optional
        The size of the Toplevel window in the format 'widthxheight'. Default is '650x120'.
    enable_add : bool, optional
        A flag to enable adding profiles. Default is False.
    master : tk.Tk, optional
        The master window for the Toplevel window. Default is None.
    """
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
        self.data_dict = data_dict
        self.title = title
        self.size = size
        self.enable_add = enable_add
        self.master = master
        
        self.size_x,self.size_y = map(int,size.split('x'))
        
        self.x_screen = self.master.winfo_screenwidth()/2
        self.y_screen = self.master.winfo_screenheight()/2
        self.x_widget,self.y_widget = map(int,self.size.split('x'))
        
        self.x = int(self.x_screen-self.x_widget/2)
        self.y = int(self.y_screen-self.y_widget/2)
        
        self.geometry(f'{self.size}+{self.x}+{self.y}')
        self.resizable(False,False)
        self.focus_set()
        self.master.attributes('-disabled', True)
        self.protocol("WM_DELETE_WINDOW", self.close)
        
        self.root_frame = ttk.Frame(self)
        self.root_frame.grid(row=0,column=0,sticky='nsew')
        
        self.root_canvas = tk.Canvas(self.root_frame)
        self.root_canvas.grid(row=0,column=0,sticky='nsw')
        
        self.item_frame = ttk.Frame(self.root_frame)
        
        self.root_canvas.create_window(0,0,window=self.item_frame,anchor='nw')
        
        self.rowconfigure([0],weight=1)
        self.columnconfigure([0],weight=1)
        
        self.data_dict=data_dict
        self.profiles = self.profiler_obj.profile_dict
        self.profile_names = list(self.profiles.keys())
        self.dir_path = profiler_obj.path
        
        self.popup_out = ''
        
        self.update_profiles()
        
        i = 0
        j = 0
        n = 0
        for profile_name in self.profile_names:
            
            label = ttk.LabelFrame(self.item_frame,
                                   text=profile_name,
                                   height=self.size_y-20,
                                   width=self.size_x/5-25
                                   )
            
            label.grid_propagate(0)
            
            
            button_overwrite = ttk.Button(label,
                                          text='Salvar',
                                          command=lambda profile_instance = self.profile_names[n]: self.overwrite( profile_name=profile_instance)
                                          )
            
            button_save = ttk.Button(label,
                                     text='Salvar Como',
                                     command=lambda profile_instance = self.profile_names[n]: self.name_popup(profile_name=profile_instance)
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
                
        
        if self.enable_add == True:
            
            add_label = ttk.LabelFrame(self.item_frame,
                                       text='Novo Perfil'
                                       )
            
            if j == 4:
                j = -1
                i += 1
            
            j += 1
            
            add_label.grid(row=i,column=j,padx=10,pady=10,sticky='nsew')
            
            button_save = ttk.Button(add_label,
                                     text='Adicionar',
                                     command=lambda: self.name_popup(parent_func=self.Add)
                                     )
            button_save.grid(row=0,column=0,sticky='nsew')
        
        if i!=0:
            self.scroll = ttk.Scrollbar(self,orient=tk.VERTICAL)
            self.scroll.grid(row=0,column=1,sticky='nse')
            
            self.root_frame.update()
            
            self.root_canvas.configure(scrollregion=[0,0,self.size_x,self.size_y*(i+1)+20],
                                  yscrollcommand=self.scroll.set
                                  )
            self.scroll.configure(command=self.root_canvas.yview)
        
        self_col,self_row=self.item_frame.size()

        self.item_frame.rowconfigure([i for i in range(self_row)], weight=1) #Faz com que a fileria de root expanda até a borda 
        self.item_frame.columnconfigure([i for i in range(self_col)], weight=1) #Faz com que a coluna de root expanda até a borda
    
    
    def update_profiles(self):
        self.profiler_obj.__init__(path=self.dir_path)
        self.profiles = self.profiler_obj.profile_dict
        self.profile_names = list(self.profiles.keys())

    def overwrite(self,
                    profile_name,
                    profiler_obj=""
                    ):
        
        profiler_obj = self.profiler_obj if profiler_obj == "" else profiler_obj

        profiler_obj.saveAs(self.data_dict, profile_name, profile_name)
        
        self.update_profiles()
        
        self.master.show_window(profile_save_wd,
                            profiler_obj=self.profiler_obj,
                            data_dict=self.data_dict,
                            title=self.title,
                            size=self.size)
        
        
        self.update()
        self.close()
    
    def saveAs(self,
                popup_output,
                profile_name,
                profile_dict,
                profiler_obj="",
                **kwargs
                ):
        """
        Saves a profile as a new profile with a user-specified name.
        
        Parameters
        ----------
        popup_output : str
            The name specified by the user for the new profile.
        profile_name : str
            The name of the profile to be saved as a new profile.
        profile_dict : dict
            The dictionary containing all the profiles.
        profiler_obj : profiler, optional
            A profiler object that contains the profiles to be saved. If not specified, the profiler_obj attribute of the class is used.
        """

        profiler_obj = self.profiler_obj if profiler_obj == "" else profiler_obj

        self.profiler_obj.saveAs(self.data_dict,
                                profile_name,
                                popup_output)

        self.update_profiles()
                    
        self.master.show_window(profile_save_wd,
                            profiler_obj=self.profiler_obj,
                            data_dict=self.data_dict,
                            title=self.title,
                            size=self.size)
        
        self.update()
        self.close()
        
    def Add(self,
            popup_output,
            popup_window,
            profile_dict,
            profiler_obj='',
            i=0,
            j=0,
            **kwargs
                ):
        
        profiler_obj = self.profiler_obj if profiler_obj == "" else profiler_obj

        self.profiler_obj.Add(self.data_dict,
                            popup_output)
        
        self.update_profiles()
        
        self.master.show_window(profile_save_wd,
                            profiler_obj=self.profiler_obj,
                            data_dict=self.data_dict,
                            title=self.title,
                            size=self.size)
        
        add_label = ttk.LabelFrame(self.item_frame,
                                    text='Novo Perfil'
                                    )

        
        if j == 4:
            j = -1
            i += 1
        
        j += 1
        
        add_label.grid(row=i,column=j,padx=10,pady=10,sticky='nsew')
        
        button_save = ttk.Button(add_label,
                                    text='Adicionar',
                                    command=lambda: self.name_popup(parent_func=self.Add)
                                    )
        button_save.grid(row=0,column=0,sticky='nsew')
        
        popup_window.destroy()
        self.update()
        self.close()


    def name_popup(self,
                    profile_name='',
                    parent_func= "",
                    button_text='Salvar'):
            
        from SUPPORT_PAGES.single_entry import single_entry

        parent_func = self.saveAs if parent_func == "" else parent_func

        label_text = 'Nome do perfil:'
        default_var = profile_name
        
        self.master.show_window(single_entry,
                            parent=self,
                            parent_func=parent_func,
                            label_text=label_text,
                            default_var=default_var,
                            button_text=button_text,
                            f_kwargs={'profile_name': profile_name,
                                        'profile_dict': self.data_dict
                                        }
                            )
            
        
        

    def close(self, event=None):
        #re-enable the main window
        self.master.attributes('-disabled', False)
        #destroy this window
        self.destroy()