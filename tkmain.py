# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 17:23:21 2022

@author: valter.gonzaga
"""
import tkinter as tk
import ttkthemes as themes
from tkinter import colorchooser
from home_page import home_page

import cfg
from News_Builder import card

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

class App(themes.ThemedTk):
        
    #----------------------------------------------------------
    #CONFIGURAÇÕES INICIAIS
    #----------------------------------------------------------
    def __init__(self,*args, **kwargs):
        #-------------
        #-Dados da GUI
        #-------------
        themes.ThemedTk.__init__(self,theme='arc',*args, **kwargs)
        
        #self.tk.call('source','sun-valley.tcl')
        #self.tk.call('set_theme','dark')
        
        self.geometry('1000x700')
        self.update()
        
        #----------------------------------------------------------
        #REFERÊNCIAS EXTERNAS
        #----------------------------------------------------------
        
        #---------------------
        #-Icone do Conta Gotas
        #---------------------
        colorpicker_file = tk.PhotoImage(file=r'Media/icon_color_picker.png')
        colorpicker_icon = colorpicker_file.subsample(45,45)
        
        self.colorpicker_icon = colorpicker_icon
        
        #-------------------------
        #-Icone do Seta para Baixo
        #-------------------------
        dpdown_icon = tk.PhotoImage(file=r'Media/icon_drop_down_arrow.png')
        dpdown_icon = dpdown_icon.subsample(40,40)
        
        self.dpdown_icon = dpdown_icon
        
        #-------------------------
        #-Icone de Atualizar
        #-------------------------
        refresh_icon = tk.PhotoImage(file=r'Media/icon_refresh.png')
        refresh_icon = refresh_icon.subsample(4,4)
        
        self.refresh_icon = refresh_icon
        
        #-------------------------
        #-Icone de Exportar
        #-------------------------
        export_icon = tk.PhotoImage(file=r'Media/icon_export.png')
        export_icon = export_icon.subsample(3,3)
        
        self.export_icon = export_icon
        
        #-------------------------
        #-Icone de Ajudo
        #-------------------------
        help_icon = tk.PhotoImage(file=r'Media/icon_help.png')
        help_icon = help_icon.subsample(3,3)
        
        self.help_icon = help_icon
        
        #-------------------------
        #-Icone de Navegador
        #-------------------------
        browser_icon = tk.PhotoImage(file=r'Media/icon_browser.png')
        browser_icon = browser_icon.subsample(4,4)
        
        self.browser_icon = browser_icon
        
        #--------------
        #-Frame Inicial
        #--------------
        frame = home_page(parent=self, controller=self)
        frame.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        

    #----------------------------------------------------------
    #FUNÇÃO: EXIBIR NOVOS FRAMES
    #----------------------------------------------------------        
    def show_frame(self,current_self, page_class,*args,**kwargs):
        
        frame = page_class(parent=self, controller=self,*args,**kwargs)
        frame.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)

    #----------------------------------------------------------
    #FUNÇÃO: EXIBIR NOVAS JANELAS
    #----------------------------------------------------------           
    def show_window(self,window_class,*args,**kwargs):
        
        window_class(master=self,*args,**kwargs)
        
    #----------------------------------------------------------
    #FUNÇÃO: EXIBIR SELETOR DE CORES
    #----------------------------------------------------------    
    def colorpicker(self,parent,color_var):
        
        color_code = colorchooser.askcolor(parent=parent)
        color_var.set(color_code[1])
    
    
    def BuildLetter(self,
                    newsletter,
                    format_dict=format_dict):
        
        mime_letter,html_letter = newsletter.build_letter()
        with open('cards_text.html','w',encoding='utf8') as cards_text:
            cards_text.write(html_letter)
        with open('display_text.html','w',encoding='utf8') as display_text:
            display_text.write(html_letter)   
        with open('display_text.eml','w',encoding='utf8') as display_text:
            display_text.write(mime_letter)    
    
    def createCard(self,
                   newsletter,
                   info,
                   format_dict=format_dict,
                   pos='end'):
        
        #---------------------------
        #Dicionário de dados do card
        #---------------------------
        
        banner=info['banner']
        bn_mode=info['banner_mode']
        bn_link=info['banner_link']
        bn_caption=info['banner_caption']
        footer=info['footer']
        ft_mode=info['footer_mode']
        ft_link=info['footer_link']
        ft_caption=info['footer_caption']
        header=info['header']
        title=info['title']
        body=info['body']
        
        
        bn_extension=''
        ft_extension=''
        if type(banner) == str:
            banner_path_sections = banner.split('.')
            bn_extension = banner_path_sections[len(banner_path_sections)-1]
        else:
            banner = ''
            
        if type(footer) == str:
            footer_path_sections = footer.split('.')
            ft_extension = footer_path_sections[len(footer_path_sections)-1]
        else:
            footer=''
        
        
        #--------------------------------
        #Parâmetros de formatação do card
        #--------------------------------
        
        
        border_color = format_dict['border_color']
        border_thickness = format_dict['border_thickness']+'px'
        border_radius = format_dict['border_radius']+'px'
        border_toggle = bool(int(format_dict['border_toggle']))
        border_padx = str(format_dict['border_padx'])
        border_pady = str(format_dict['border_pady'])
        max_width = int(format_dict['max_width'])
        
        body_font = format_dict['body_font']
        body_size = format_dict['body_size']+'px'
        body_padx = str(format_dict['body_padx'])
        body_pady = str(format_dict['body_pady'])
        
        tab_handler = format_dict['tab_handler']
        
        header_font = format_dict['header_font']
        header_size = format_dict['header_size']+'px'
        header_bold = bool(int(format_dict['header_bold']))
        header_color = format_dict['header_color']
        header_padx = str(format_dict['header_padx'])
        header_pady = str(format_dict['header_pady'])
        
        banner_padx = str(format_dict['banner_padx'])
        banner_pady = str(format_dict['banner_pady'])
        
        title_font = format_dict['title_font']
        title_size = format_dict['title_size']+'px'
        title_bold = bool(format_dict['title_bold'])
        
        sectitle_font = format_dict['sectitle_font']
        sectitle_size = format_dict['sectitle_size']+'px'
        sectitle_bold = bool(int(format_dict['sectitle_bold']))
        
        footer_font = format_dict['footer_font']
        footer_size = format_dict['footer_size']+'px'
        footer_padx = str(format_dict['footer_padx'])
        footer_pady = str(format_dict['footer_pady'])
        
        #-----------------
        #Confecção do card
        #-----------------

        new_card = card(newsletter=newsletter,
                        banner=banner,
                        banner_mode=bn_mode,
                        banner_extension=bn_extension,
                        banner_hyperlink=bn_link,
                        banner_caption=bn_caption,
                        banner_padx=banner_padx,
                        banner_pady=banner_pady,
                        footer=footer,
                        footer_mode=ft_mode,
                        footer_extension=ft_extension,
                        footer_hyperlink=ft_link,
                        footer_font=footer_font,
                        footer_size=footer_size,
                        footer_caption=ft_caption,
                        footer_padx=footer_padx,
                        footer_pady=footer_pady,
                        header=header,
                        header_font=header_font,
                        header_size=header_size,
                        header_bold=header_bold,
                        header_color=header_color,
                        header_padx=header_padx,
                        header_pady=header_pady,
                        title=title,
                        title_font=title_font,
                        title_size=title_size,
                        title_bold=title_bold,
                        body=body,
                        body_font=body_font,
                        body_size=body_size,
                        body_padx=body_padx,
                        body_pady=body_pady,
                        tab_handler=tab_handler,
                        sectitle_font=sectitle_font,
                        sectitle_size=sectitle_size,
                        sectitle_bold=sectitle_bold,
                        border_color=border_color,
                        border_thickness=border_thickness,
                        border_corner_radius=border_radius,
                        border_toggle=border_toggle,
                        border_padx=border_padx,
                        border_pady=border_pady,
                        max_width=max_width
                        )
        
        new_card.set_info(info)
        
        newsletter.add_card(new_card,pos)
        
        self.BuildLetter(newsletter=newsletter,
                         format_dict=format_dict)  
            