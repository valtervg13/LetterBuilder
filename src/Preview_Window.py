# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 14:30:34 2022

@author: valter.gonzaga
"""

import tkinter as tk
from tkinter import ttk
import util

class pvWidget():
    """

    Parameters
    ----------
    window_obj : tk.Frame
        Frame onde a Aba de Preqview será inserida.
    parent : tk.Widget ou tk.TK
        widget pai do frame.
    controller : tk.TK
        Widget raiz da janela.
    width : float, optional
        Percentual da largura da janela ocupado por preview. 
        The default is 0.66.
    height : TYPE, optional
        Percentual da altura da janela ocupado por preview.
        The default is 0.9.
    """
    def __init__(self, 
                 window_obj, 
                 parent, 
                 controller,
                 width = 0.66,
                 height = 0.9):

        
        from html_viewport import HTML_viewport
        
        self.window_obj = window_obj
        self.parent = parent
        self.controller = controller
        self.width = width
        self.height = height
         
        #Frame da Janela de Visualização
        self.pv_frame = ttk.Frame(self.window_obj,height=self.height*self.parent.winfo_height(),width=self.width*self.parent.winfo_width())
        self.pv_frame.grid(row=1,column=0,rowspan=3,sticky='nsew')
        self.pv_frame.grid_propagate(0)
        self.pv_frame.update()
        
        
        #Label "Preview"
        self.pv_label = ttk.Label(self.window_obj,anchor='w',text='Preview',font=('Courier New',20))
        self.pv_label.grid(row=0,column=0,padx=40,pady=10,sticky='nsew')
        
        
        #Texto da janela
        
        self.pv_text = HTML_viewport(self.pv_frame)
        
        self. pv_text.update()
        self.pv_text.grid(row=1,column=0,padx=40,pady=(5,2))
        
        
        #Frame da toolbar
        self.pv_toolbar_frame = ttk.Frame(self.pv_frame,width=self.pv_frame.winfo_width())
        self.pv_toolbar_frame.grid(row=2,column=0,padx=40,pady=(0,5),sticky='sew')
        
        #Botão de exportar
        
        self.pv_btt_export = ttk.Button(self.pv_toolbar_frame,
                                   image=self.controller.export_icon,
                                   compound=tk.LEFT,
                                   text='Exportar\nE-mail',
                                   command= lambda: util.exportEML(),
                                   )
        self.pv_btt_export.grid(row=0,column=0,sticky='w')
        
        #Botão de ajuda.
        self.pv_btt_refresh = ttk.Button(self.pv_toolbar_frame,
                                    image=controller.help_icon,
                                    compound=tk.LEFT,
                                    text='Ajuda',
                                    command=lambda: util.Helper(self.pv_text)
                                    )
        
        self.pv_btt_refresh.grid(row=0,column=1,sticky='e')
        
        #Botão de Navegador.
        self.pv_btt_refresh = ttk.Button(self.pv_toolbar_frame,
                                    image=self.controller.browser_icon,
                                    compound=tk.LEFT,
                                    text='Abrir no Navegador',
                                    command=lambda: util.DisplayBrowser()
                                    )
        
        self.pv_btt_refresh.grid(row=0,column=2,sticky='e')
        
        #Botão de refrescar visualização.
        self.pv_btt_refresh = ttk.Button(self.pv_toolbar_frame,
                                    image=self.controller.refresh_icon,
                                    compound=tk.LEFT,
                                    text='Recarregar',
                                    command=lambda: util.RefreshPv(self.pv_text)
                                    )
        
        self.pv_btt_refresh.grid(row=0,column=3,sticky='e')
        
        self.pv_toolbar_frame_col,self.pv_toolbar_frame_row=self.pv_toolbar_frame.size()
        self.pv_toolbar_frame.rowconfigure([i for i in range(self.pv_toolbar_frame_row)],weight=1)
        self.pv_toolbar_frame.columnconfigure([i for i in range(self.pv_toolbar_frame_col)],weight=1)