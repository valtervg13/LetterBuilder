# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 17:29:42 2022

@author: valter.gonzaga
"""
import tkinter as tk
from tkinter import ttk


import cfg
import util

from Preview_Window import pvWidget

#==============================================================================
#VARIÁVEIS GLOBAIS
#==============================================================================

info_dict_list = cfg.info_dict_list
format_dict = cfg.format_dict
import_dict = cfg.import_dict
monthdays = cfg.monthdays
monthdays_dict = cfg.months_dict

format_data_path = cfg.format_data_path
import_data_path = cfg.import_data_path


html_errmessages = cfg.html_errmessages
news = cfg.news

#==============================================================================
# PÁGINA INICIAL
#==============================================================================

class home_page(ttk.Frame):
    def __init__(self, parent, controller):
        
        from adding_page import adding_page
        from html_viewport import HTML_viewport
        from edit_page import edit_page


        ttk.Frame.__init__(self, parent,
                          height=parent.winfo_height(),
                          width=parent.winfo_width())
        self.controller = controller

        #JANELA PRINCIPAL
        #JANELA DE VIZUALISAÇÃO
        #Frame da Janela de Visualização
        pv_widget = pvWidget(window_obj=self, 
                            parent=parent, 
                            controller=self.controller,
                            width = 0.75)
        pv_frame = pv_widget.pv_frame
        
        #FRAME DO BOTÕES
        bt_frame = ttk.Frame(self,height=0.5*parent.winfo_height(),width=0.25*parent.winfo_width())
        bt_frame.grid(row=2,column=2,sticky='nsew')
        bt_frame.grid_propagate(0)
        bt_frame.update()
        

        #BOTÃO DE ADCIONAR CARDS
        bt_addcards = ttk.Button(bt_frame,
                                 text='Adicionar Cards',
                                 width=15,
                                 command=lambda: controller.show_frame(current_self=self,
                                                                       page_class=adding_page
                                                                       )
                                 )
        bt_addcards.grid(row=0,column=0,padx=10,pady=(100,10))
        
        #BOTÃO DE EDITAR CARDS
        bt_editcards = ttk.Button(bt_frame,text='Editar Cards',
                                  width=15,
                                  command=lambda: controller.show_frame(current_self=self,
                                                                        page_class=edit_page
                                                                        )
                                  )
        
        bt_editcards.grid(row=1,column=0,padx=10,pady=10)
        

        #SEPARADORES
        
        pv_separtor=ttk.Separator(self,orient=tk.VERTICAL)
        pv_separtor.grid(row=0,column=1,rowspan=4,sticky='nsew')
        
        #REDIMENSIONAMENTO DINAMICO
        self_col,self_row=self.size()

        self.rowconfigure([i for i in range(self_row)], weight=1) #Faz com que a fileria de root expanda até a borda 
        self.columnconfigure([i for i in range(self_col)], weight=1) #Faz com que a coluna de root expanda até a borda
        
        bt_frame_col,bt_frame_row=bt_frame.size()
        bt_frame.rowconfigure([i for i in range(bt_frame_row)],weight=1)  
        bt_frame.columnconfigure([i for i in range(bt_frame_col)],weight=1)
        
        
        pv_frame_col,pv_frame_row = pv_frame.size()
        pv_frame.rowconfigure([i for i in range(pv_frame_row)],weight=1)
        pv_frame.columnconfigure([i for i in range(pv_frame_col)],weight=1)