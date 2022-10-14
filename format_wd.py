# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 14:24:40 2022

@author: valter.gonzaga
"""
import tkinter as tk
from tkinter import ttk
import util



#====================
#Janela de Formatação
#====================

class format_wd(tk.Toplevel):
    def __init__(self,
                 title = 'Opções de Formatação',
                 size = '600x350',
                 master = None):
        
        from cfg import (format_data_path,
                         format_dict)
        

        
        super().__init__(master = master)
        self.title(title)
        self.geometry(f'{size}+{0}+{0}')
        self.resizable(False,False)
        
        
        self.root_frame = ttk.Frame(self)
        self.root_frame.grid(row=0,column=0,sticky='nsew')
        self.rowconfigure([0],weight=1)
        self.columnconfigure([0],weight=1)
        
        self.root_menus = ttk.Notebook(self.root_frame)
        self.root_menus.grid(row=0,column=0,sticky='nsew')
        

        #======================================================
        #FUNÇÃO: CARREGAR PERFIL
        #======================================================
        def load_button():
                from profilers import (profiler, 
                                       profile_load_wd,
                                       profile_save_wd,
                                       format_profiler)
                
                master.show_window(profile_load_wd,
                                   parent=self,
                                   parent_class=('window',format_wd),
                                   profiler_obj=format_profiler,
                                   data_dict=format_dict)

        #---------------------------------------------------------------
        #OPÇÕES PARA A BORDA
        #---------------------------------------------------------------
        
        #------
        #-Frame
        #------
        border_frame = ttk.Frame(self.root_menus)
        border_frame.grid(row=0,column=0,padx=10,pady=10,sticky='nw')

        
        #-----------------------
        #-Ligar e Desligar Borda
        #-----------------------
        
        #--Label
        border_list_label = ttk.Label(border_frame,text='Utilizar borda:',anchor='w')
        border_list_label.grid(row=0,column=0,padx=(10,5),pady=10,sticky='w')
        
        border_radial_frame = ttk.Frame(border_frame)
        border_radial_frame.grid(row=0,column=1,padx=10,pady=10,sticky='ew')
        
        
        self.toggle_bdr = tk.StringVar()
        self.toggle_bdr.set(bool(int(format_dict['border_toggle'])))
        
        border_list_true = ttk.Radiobutton(border_radial_frame,
                                           text='Ligada',
                                           var=self.toggle_bdr,
                                           value=True
                                           )
        border_list_true.grid(row=0,column=0,sticky='w')
        
        border_list_false = ttk.Radiobutton(border_radial_frame,
                                            text='Desligada',
                                            var=self.toggle_bdr,
                                            value=False
                                            )
        border_list_false.grid(row=1,column=0,sticky='w')
        
        
        #---------------
        #-Escolha da Cor
        #---------------
        
        #--Label
        border_color_label = ttk.Label(border_frame,text='Cor:',anchor='w')
        border_color_label.grid(row=1,column=0,padx=(10,5),pady=2,sticky='w')
        
        #--Entrada
        self.color_bdr = tk.StringVar()
        self.color_bdr.set(format_dict['border_color'])
        border_color_entry = ttk.Entry(border_frame,textvariable = self.color_bdr,width='10')
        border_color_entry.grid(row=1,column=1,padx=10,pady=2,sticky='ew')  
        
        #--Botão conta-gotas
        border_color_button = ttk.Button(border_frame,
                                         image=master.colorpicker_icon,
                                         width=20,
                                         command=lambda: master.colorpicker(parent=self,color_var=self.color_bdr)
                                         )
        border_color_button.grid(row=1,column=2,padx=(2,10),pady=20)
        
        #---------------------
        #-Escolha da Expessura
        #---------------------
        
        #--Label
        border_thick_label = ttk.Label(border_frame,text='Espessura:',anchor='w')
        border_thick_label.grid(row=2,column=0,padx=(10,5),pady=2,sticky='w')
        
        #--Entrada
        self.thick_bdr = tk.StringVar()
        self.thick_bdr.set(format_dict['border_thickness'])
        border_thick_entry = ttk.Entry(border_frame,textvariable = self.thick_bdr,width='4')
        border_thick_entry.grid(row=2,column=1,padx=(10,1),pady=2,sticky='ew') 
        
        #--Label Unidades de Medida
        border_thick_units = ttk.Label(border_frame,text='px',anchor='w')
        border_thick_units.grid(row=2,column=2,padx=(1,10),pady=2,sticky='w')
        
        #-------------------------
        #-Escolha do Raio da Borda
        #-------------------------
        
        #--Label
        border_radius_label = ttk.Label(border_frame,text='Raio de Borda:',anchor='w')
        border_radius_label.grid(row=3,column=0,padx=(10,5),pady=2,sticky='w')
        
        #--Entrada
        self.radius_bdr = tk.StringVar()
        self.radius_bdr.set(format_dict['border_radius'])
        border_rad_entry = ttk.Entry(border_frame,textvariable =self.radius_bdr,width='4')
        border_rad_entry.grid(row=3,column=1,padx=(10,1),pady=2,sticky='ew') 
        
        #--Label Unidades de Medida
        border_rad_units = ttk.Label(border_frame,text='px',anchor='w')
        border_rad_units.grid(row=3,column=2,padx=(1,10),pady=2,sticky='w')
        
        #-------------------------
        #-Escolha do Padding
        #-------------------------
        
        #--Label
        border_padx_label = ttk.Label(border_frame,text='Margem horizontal:',anchor='w')
        border_padx_label.grid(row=4,column=0,padx=(10,5),pady=2,sticky='w')
        
        #--Entpada
        self.padx_bdr = tk.StringVar()
        self.padx_bdr.set(format_dict['border_padx'])
        border_pad_entry = ttk.Entry(border_frame,
                                     textvariable = self.padx_bdr,
                                     width='4')
        border_pad_entry.grid(row=4,column=1,padx=(10,1),pady=2,sticky='ew') 
        
        #--Label Unidades de Medida
        border_pad_units = ttk.Label(border_frame,text='%',anchor='w')
        border_pad_units.grid(row=4,column=2,padx=(1,10),pady=2,sticky='w')
        
        #--Label
        border_pady_label = ttk.Label(border_frame,text='Margem vertical:',anchor='w')
        border_pady_label.grid(row=5,column=0,padx=(10,5),pady=2,sticky='w')
        
        #--Entpada
        self.pady_bdr = tk.StringVar()
        self.pady_bdr.set(format_dict['border_pady'])
        border_pad_entry = ttk.Entry(border_frame,
                                     textvariable = self.pady_bdr,
                                     width='4')
        border_pad_entry.grid(row=5,column=1,padx=(10,1),pady=2,sticky='ew') 
        
        #--Label Unidades de Medida
        border_pad_units = ttk.Label(border_frame,text='%',anchor='w')
        border_pad_units.grid(row=5,column=2,padx=(1,10),pady=2,sticky='w')
        
        #-------------------------
        #-Escolha da Largura Maxima
        #-------------------------
        
        #--Label
        border_wd_label = ttk.Label(border_frame,text='Largura Máxima:',anchor='w')
        border_wd_label.grid(row=6,column=0,padx=(10,5),pady=2,sticky='w')
        
        #--Entpada
        self.wd_bdr = tk.StringVar()
        self.wd_bdr.set(format_dict['max_width'])
        border_wd_entry = ttk.Entry(border_frame,
                                    textvariable = self.wd_bdr,
                                    width='4')
        border_wd_entry.grid(row=6,column=1,padx=(10,1),pady=2,sticky='ew') 
        
        #--Label Unidades de Medida
        border_wd_units = ttk.Label(border_frame,text='px',anchor='w')
        border_wd_units.grid(row=6,column=2,padx=(1,10),pady=2,sticky='w')
        
        #---------------------------------------------------------------
        #OPÇÕES PARA O BANNER DO TEXTO
        #---------------------------------------------------------------
        
        #------
        #-Frame
        #------
        banner_frame = ttk.Frame(self.root_menus)
        banner_frame.grid(row=10,column=0,padx=10,pady=2,sticky='nw')
           
        #-------------------------
        #-Escolha do Padding
        #-------------------------
        
        #--Label
        banner_padx_label = ttk.Label(banner_frame,text='Margem horizontal:',anchor='w')
        banner_padx_label.grid(row=0,column=0,padx=(10,5),pady=2,sticky='w')
        
        #--Entpada
        self.padx_bn = tk.StringVar()
        self.padx_bn.set(format_dict['banner_padx'])
        banner_pad_entry = ttk.Entry(banner_frame,
                                     textvariable = self.padx_bn,
                                     width='4')
        banner_pad_entry.grid(row=0,column=1,padx=(10,1),pady=2,sticky='ew') 
        
        #--Label Unidades de Medida
        banner_pad_units = ttk.Label(banner_frame,text='%',anchor='w')
        banner_pad_units.grid(row=0,column=2,padx=(1,10),pady=2,sticky='w')
        
        #--Label
        banner_pady_label = ttk.Label(banner_frame,text='Margem vertical:',anchor='w')
        banner_pady_label.grid(row=1,column=0,padx=(10,5),pady=2,sticky='w')
        
        #--Entrada
        self.pady_bn = tk.StringVar()
        self.pady_bn.set(format_dict['banner_pady'])
        banner_pad_entry = ttk.Entry(banner_frame,
                                     textvariable = self.pady_bn,
                                     width='4')
        banner_pad_entry.grid(row=1,column=1,padx=(10,1),pady=2,sticky='ew') 
        
        #--Label Unidades de Medida
        banner_pad_units = ttk.Label(banner_frame,text='%',anchor='w')
        banner_pad_units.grid(row=1,column=2,padx=(1,10),pady=2,sticky='w')
        
        
        #---------------------------------------------------------------
        #OPÇÕES PARA O CORPO DO TEXTO
        #---------------------------------------------------------------
        
        #------
        #-Frame
        #------
        body_frame = ttk.Frame(self.root_menus)
        body_frame.grid(row=2,column=0,padx=10,pady=10,sticky='nw')
        
        
        #-----------------
        #-Seleção da Fonte
        #-----------------
        
        #--Label
        body_font_label = ttk.Label(body_frame,text='Fonte:',anchor='w')
        body_font_label.grid(row=0,column=0,padx=(10,5),pady=(10,2),sticky='w')
        
        #--Entrada
        self.font_bd = tk.StringVar()
        self.font_bd.set(format_dict['body_font'])
        body_font_entry = ttk.Entry(body_frame,textvariable = self.font_bd)
        body_font_entry.grid(row=0,column=1,padx=10,pady=(10,2),sticky='ew')
        
        
        #----------------------------
        #-Escolha do Tamanho da Fonte
        #----------------------------
        
        #--Label
        body_size_label = ttk.Label(body_frame,text='Tamanho da Fonte:',anchor='w')
        body_size_label.grid(row=1,column=0,padx=(10,5),pady=2,sticky='w')
        
        #--Entrada
        self.size_bd = tk.StringVar()
        self.size_bd.set(format_dict['body_size'])
        body_size_entry = ttk.Entry(body_frame,textvariable = self.size_bd,width='4')
        body_size_entry.grid(row=1,column=1,padx=(10,1),pady=2,sticky='ew') 
        
        #--Label Unidades de Medida
        body_size_units = ttk.Label(body_frame,text='pt',anchor='w')
        body_size_units.grid(row=1,column=2,padx=(1,10),pady=2,sticky='w')
        
        #----------------------------
        #-Escolha do Tipo de Listagem
        #----------------------------
        
        #--Label
        body_list_label = ttk.Label(body_frame,text='Listas:',anchor='w')
        body_list_label.grid(row=2,column=0,padx=(10,5),pady=2,sticky='w')
        
        body_radial_frame = ttk.Frame(body_frame)
        body_radial_frame.grid(row=2,column=1,padx=10,pady=2,sticky='ew')
        
        
        self.listopt_bd = tk.StringVar()
        self.listopt_bd.set(format_dict['tab_handler'])
        
        body_list_true = ttk.Radiobutton(body_radial_frame,text='Tópicos',
                                         var=self.listopt_bd,value='bullet')
        body_list_true.grid(row=0,column=0,sticky='w')
        
        body_list_false = ttk.Radiobutton(body_radial_frame,text='Numérica',
                                         var=self.listopt_bd,value='enumerada')
        body_list_false.grid(row=1,column=0,sticky='w')
        
        body_list_false = ttk.Radiobutton(body_radial_frame,text='Descrição',
                                         var=self.listopt_bd,value='descrição')
        body_list_false.grid(row=2,column=0,sticky='w')

        
        #-------------------------
        #-Escolha do Padding
        #-------------------------
        
        #--Label
        body_padx_label = ttk.Label(body_frame,text='Margem horizontal:',anchor='w')
        body_padx_label.grid(row=3,column=0,padx=(10,5),pady=2,sticky='w')
        
        #--Entpada
        self.padx_bd = tk.StringVar()
        self.padx_bd.set(format_dict['body_padx'])
        body_pad_entry = ttk.Entry(body_frame,
                                     textvariable = self.padx_bd,
                                     width='4')
        body_pad_entry.grid(row=3,column=1,padx=(10,1),pady=2,sticky='ew') 
        
        #--Label Unidades de Medida
        body_pad_units = ttk.Label(body_frame,text='%',anchor='w')
        body_pad_units.grid(row=3,column=2,padx=(1,10),pady=2,sticky='w')
        
        #--Label
        body_pady_label = ttk.Label(body_frame,text='Margem vertical:',anchor='w')
        body_pady_label.grid(row=4,column=0,padx=(10,5),pady=2,sticky='w')
        
        #--Entpada
        self.pady_bd = tk.StringVar()
        self.pady_bd.set(format_dict['body_pady'])
        body_pad_entry = ttk.Entry(body_frame,
                                     textvariable = self.pady_bd,
                                     width='4')
        body_pad_entry.grid(row=4,column=1,padx=(10,1),pady=2,sticky='ew') 
        
        #--Label Unidades de Medida
        body_pad_units = ttk.Label(body_frame,text='%',anchor='w')
        body_pad_units.grid(row=4,column=2,padx=(1,10),pady=2,sticky='w')
        
        
        #---------------------------------------------------------------
        #OPÇÕES PARA O TÍTULO DO TEXTO
        #---------------------------------------------------------------
        
        #------
        #-Frame
        #------
        title_frame = ttk.Frame(self.root_menus)
        title_frame.grid(row=4,column=0,padx=10,pady=10,sticky='nw')
        
        
        #-----------------
        #-Seleção da Fonte
        #-----------------
        
        #--Label
        title_font_label = ttk.Label(title_frame,text='Fonte:',anchor='w')
        title_font_label.grid(row=0,column=0,padx=(10,5),pady=2,sticky='w')
        
        #--Entrada
        self.font_ttl = tk.StringVar()
        self.font_ttl.set(format_dict['title_font'])
        title_font_entry = ttk.Entry(title_frame,textvariable = self.font_ttl)
        title_font_entry.grid(row=0,column=1,padx=10,pady=2,sticky='ew')
        
        
        #----------------------------
        #-Escolha do Tamanho da Fonte
        #----------------------------
        
        #--Label
        title_size_label = ttk.Label(title_frame,text='Tamanho da Fonte:',anchor='w')
        title_size_label.grid(row=1,column=0,padx=(10,5),pady=2,sticky='w')
        
        #--Entrada
        self.size_ttl = tk.StringVar()
        self.size_ttl.set(format_dict['title_size'])
        title_size_entry = ttk.Entry(title_frame,textvariable = self.size_ttl,width='4')
        title_size_entry.grid(row=1,column=1,padx=(10,1),pady=2,sticky='ew') 
        
        #--Label Unidades de Medida
        title_size_units = ttk.Label(title_frame,text='pt',anchor='w')
        title_size_units.grid(row=1,column=2,padx=(1,10),pady=2,sticky='w')
        
        #-----------------------------
        #-Escolha entre Negrito ou Não
        #-----------------------------
        
        #--Label
        title_bold_label = ttk.Label(title_frame,text='Formatação:',anchor='w')
        title_bold_label.grid(row=2,column=0,padx=(10,5),pady=2,sticky='w')
        
        title_radial_frame = ttk.Frame(title_frame)
        title_radial_frame.grid(row=2,column=1,padx=10,pady=2,sticky='ew')
        
        
        self.boldopt_ttl = tk.StringVar()
        self.boldopt_ttl.set(format_dict['title_bold'])
        
        title_bold_true = ttk.Radiobutton(title_radial_frame,text='Negrito',
                                         var=self.boldopt_ttl,value='1')
        title_bold_true.grid(row=0,column=0,sticky='w')
        
        title_bold_false = ttk.Radiobutton(title_radial_frame,text='Normal',
                                         var=self.boldopt_ttl,value='0')
        title_bold_false.grid(row=1,column=0,sticky='w')
        
        
        
        #---------------------------------------------------------------
        #OPÇÕES PARA OS SUBTÍTULOS DO TEXTO
        #---------------------------------------------------------------
        
        #------
        #-Frame
        #------
        sectitle_frame = ttk.Frame(self.root_menus)
        sectitle_frame.grid(row=6,column=0,padx=10,pady=10,sticky='nw')
        
        #-----------------
        #-Seleção da Fonte
        #-----------------
        
        #--Label
        sectitle_font_label = ttk.Label(sectitle_frame,text='Fonte:',anchor='w')
        sectitle_font_label.grid(row=0,column=0,padx=(10,5),pady=2,sticky='w')
        
        #--Entrada
        self.font_sct = tk.StringVar()
        self.font_sct.set(format_dict['sectitle_font'])
        sectitle_font_entry = ttk.Entry(sectitle_frame,textvariable = self.font_sct)
        sectitle_font_entry.grid(row=0,column=1,padx=10,pady=2,sticky='ew')
        
        
        #----------------------------
        #-Escolha do Tamanho da Fonte
        #----------------------------
        
        #--Label
        sectitle_size_label = ttk.Label(sectitle_frame,text='Tamanho da Fonte:',font='Times',anchor='w')
        sectitle_size_label.grid(row=1,column=0,padx=(10,5),pady=2,sticky='w')
        
        #--Entrada
        self.size_sct = tk.StringVar()
        self.size_sct.set(format_dict['sectitle_size'])
        sectitle_size_entry = ttk.Entry(sectitle_frame,textvariable = self.size_sct,width='4')
        sectitle_size_entry.grid(row=1,column=1,padx=(10,1),pady=2,sticky='ew') 
        
        #--Label Unidades de Medida
        sectitle_size_units = ttk.Label(sectitle_frame,text='pt',anchor='w')
        sectitle_size_units.grid(row=1,column=2,padx=(1,10),pady=2,sticky='w')
        
        #-----------------------------
        #-Escolha entre Negrito ou Não
        #-----------------------------
        
        #--Label
        sectitle_bold_label = ttk.Label(sectitle_frame,text='Formatação:',anchor='w')
        sectitle_bold_label.grid(row=2,column=0,padx=(10,5),pady=2,sticky='w')
        
        sectitle_radial_frame = ttk.Frame(sectitle_frame)
        sectitle_radial_frame.grid(row=2,column=1,padx=10,pady=2,sticky='ew')
        
        
        self.boldopt_sct = tk.StringVar()
        self.boldopt_sct.set(format_dict['sectitle_bold'])
        
        sectitle_bold_true = ttk.Radiobutton(sectitle_radial_frame,text='Negrito',
                                         var=self.boldopt_sct,value='1')
        sectitle_bold_true.grid(row=0,column=0,sticky='w')
        
        sectitle_bold_false = ttk.Radiobutton(sectitle_radial_frame,text='Normal',
                                         var=self.boldopt_sct,value='0')
        sectitle_bold_false.grid(row=1,column=0,sticky='w')
        
        
        #---------------------------------------------------------------
        #OPÇÕES PARA O RODAPÉ
        #---------------------------------------------------------------
        
        #------
        #-Frame
        #------
        footer_frame = ttk.Frame(self.root_menus)
        footer_frame.grid(row=8,column=0,padx=10,pady=10,sticky='nw')
        
        #-----------------
        #-Seleção da Fonte
        #-----------------
        
        #--Label
        footer_font_label = ttk.Label(footer_frame,text='Fonte:',anchor='w')
        footer_font_label.grid(row=0,column=0,padx=(10,5),pady=2,sticky='w')
        
        #--Entrada
        self.font_ft = tk.StringVar()
        self.font_ft.set(format_dict['footer_font'])
        footer_font_entry = ttk.Entry(footer_frame,textvariable = self.font_ft)
        footer_font_entry.grid(row=0,column=1,padx=10,pady=2,sticky='ew')
        
        
        #----------------------------
        #-Escolha do Tamanho da Fonte
        #----------------------------
        
        #--Label
        footer_size_label = ttk.Label(footer_frame,text='Tamanho da Fonte:',anchor='w')
        footer_size_label.grid(row=1,column=0,padx=(10,5),pady=2,sticky='w')
        
        #--Entrada
        self.size_ft = tk.StringVar()
        self.size_ft.set(format_dict['footer_size'])
        footer_size_entry = ttk.Entry(footer_frame,textvariable = self.size_ft,width='4')
        footer_size_entry.grid(row=1,column=1,padx=(10,1),pady=2,sticky='ew') 
        
        #--Label Unidades de Medida
        footer_size_units = ttk.Label(footer_frame,text='pt',anchor='w')
        footer_size_units.grid(row=1,column=2,padx=(1,10),pady=2,sticky='w')
        
        #-------------------------
        #-Escolha do Padding
        #-------------------------
        
        #--Label
        footer_padx_label = ttk.Label(footer_frame,text='Margem horizontal:',anchor='w')
        footer_padx_label.grid(row=2,column=0,padx=(10,5),pady=2,sticky='w')
        
        #--Entpada
        self.padx_ft = tk.StringVar()
        self.padx_ft.set(format_dict['footer_padx'])
        footer_pad_entry = ttk.Entry(footer_frame,
                                     textvariable = self.padx_ft,
                                     width='4')
        footer_pad_entry.grid(row=2,column=1,padx=(10,1),pady=2,sticky='ew') 
        
        #--Label Unidades de Medida
        footer_pad_units = ttk.Label(footer_frame,text='%',anchor='w')
        footer_pad_units.grid(row=2,column=2,padx=(1,10),pady=2,sticky='w')
        
        #--Label
        footer_pady_label = ttk.Label(footer_frame,text='Margem vertical:',anchor='w')
        footer_pady_label.grid(row=3,column=0,padx=(10,5),pady=2,sticky='w')
        
        #--Entrada
        self.pady_ft = tk.StringVar()
        self.pady_ft.set(format_dict['footer_pady'])
        footer_pad_entry = ttk.Entry(footer_frame,
                                     textvariable = self.pady_ft,
                                     width='4')
        footer_pad_entry.grid(row=3,column=1,padx=(10,1),pady=2,sticky='ew') 
        
        #--Label Unidades de Medida
        footer_pad_units = ttk.Label(footer_frame,text='%',anchor='w')
        footer_pad_units.grid(row=3,column=2,padx=(1,10),pady=2,sticky='w')
        
        #---------------------------------------------------------------
        #OPÇÕES PARA O CABEÇALHO DO TEXTO
        #---------------------------------------------------------------
        
        #------
        #-Frame
        #------
        header_frame = ttk.Frame(self.root_menus)
        header_frame.grid(row=10,column=0,padx=10,pady=2,sticky='nw')
        
        #-----------------
        #-Seleção da Fonte
        #-----------------
        
        #--Label
        header_font_label = ttk.Label(header_frame,text='Fonte:',anchor='w')
        header_font_label.grid(row=0,column=0,padx=(10,5),pady=2,sticky='w')
        
        #--Entrada
        self.font_hd = tk.StringVar()
        self.font_hd.set(format_dict['header_font'])
        header_font_entry = ttk.Entry(header_frame,textvariable = self.font_hd)
        header_font_entry.grid(row=0,column=1,padx=10,pady=2,sticky='ew')
        
        
        #----------------------------
        #-Escolha do Tamanho da Fonte
        #----------------------------
        
        #--Label
        header_size_label = ttk.Label(header_frame,text='Tamanho da Fonte:',anchor='w')
        header_size_label.grid(row=1,column=0,padx=(10,5),pady=2,sticky='w')
        
        #--Entrada
        self.size_hd = tk.StringVar()
        self.size_hd.set(format_dict['header_size'])
        header_size_entry = ttk.Entry(header_frame,textvariable = self.size_hd,width='4')
        header_size_entry.grid(row=1,column=1,padx=(10,1),pady=2,sticky='ew') 
        
        #--Label Unidades de Medida
        header_size_units = ttk.Label(header_frame,text='pt',anchor='w')
        header_size_units.grid(row=1,column=2,padx=(1,10),pady=2,sticky='w')
        
        #-----------------------------
        #-Escolha entre Negrito ou Não
        #-----------------------------
        
        #--Label
        header_bold_label = ttk.Label(header_frame,text='Formatação:',anchor='w')
        header_bold_label.grid(row=2,column=0,padx=(10,5),pady=2,sticky='w')
        
        header_radial_frame = ttk.Frame(header_frame)
        header_radial_frame.grid(row=2,column=1,padx=10,pady=2,sticky='ew')
        
        
        self.boldopt_hd = tk.StringVar()
        self.boldopt_hd.set(format_dict['header_bold'])
        
        header_bold_true = ttk.Radiobutton(header_radial_frame,text='Negrito',
                                         var=self.boldopt_hd,value='1')
        header_bold_true.grid(row=0,column=0,sticky='w')
        
        header_bold_false = ttk.Radiobutton(header_radial_frame,text='Normal',
                                         var=self.boldopt_hd,value='0')
        header_bold_false.grid(row=1,column=0,sticky='w')
        
        #---------------
        #-Escolha da Cor
        #---------------
        
        #--Label
        header_color_label = ttk.Label(header_frame,text='Cor:',anchor='w')
        header_color_label.grid(row=3,column=0,padx=(10,5),pady=2,sticky='w')
        
        #--Entrada
        self.color_hd = tk.StringVar()
        self.color_hd.set(format_dict['header_color'])
        header_color_entry = ttk.Entry(header_frame,textvariable = self.color_hd,width='10')
        header_color_entry.grid(row=3,column=1,padx=10,pady=2,sticky='ew')  
        
        #--Botão conta-gotas
        header_color_button = ttk.Button(header_frame,
                                         image=master.colorpicker_icon,
                                         width=20,
                                        command=lambda: master.colorpicker(color_var=self.color_hd)
                                        )
        header_color_button.grid(row=3,column=2,padx=(2,10),pady=2)
        
        #-------------------------
        #-Escolha do Padding
        #-------------------------
        
        #--Label
        header_padx_label = ttk.Label(header_frame,text='Margem horizontal:',anchor='w')
        header_padx_label.grid(row=4,column=0,padx=(10,5),pady=2,sticky='w')
        
        #--Entpada
        self.padx_hd = tk.StringVar()
        self.padx_hd.set(format_dict['header_padx'])
        header_pad_entry = ttk.Entry(header_frame,
                                     textvariable = self.padx_hd,
                                     width='4')
        header_pad_entry.grid(row=4,column=1,padx=(10,1),pady=2,sticky='ew') 
        
        #--Label Unidades de Medida
        header_pad_units = ttk.Label(header_frame,text='%',anchor='w')
        header_pad_units.grid(row=4,column=2,padx=(1,10),pady=2,sticky='w')
        
        #--Label
        header_pady_label = ttk.Label(header_frame,text='Margem vertical:',anchor='w')
        header_pady_label.grid(row=5,column=0,padx=(10,5),pady=2,sticky='w')
        
        #--Entrada
        self.pady_hd = tk.StringVar()
        self.pady_hd.set(format_dict['header_pady'])
        header_pad_entry = ttk.Entry(header_frame,
                                     textvariable = self.pady_hd,
                                     width='4')
        header_pad_entry.grid(row=5,column=1,padx=(10,1),pady=2,sticky='ew') 
        
        #--Label Unidades de Medida
        header_pad_units = ttk.Label(header_frame,text='%',anchor='w')
        header_pad_units.grid(row=5,column=2,padx=(1,10),pady=2,sticky='w')
        
        #---------------------------------------------------------------
        #BOTÕES
        #---------------------------------------------------------------
        
        #----------------
        #Frame dos Botões
        #----------------
        self.button_frame = ttk.Frame(self.root_frame)
        self.button_frame.grid(row=0,column=1,padx=10,pady=15,sticky='')
        
        #------------------------
        #Botão de Carregar Perfil
        #-------------------------
        self.load_profile_button = ttk.Button(self.button_frame,text='Carregar Perfil',
                                         width=25,
                                        command=lambda: load_button())
        self.load_profile_button.grid(row=0,column=0,padx=10,pady=5,sticky='n')
        
        #----------------------
        #Botão de Salvar Perfil
        #----------------------
        self.save_profile_button = ttk.Button(self.button_frame,text='Salvar como Perfil',
                                         width=25,
                                        command=lambda: self.save_format(mode=2))
        self.save_profile_button.grid(row=1,column=0,padx=10,pady=5,sticky='ns')
        
        
        #--------------------------------
        #Botão de aplicar ao próximo card
        #--------------------------------
        self.apply_button = ttk.Button(self.button_frame,text='Aplicar',
                                         width=25,
                                        command=lambda: self.save_format(mode=0))
        self.apply_button.grid(row=2,column=0,padx=10,pady=5,sticky='ns')
        
        #-----------------------------------
        #Botão de Tornar Configuração Padrão
        #-----------------------------------
        self.default_button = ttk.Button(self.button_frame,
                                         text='Aplicar e Tornar Padrão',
                                         width=25,
                                         command=lambda: self.save_format(mode=1))
        self.default_button.grid(row=3,column=0,padx=10,pady=5,sticky='s')

        
        #---------------------------------------------------------------
        #SEPARADORES
        #---------------------------------------------------------------
        
        
        #---------------------------------------------------------------
        #REDIMENSIONAMENTO DINAMICO
        #---------------------------------------------------------------
        root_col,root_row=self.root_frame.size()

        self.root_frame.rowconfigure([i for i in range(root_row)], weight=1) #Faz com que a fileria de root expanda até a borda 
        self.root_frame.columnconfigure([i for i in range(root_col)], weight=1) #Faz com que a coluna de root expanda até a borda

        
        
        root_col,root_row=self.root_menus.size()

        self.root_menus.rowconfigure([i for i in range(root_row)], weight=1) #Faz com que a fileria de root expanda até a borda 
        self.root_menus.columnconfigure([i for i in range(root_col)], weight=1) #Faz com que a coluna de root expanda até a borda

        #--------------------------------------------------------------
        # ADIÇÃO DOS FRAMES AO NOTEBOOK
        #--------------------------------------------------------------

        self.root_menus.add(border_frame, text='Borda')
        self.root_menus.add(header_frame, text='Cabeçalho')
        self.root_menus.add(banner_frame, text='Banner')
        self.root_menus.add(title_frame, text='Título')
        self.root_menus.add(sectitle_frame, text='Subtítulo')
        self.root_menus.add(body_frame, text='Corpo')
        self.root_menus.add(footer_frame, text='Rodapé')
        
    #======================================================
    #FUNÇÃO: SALVAR OPÇÕES DE FORMATAÇÃO E TORNA-LAS PADRÃO
    #======================================================
    def save_format(self, 
                    mode=0, 
                    profile_name='', 
                    profile_file='Perfil 1.cfg'
                    ):
        """
        Função que salva os dados de formatação.
        
        Parameters
        ----------
        mode : int, optional
            Opções:
                1. `mode` = 0: aplica formatação aos próximos cards. 
                2. `mode` = 1: aplica aos próximos e salva como padrão para o 
                futuro
                3. `mode` = 2: salva como perfil.

        Returns
        -------
        None.

        """
        from cfg import (format_data_path,
                         format_dict)
        
        from profilers import (profiler, 
                               profile_load_wd,
                               profile_save_wd,
                               format_profiler)
        
        #---------------------------------------------------------------
        #SALVAR DADOS OBTIDOS EM ATRIBUTOS DE CLASSE
        #---------------------------------------------------------------
        self.update()
        self.update_idletasks()
        
        self.border_color = self.color_bdr.get()
        self.border_thickness = self.thick_bdr.get()
        self.border_radius = self.radius_bdr.get()
        self.border_padx = self.padx_bdr.get()
        self.border_pady = self.pady_bdr.get()
        self.border_toggle = self.toggle_bdr.get()
        self.border_maxwidth = int(self.wd_bdr.get())
        
        self.header_font = self.font_hd.get()
        self.header_size = self.size_hd.get()
        self.header_bold = self.boldopt_hd.get()
        self.header_color = self.color_hd.get()
        self.header_padx = self.padx_hd.get()
        self.header_pady = self.pady_hd.get()
        
        self.banner_padx = self.padx_bn.get()
        self.banner_pady = self.pady_bn.get()
        
        self.body_font = self.font_bd.get()
        self.body_size = self.size_bd.get()
        self.body_padx = self.padx_bd.get()
        self.body_pady = self.pady_bd.get()
        self.tab_handler = self.listopt_bd.get()
        
        self.title_font = self.font_ttl.get()
        self.title_size = self.size_ttl.get()
        self.title_bold = self.boldopt_ttl.get()
        
        self.sectitle_font = self.font_sct.get()
        self.sectitle_size = self.size_sct.get()
        self.sectitle_bold = self.boldopt_sct.get()
        
        self.footer_font = self.font_ft.get()
        self.footer_size = self.size_ft.get()
        self.footer_padx = self.padx_ft.get()
        self.footer_pady = self.pady_ft.get()
        
        #--------------------------------------
        #-Atualização do dicionário de formatos
        #--------------------------------------

        format_dict['border_color'] = self.border_color
        format_dict['border_thickness'] = self.border_thickness
        format_dict['border_radius'] = self.border_radius
        format_dict['border_toggle'] = self.border_toggle
        format_dict['border_padx'] = self.border_padx
        format_dict['border_pady'] = self.border_pady
        format_dict['max_width'] = self.border_maxwidth
        
        format_dict['header_font'] = self.header_font
        format_dict['header_size'] = self.header_size
        format_dict['header_bold'] = self.header_bold
        format_dict['header_color'] = self.header_color
        format_dict['header_padx'] = self.header_padx
        format_dict['header_pady'] = self.header_pady
        
        format_dict['banner_padx'] = self.banner_padx
        format_dict['banner_pady'] = self.banner_pady
        
        format_dict['body_font'] = self.body_font
        format_dict['body_size'] = self.body_size
        format_dict['body_padx'] = self.body_padx
        format_dict['body_pady'] = self.body_pady
        
        format_dict['tab_handler'] =  self.tab_handler
        
        format_dict['title_font'] = self.title_font
        format_dict['title_size'] = self.title_size
        format_dict['title_bold'] = self.title_bold
        
        format_dict['sectitle_font'] = self.sectitle_font
        format_dict['sectitle_size'] = self.sectitle_size
        format_dict['sectitle_bold'] = self.sectitle_bold
        
        format_dict['footer_font'] = self.footer_font
        format_dict['footer_size'] = self.footer_size
        format_dict['footer_padx'] = self.footer_padx
        format_dict['footer_pady'] = self.footer_pady
        
        
        
        #------------------------------------------------------
        #-mode=1: salva na memória as configurações como padrão 
        #------------------------------------------------------
        if mode == 1:
            util.store_data('Data/format_data.cfg', format_dict)
            
        #------------------------------------------------------
        #-mode=2: salva na memória as configurações como perfil
        #------------------------------------------------------
        if mode == 2:  
            
            self.master.show_window(profile_save_wd,
                                    profiler_obj=format_profiler,
                                    data_dict=format_dict)