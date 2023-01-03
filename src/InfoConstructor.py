# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 15:58:01 2021

@author: valter.gonzaga

Algoritimo para criação instantânea de informes
Versão = 1.0.0

Change_log:
    - Página de Edição de Cards
    
"""

import sys
import warnings

from tkmain import App

#if not sys.warnoptions:
    #warnings.simplefilter("ignore")

import ctypes
 
ctypes.windll.shcore.SetProcessDpiAwareness(1)

""""
=====================================================================
TKINTER
=====================================================================
"""
def main():
    """
    ===============================================================================
    INICIALIZAÇÃO
    ===============================================================================
    """

    #==============================================================================
    #MENSAGEM INICIAL
    #==============================================================================
    with open('display_text.html','w',encoding='utf8') as display_view:
        with open('help_text.html','r',encoding='utf8') as help_text:
            entry_message = help_text.read().replace('<self_file>',
                                                     'display_text.html'
                                                     )
        
        display_view.write(entry_message)
        display_view.close()  

    
    app = App()
    
    app.title('Info Builder v=1.0.0')
    app.state('zoomed')
    app.mainloop()  


if __name__ == "__main__":
    
    main()
