# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 14:39:29 2022

@author: valter.gonzaga
"""
import tkinter as tk
from tkinter import ttk
from SUPPORT_PAGES.Preview_Window import pvWidget

import Utilities.util as util


class adding_page(ttk.Frame):
    def __init__(self, parent, controller):
        
        from HOME_PAGES.home_page import home_page
        from BUILDING_PAGES.sheet_import_builder import card_builder
        from BUILDING_PAGES.card_importer import card_importer
        from BUILDING_PAGES.web_scrapper_builder import web_scrapper_page
        from SUPPORT_PAGES.html_viewport import HTML_viewport
        
        ttk.Frame.__init__(self, parent,
                          height=parent.winfo_height(),
                          width=parent.winfo_width())
        self.controller = controller
        
                
        #---------------------------------------------------------------
        #JANELA DE VIZUALISAÇÃO
        #---------------------------------------------------------------
        
        #Frame da Janela de Visualização
        pv_widget = pvWidget(window_obj=self, 
                             parent=parent, 
                             controller=self.controller)
        
        pv_frame = pv_widget.pv_frame

        #---------------------------------------------------------------
        #FRAME DO BOTÕES
        #---------------------------------------------------------------
        
        bt_frame = ttk.Frame(self,height=0.5*parent.winfo_height(),width=0.33*parent.winfo_width())
        bt_frame.grid(row=2,column=2,sticky='nsew')
        bt_frame.grid_propagate(0)
        bt_frame.update()
        
        #BOTÃO DE ADCIONAR CARDS MANUALMENTE
        bt_addcards = ttk.Button(bt_frame,text='Adicionar Manualmente',width=25,command=lambda: controller.show_frame(self,card_builder))
        bt_addcards.grid(row=0,column=0,padx=10,pady=(100,10))
        
        #BOTÃO DE IMPORTAR DADOS
        bt_import = ttk.Button(bt_frame,text='Importar de Planilha',width=25,command=lambda: controller.show_frame(self,card_importer))
        bt_import.grid(row=1 ,column=0,padx=10,pady=(100,10))

        #BOTÃO DE WEB SCRAPPER
        bt_web = ttk.Button(bt_frame,text='Importar da Internet',width=25,command=lambda: controller.show_frame(self,web_scrapper_page))
        bt_web.grid(row=2 ,column=0,padx=10,pady=(100,10))
        
        
        #BOTÃO DE VOLTAR      
        bt_back = ttk.Button(self,
                             text='Voltar',
                             width=15,
                             command=lambda: controller.show_frame(self,home_page)
                             )
        
        bt_back.grid(row=3,column=2,padx=10,pady=(100,10))
        
        #---------------------------------------------------------------
        #SEPARADORES
        #---------------------------------------------------------------
        
        pv_separtor=ttk.Separator(self,orient=tk.VERTICAL)
        pv_separtor.grid(row=0,column=1,rowspan=4,sticky='nsew')
        
        #---------------------------------------------------------------
        #REDIMENSIONAMENTO DINAMICO
        #---------------------------------------------------------------
        self_col,self_row=self.size()

        self.rowconfigure([i for i in range(self_row)], weight=1) #Faz com que a fileria de root expanda até a borda 
        self.columnconfigure([i for i in range(self_col)], weight=1) #Faz com que a coluna de root expanda até a borda
        
        bt_frame_col,bt_frame_row=bt_frame.size()
        bt_frame.rowconfigure([i for i in range(bt_frame_row)],weight=1)  
        bt_frame.columnconfigure([i for i in range(bt_frame_col)],weight=1)
        
        pv_frame_col,pv_frame_row=pv_frame.size()
        pv_frame.rowconfigure([i for i in range(pv_frame_row)],weight=1)
        pv_frame.columnconfigure([i for i in range(pv_frame_col)],weight=1)