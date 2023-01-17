# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 14:36:18 2022

@author: valter.gonzaga
"""
import tkinter as tk
from tkinter import ttk

#========================
#Text Entry Pop-up Window
#========================
class single_entry(tk.Toplevel):
    """  
    Janela pop-up contendo contendo um campo de entrada e botão de confirmação.
    A confirmação chama uma função fornecida no argumento, utilizando como parâmetro
    a entrada obtida no campo de texto.
    
    Atributes
    ----------
    parent : tk.Toplevel ou tk.TK()
        objeto de onde `single_entry` foi chamado.
    parent_func : callable
        função de `parent` que receba como argumentos::
            
            parent_func(popup_output,**kwargs)
            
        onde `**kwargs` deve ser adicionado **obrigatoriamente** e, na ocasião da cahamada
        , conterá as variáveis ``parent = parent``  e  ``popup_window = self``, conforme
        definidos em `single_entry`.
            
    master : tk.TK()
        objeto raíz da GUI.
    size : TYPE, optional
        tamanho da janela conforme formatação de tk.Toplevel.size. 
        O padrão é '150x125'.
    f_kwargs : dict, optional
        argumentos adicionais a serem passados para `parent_func` em adição à `parent`
        e `popup_window`.
        O padrão é {}.
    **kwargs : dict
        argumentos adicionais de formatação da janela, listados a seguir:
            
            - `label_text`: define o texto da chamada da janela; O padrão é 'Entre com os dados:'
            - `default_var`: valor padrão para a entrada de texto;
            - `button_text`: texto do botão. O padrão é 'Avançar'; 
            - `id`: sendo `var` o valor entrado no campo de texto, fornecer uma string de 'id'
              resulta na alteração do retorno enviado a `parent_func`de `var`para ``{id:var}``
    
    Example
    -------
    
    
    """
    def __init__(self,
                 parent,
                 parent_func,
                 master,
                 size = '300x150',
                 f_kwargs = {},
                 **kwargs):

        super().__init__(master = master)
        
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
        
        self.label_text = kwargs.pop('label_text','Entre com os dados:')
        self.default_var = kwargs.pop('default_var','' )
        self.button_text = kwargs.pop('button_text','Avançar' )
        self.id = kwargs.pop('id','')
        
        def action(self):
            
            popup_output=({str(self.id):self.var.get()} 
                          if self.id != ''
                          else self.var.get()
                          )
            
            parent_func(self=parent,
                        popup_output=popup_output,
                        parent=parent,
                        popup_window = self,
                        **f_kwargs)
        


        self.root_frame = ttk.Frame(self)
        self.root_frame.grid(row=0,column=0,padx=0,pady=0,sticky='nsew')
        
        self.label = ttk.Label(self.root_frame,text=self.label_text)
        self.label.grid(row=0,column=0,padx=10,pady=10,sticky='nw')
        
        self.var = tk.StringVar()
        self.var.set(self.default_var)
        self.entry = ttk.Entry(self.root_frame,
                               textvariable=self.var)
        self.entry.grid(row=1,column=0,padx=10,pady=10,sticky='ew')
        
        self.button = ttk.Button(self.root_frame,
                                text=self.button_text,
                                command=lambda: action(self)
                                )
        self.button.grid(row=2,column=0,padx=10,pady=10,sticky='se')
        
        self_col,self_row=self.root_frame.size()

        self.root_frame.rowconfigure([i for i in range(self_row)], weight=1) #Faz com que a fileria de root expanda até a borda 
        self.root_frame.columnconfigure([i for i in range(self_col)], weight=1) #Faz com que a coluna de root expanda até a borda
        
    def close(self, event=None):
        #re-enable the main window
        self.master.attributes('-disabled', False)
        #destroy this window
        self.destroy()
