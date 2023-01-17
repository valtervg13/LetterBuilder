# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 14:15:05 2022

@author: valter.gonzaga
"""

import tkinter as tk
from tkinter import ttk
from SUPPORT_PAGES.Preview_Window import pvWidget

import Utilities.util as util

def list_cards(newsletter,
               canvas_width,
               frame,
               editor_window,
               editor_window_call,
               self_page,
               window,
               master):
    
    from cfg import format_dict
    
    width = canvas_width
    if newsletter.cards != []:
        for i,card_obj in enumerate(newsletter.cards):
            
            
            obj_frame = tk.Frame(frame, bg='#fff',
                                 height=30,
                                 width=0.95*width)
            obj_frame.grid(row=i,column=0,padx=10,pady=1,sticky='nsew')
            obj_frame.grid_propagate(0)
            
            obj_label1 = ttk.Label(obj_frame,
                                  text=f'{i+1}.',
                                  background='#fff',
                                  width=10
                                  )
            obj_label1.grid(row=0,column=0,padx=(10,0),sticky='nsw')
            
            obj_label2 = ttk.Label(obj_frame,
                                  text=card_obj.title,
                                  background='#fff',
                                  borderwidth = 5,
                                  width=100
                                  )
            obj_label2.grid(row=0,column=1,sticky='nsw')
            
            obj_edit = ttk.Button(obj_frame,
                                  text='Editar',
                                  command=lambda card=card_obj,idx=i: editor_window_call(editor_window,
                                                                                           edit_pg=self_page,
                                                                                           card_obj=card,
                                                                                           pos=idx),
                                  width=0.1*width
                                  )
            
            obj_edit.grid(row=0,column=2,padx=5,sticky='nse')
            

            
            def delete(pos):
                newsletter.delete_card(pos=pos)
                
                master.BuildLetter(newsletter=newsletter,
                                   format_dict=format_dict)
                
                master.show_frame(master,edit_page)
            
                window.destroy()
            
            obj_delete = ttk.Button(obj_frame,
                                    text='Deletar',
                                    command=lambda idx=i: delete(pos=idx),
                                    width=0.1*width
                                    )
            
            obj_delete.grid(row=0,column=3,padx=5,sticky='nse')
            
            obj_frame_col,obj_frame_row=obj_frame.size()
            obj_frame.rowconfigure([0,1,2,3],weight=1)
            obj_frame.columnconfigure([0],weight=1)
        
    else:
            obj_frame = ttk.Frame(frame,borderwidth=10,width=width,height=600)
            obj_frame.grid(row=0,column=0,padx=1,pady=1,sticky='nsew')
            obj_frame.grid_propagate(0)
            
            obj_label = ttk.Label(obj_frame, text='Nenhum Card Encontrado')
            obj_label.grid(row=0,column=0,sticky='nsew')
            
            obj_frame_col,obj_frame_row=obj_frame.size()
            obj_frame.rowconfigure([i for i in range(obj_frame_row)],weight=1)
            obj_frame.columnconfigure([i for i in range(obj_frame_col)],weight=1)


class edit_page(ttk.Frame):
    def __init__(self, parent, controller):
        
        from HOME_PAGES.home_page import home_page
        from SUPPORT_PAGES.html_viewport import HTML_viewport
        from SUPPORT_PAGES.editor_wd import editor_wd
        from cfg import news
        
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
                             controller=self.controller,
                             width=0.4,
                             height=0.9)
        
        pv_frame = pv_widget.pv_frame
        #---------------------------------------------------------------
        #FRAME DO BOTÕES
        #---------------------------------------------------------------
        
        bt_frame = ttk.Frame(self,height=0.8*parent.winfo_height(),width=0.6*parent.winfo_width())
        bt_frame.grid(row=2,column=2,sticky='nsew')
        bt_frame.grid_propagate(0)
        bt_frame.update()
        
        #CANVAS DA LISTA DE CARDS

        list_frame = ttk.Frame(bt_frame)
        list_frame.grid(row=0,column=0,sticky='nsew')
        
        card_canvas = tk.Canvas(list_frame)
        
        card_frame = ttk.Frame(card_canvas,
                               width=bt_frame.winfo_width(),
                               )
        
        card_frame.grid(row=0,column=0,sticky='nsew')

        card_canvas.grid(row=0,column=0,padx=10,pady=5,sticky='nsew')
        
        card_canvas.create_window((0,0),window=card_frame,anchor='nw',tags='frame')
        
        card_canvas.configure(height=500)

        list_cards(news, 
                   bt_frame.winfo_width(),
                   card_frame,
                   editor_wd,
                   controller.show_window,
                   self_page=self,
                   window=self,
                   master=self.master)
        
        if len(news.cards) > 16:
            scroll = tk.Scrollbar(list_frame,orient="vertical")
            scroll.grid(row=0,column=1,sticky='ns')
            scroll.config(command=card_canvas.yview)

            card_canvas.configure(scrollregion=[0,0,bt_frame.winfo_width(),len(news.cards)*30],
                                  yscrollcommand=scroll.set
                                  )

        
        #-BOTÃO DE VOLTAR
        bt_back = ttk.Button(bt_frame,text='Voltar',
                            width=8,
                            command=lambda: controller.show_frame(self,home_page))
        bt_back.grid(row=1,column=0,padx=10)

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
    
        list_frame_col,list_frame_row=card_frame.size()
        list_frame.columnconfigure([0],weight=1)
        
        pv_frame_col,pv_frame_row=pv_frame.size()
        pv_frame.rowconfigure([i for i in range(pv_frame_row)],weight=1)
        pv_frame.columnconfigure([i for i in range(pv_frame_col)],weight=1)
        
        bt_frame_col,bt_frame_row=bt_frame.size()
        bt_frame.rowconfigure([i for i in range(bt_frame_row)],weight=1)
        bt_frame.columnconfigure([i for i in range(bt_frame_col)],weight=1)
        bt_frame.rowconfigure(1,weight=0)