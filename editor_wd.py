# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 17:15:25 2022

@author: valter.gonzaga
"""

# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 14:24:40 2022

@author: valter.gonzaga
"""
import tkinter as tk
from tkinter import ttk
from News_Builder import card,Newsletter
from format_wd import format_wd
import util

#====================
#Janela de Formatação
#====================

class editor_wd(format_wd):
    def __init__(self,
                 card_obj: card,
                 edit_pg,
                 pos: int,
                 title = 'Editar Card',
                 size = '700x350',
                 master = None
                 ):
        
        super().__init__(title = title,
                         size = size,
                         master = master)
        
        save_format = super().save_format
        
        from cfg import format_dict

        def apply():
            from edit_page import edit_page
            
            pos_idx = int(self.pos_var.get())

            save_format()
            
            news.cards.pop(pos)
            
            if pos_idx == pos-1:
                pos_idx = 'replace'
            

            self.master.createCard(newsletter=news,
                                   info=card_obj.info,
                                   format_dict=format_dict,
                                   pos=pos_idx)
            
            self.master.show_frame(self.master,edit_page)
            
            edit_pg.close()
            
            
                  
        self.title(title)
        self.geometry(f'{size}+{0}+{0}')
        self.resizable(False,False)
        
        from cfg import news

        
        self.general_frame = ttk.Frame(self.root_menus)
        self.general_frame.grid(row=0,column=0,sticky='nsew')
        self.rowconfigure([0],weight=1)
        self.columnconfigure([0],weight=1)
        
        
        self.pos_label = ttk.Label(self.general_frame,text='Posição')
        
        self.pos_var = tk.StringVar()
        self.pos_var.set(f'{pos+1}')
        self.general_frame.update()
        
        self.pos_entry = ttk.Entry(self.general_frame,
                              width=3,
                              textvariable=self.pos_var)

        
        self.pos_label.grid(row=0,column=0,padx=5,pady=3,sticky='nw')
        self.pos_entry.grid(row=0,column=1,padx=5,pady=3,sticky='ne')
        
        self.root_menus.add(self.general_frame,text='Geral')
        
        self.apply_button = ttk.Button(self.button_frame,text='Aplicar',
                                       width=25,
                                       command=lambda: apply()
                                       )
        
        self.apply_button.grid(row=2,column=0,padx=10,pady=5,sticky='ns')
        
        
        

            
