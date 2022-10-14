# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 15:49:53 2022

@author: valter.gonzaga
"""
import string
import tkinter as tk
import os

"""
#----------------------------------------------------------------------
#FUNÇÃO: OBTER ARQUIVOS DA MEMÓRIA
#----------------------------------------------------------------------
"""

def fetch_data(path):
    """
    os padrões são estruturados, documentar como funciona!!!!

    Parameters
    ----------
    path : TYPE
        DESCRIPTION.

    Returns
    -------
    data_dict : TYPE
        DESCRIPTION.

    """
    with open(path,'r',encoding='utf-8') as cfg:
        data = cfg.read().split('\n')
        data = [(line.split('=')[0],line.split('=')[1]) for line in data
                if line != '']
        
        data_dict = dict(data)
        
        #CHECAGEM SE OS VALORES SÃO UMA LISTA
        for key,value in data_dict.items():
            value_list = value.split(';')
            if len(value_list) > 1:
                data_dict[key] = tuple(value_list)
        
        return data_dict
    
"""
===============================================================================
#FUNÇÃO: ESCREVER ARQUIVOS NA MEMÓRIA
===============================================================================
"""

def store_data(path,data_dict):
    text_formated = "\n".join([f'{str(key)}={str(value)}' 
                               if type(value) != tuple 
                               else f'{str(key)}={";".join(list(map(str,value)))}'
                               for key,value in data_dict.items()    
                               ]
                              )
    
    with open(path,'w',encoding='utf-8') as cfg:
        cfg.write(text_formated)
"""
===============================================================================
#FUNÇÃO: TRADUZIR LETRA DE COLUNA PARA NÚMERO
===============================================================================
"""
def col2num(col):
    num = 0

    
    for multi_idx,c in enumerate(col):
        if c in string.ascii_letters:
            
            num = (num 
                   + ((ord(c.upper())-ord('A')+1)
                      *26**(len(col)-(multi_idx+1))
                      )
                   )
            
    return num-1

"""
===============================================================================
#FUNÇÃO: SALVAR DADOS EM NOVO ARQUIVO .EML
===============================================================================
"""

def exportEML():
    with open('display_text.eml','r',encoding='utf8') as root_file:
        root_data = root_file.read()
        root_file.close()
    
    new_file = tk.filedialog.asksaveasfile(defaultextension ='*.*',
                                           filetypes=[('E-mail Outlook','*.eml'),
                                                      ('Todos os Arquivos','*.*')
                                                      ]
                                           )
    
    with open(new_file.name,'w',encoding='utf8') as file:
        file.write(root_data)
        file.close()
        
"""
===============================================================================
#FUNÇÃO: NAVEGAR POR EXPLORADOR DE ARQUIVOS
===============================================================================
"""

def browseFiles(var:tk.StringVar,*args):
    
        from cfg import browse_path

        file_path = tk.filedialog.askopenfilename(initialdir = browse_path,
                                                  title = "Select a File")
        var.set(file_path)
        
        if file_path != browse_path and file_path != '':
            browse_path = file_path
            store_data('Data/config.cfg', {'browse_path':file_path})

def RefreshPv(display_widget):
    with open('cards_text.html','r',encoding='utf8') as card_text:
        display_text = card_text.read()

    with open('display_text.html','w',encoding='utf8') as display:
        display.write(display_text)
    
    with open('display_text.html','r',encoding='utf8') as display:
        display_widget.load_html(display.read())

def Helper(display_widget):

    with open('display_text.html','w',encoding='utf-8') as display:
        with open('help_text.html','r',encoding='utf-8') as help_text:
            entry_message = help_text.read().replace('<self_file>',
                                                     'display_text.html'
                                                     )
        
        display.write(entry_message)
        display.close()  
        
        
    with open('display_text.html','r',encoding='utf-8') as display:
        display_widget.load_html(display.read())
        
        
def DisplayBrowser():
    os.system('display_text.html')
        
        

        