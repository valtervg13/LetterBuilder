# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 17:15:04 2022

@author: valter.gonzaga
"""
import tkinterweb as web
from cfg import html_errmessages

class HTML_viewport():
    def __init__(self):
        return None
        
    def __new__(cls,parent):

        pv_text = web.HtmlFrame(parent,
                                messages_enabled=html_errmessages
                                )
        
        with open('display_text.html','r',encoding='utf8') as display:
            pv_text.load_html(display.read())
        
        return pv_text
